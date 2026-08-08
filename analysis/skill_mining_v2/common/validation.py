"""Validation helpers for skill_mining_v2 pipeline outputs."""

from __future__ import annotations

import re
from typing import Any, Iterable

import pandas as pd

from analysis.skill_mining_v2.common.io import loads_actions

CAUSAL_LANGUAGE_PATTERNS = [
    r"\bcause[sd]?\b",
    r"\bbecause\b",
    r"\bleads to\b",
    r"\bresults in\b",
    r"\btherefore\b",
    r"\bguarantee[sd]?\b",
    r"\bincreases win rate\b",
    r"\bwill win\b",
    r"\bimproves win rate by\b",
    r"\b必然\b",
    r"\b导致\b",
    r"\b因此\b",
    r"\b保证\b",
]


def check_temporal_leakage(
    feature_times: dict[str, float],
    decision_time: float,
    *,
    tolerance: float = 0.0,
) -> list[str]:
    """Return feature names whose timestamp exceeds decision_time (potential leakage)."""
    leaks: list[str] = []
    for name, t in feature_times.items():
        if t is None:
            continue
        if float(t) > decision_time + tolerance:
            leaks.append(name)
    return leaks


def check_time_leakage_opening(actions: list[dict[str, Any]], horizon: float) -> bool:
    """Return True if all actions are within horizon (sanity check)."""
    return all(
        a.get("second") is None or float(a["second"]) <= horizon + 1e-6 for a in actions
    )


def validate_no_future_actions(actions: list[dict[str, Any]], cutoff: float) -> bool:
    return check_time_leakage_opening(actions, cutoff)


def validate_graph_structure(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate temporal DAG structure of a strategy graph."""
    issues: list[str] = []
    node_ids = {n.get("id") for n in nodes}
    times = {n.get("id"): n.get("time") for n in nodes}

    for e in edges:
        src = e.get("from") or e.get("source")
        dst = e.get("to") or e.get("target")
        if src not in node_ids or dst not in node_ids:
            issues.append(f"missing node for edge {src}->{dst}")
            continue
        t_src, t_dst = times.get(src), times.get(dst)
        if t_src is not None and t_dst is not None and float(t_dst) <= float(t_src):
            issues.append(f"non-forward edge {src}({t_src})->{dst}({t_dst})")

    adj: dict[Any, list[Any]] = {nid: [] for nid in node_ids}
    for e in edges:
        src = e.get("from") or e.get("source")
        dst = e.get("to") or e.get("target")
        if src in adj and dst in adj:
            adj[src].append(dst)

    visited: set[Any] = set()
    stack: set[Any] = set()

    def dfs(u: Any) -> bool:
        if u in stack:
            return True
        if u in visited:
            return False
        visited.add(u)
        stack.add(u)
        for v in adj.get(u, []):
            if dfs(v):
                return True
        stack.remove(u)
        return False

    for nid in node_ids:
        if dfs(nid):
            issues.append("cycle detected")
            break

    return {"valid": len(issues) == 0, "issues": issues, "n_nodes": len(nodes), "n_edges": len(edges)}


def validate_graph(graph: dict[str, Any]) -> list[str]:
    """Legacy wrapper around validate_graph_structure."""
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    return validate_graph_structure(nodes, edges)["issues"]


def validate_skill_grounding(
    skill: dict[str, Any],
    evidence: dict[str, Any] | None = None,
    graph: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Check that skill claims are grounded in evidence / graph edges."""
    issues: list[str] = []
    for key in ("opening_id", "race", "directional_matchup"):
        if not skill.get(key):
            issues.append(f"missing skill.{key}")

    if evidence:
        for key in ("support", "representative_replays"):
            if key not in evidence:
                issues.append(f"missing evidence.{key}")
        support = evidence.get("support")
        if support is not None and int(support) <= 0:
            issues.append("evidence.support must be positive")
        if not evidence.get("representative_replays"):
            issues.append("evidence.representative_replays must not be empty")

    if graph is not None:
        edge_map = {e.get("edge_id"): e for e in graph.get("edges", []) if e.get("edge_id")}
        for rule in skill.get("preferred_rules", []):
            eid = rule.get("evidence_id") or rule.get("edge_id")
            if not eid or eid not in edge_map:
                issues.append(
                    f"preferred rule {rule.get('rule_id')} references missing edge {eid}"
                )
            elif edge_map[eid].get("edge_label") != "preferred":
                issues.append(f"preferred rule {rule.get('rule_id')} not grounded in preferred edge")
        for rule in skill.get("avoid_rules", []):
            eid = rule.get("evidence_id") or rule.get("edge_id")
            if not eid or eid not in edge_map:
                issues.append(
                    f"avoid rule {rule.get('rule_id')} references missing edge {eid}"
                )
            elif edge_map[eid].get("edge_label") != "harmful":
                issues.append(f"avoid rule {rule.get('rule_id')} not grounded in harmful edge")

    preferred = skill.get("preferred_edges") or []
    harmful = skill.get("harmful_edges") or []
    for edge in preferred + harmful:
        if "lift" not in edge and "adjusted_lift" not in edge:
            issues.append(f"edge missing lift: {edge.get('id', edge)}")

    return {"valid": len(issues) == 0, "issues": issues}


def validate_canonical_entities(
    entities: Iterable[str],
    kb_names: set[str] | frozenset[str] | dict[str, Any],
) -> dict[str, Any]:
    """Check entity names against SC2 knowledge base."""
    if isinstance(kb_names, dict):
        known = set(kb_names.get("units", {})) | set(kb_names.get("upgrades", {})) | set(
            kb_names.get("abilities", {})
        )
    else:
        known = set(kb_names)
    unknown = sorted(
        {
            e
            for e in entities
            if e
            and e not in known
            and e not in {"Unknown", "Combat", "Gas", "Base"}
            and not any(str(e).startswith(p) for p in ("Combat_", "Prod_", "Tech_", "Static_", "Upgrade_"))
        }
    )
    return {"valid": len(unknown) == 0, "unknown_entities": unknown, "n_checked": len(list(entities))}


def load_kb_entity_names(kb: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for _section, items in kb.items():
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and "name" in item:
                    names.add(str(item["name"]))
    return names


def detect_causal_language(text: str) -> list[str]:
    """Flag causal/overclaim phrases in annotation text."""
    hits: list[str] = []
    for pat in CAUSAL_LANGUAGE_PATTERNS:
        if re.search(pat, text or "", flags=re.IGNORECASE):
            hits.append(pat)
    return hits


def validate_annotation_text(text: str) -> list[str]:
    return [f"causal_language:{pat}" for pat in detect_causal_language(text)]


def validate_annotation_packet(
    packet: dict[str, Any],
    *,
    kb_names: set[str] | dict[str, Any] | None = None,
) -> dict[str, Any]:
    issues: list[str] = []
    for field in ("summary", "strategy_description", "transition_rationale"):
        text = packet.get(field)
        if text:
            issues.extend(validate_annotation_text(str(text)))
    entities = packet.get("entities") or []
    if kb_names is not None:
        ent_val = validate_canonical_entities(entities, kb_names)
        issues.extend(ent_val["unknown_entities"])
    return {"valid": len(issues) == 0, "issues": issues}


def row_actions(row: Any) -> list[dict[str, Any]]:
    if hasattr(row, "get"):
        return loads_actions(row.get("own_actions"))
    return loads_actions(getattr(row, "own_actions", None))


def summarize_validation_reports(reports: list[dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(reports)
