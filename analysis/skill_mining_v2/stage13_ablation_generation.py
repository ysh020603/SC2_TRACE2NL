"""Stage 13 — generate ablation skill variants from the same mined evidence."""

from __future__ import annotations

import copy
from typing import Any

import pandas as pd

from analysis.skill_mining_v2.common.io import ensure_dir, estimate_tokens, read_json, write_json
from analysis.skill_mining_v2.common.validation import validate_graph
from analysis.skill_mining_v2.config import PipelineConfig


METHODS = {
    "ablation_single_trace": {
        "population": False,
        "opponent_adaptive": False,
        "graph": False,
        "negative": False,
        "value_filtering": False,
    },
    "ablation_static_population": {
        "population": True,
        "opponent_adaptive": False,
        "graph": False,
        "negative": False,
        "value_filtering": False,
    },
    "ablation_flat_adaptive": {
        "population": True,
        "opponent_adaptive": True,
        "graph": False,
        "negative": True,
        "value_filtering": True,
    },
    "ablation_positive_only": {
        "population": True,
        "opponent_adaptive": True,
        "graph": True,
        "negative": False,
        "value_filtering": True,
    },
    "ablation_frequency_only": {
        "population": True,
        "opponent_adaptive": True,
        "graph": True,
        "negative": True,
        "value_filtering": False,
    },
}


def _load_full_skill(cfg: PipelineConfig, opening_id: str, rel_path: str) -> dict[str, Any]:
    root = cfg.repo_root / rel_path
    return {
        "skill": read_json(root / "skill.json"),
        "evidence": read_json(root / "evidence.json"),
        "graph": read_json(root / "strategy_graph.json"),
        "annotation": read_json(root / "annotation.json"),
        "path": root,
    }


def _single_trace_skill(full: dict[str, Any], trace: dict[str, Any] | None) -> dict[str, Any]:
    skill = copy.deepcopy(full["skill"])
    skill["method"] = "ablation_single_trace"
    skill["preferred_rules"] = []
    skill["avoid_rules"] = []
    skill["default_evolution"] = [
        {
            "step_id": f"{skill['skill_id']}_TRACE_01",
            "phase": [0, 600],
            "description": "Follow one winning trajectory nearest to the opening medoid.",
            "prototype": (
                [x.strip() for x in str(trace.get("key_sequence") or "").split(">") if x.strip()]
                if trace
                else skill["opening"].get("prototype") or []
            ),
            "source_trace": trace,
        }
    ]
    skill["strategy_graph"] = None
    return skill


def _static_population_skill(full: dict[str, Any]) -> dict[str, Any]:
    skill = copy.deepcopy(full["skill"])
    skill["method"] = "ablation_static_population"
    skill["preferred_rules"] = []
    skill["avoid_rules"] = []
    # keep only default evolution, strip opponent conditions
    cleaned = []
    for step in skill.get("default_evolution") or []:
        s = dict(step)
        s.pop("opponent_condition", None)
        cleaned.append(s)
    skill["default_evolution"] = cleaned
    skill["strategy_graph"] = None
    return skill


def _flat_adaptive_skill(full: dict[str, Any]) -> dict[str, Any]:
    skill = copy.deepcopy(full["skill"])
    skill["method"] = "ablation_flat_adaptive"
    skill["strategy_graph"] = None
    # keep rules but remove next_state / path linkage emphasis
    for rule in skill.get("preferred_rules") or []:
        rule = rule
        rule["next_state"] = None
    for rule in skill.get("avoid_rules") or []:
        rule["next_state"] = None
    return skill


def _positive_only_skill(full: dict[str, Any]) -> dict[str, Any]:
    skill = copy.deepcopy(full["skill"])
    graph = copy.deepcopy(full["graph"])
    skill["method"] = "ablation_positive_only"
    skill["avoid_rules"] = []
    graph["edges"] = [
        e for e in graph.get("edges") or [] if e.get("edge_label") in {"preferred", "default"}
    ]
    return skill, graph


def _frequency_only_skill(full: dict[str, Any], edges_df: pd.DataFrame) -> tuple[dict[str, Any], dict[str, Any]]:
    skill = copy.deepcopy(full["skill"])
    graph = copy.deepcopy(full["graph"])
    skill["method"] = "ablation_frequency_only"
    oid = skill["skill_id"]
    sub = edges_df[edges_df["opening_id"] == oid] if len(edges_df) else edges_df
    if len(sub):
        # take top frequency responses ignoring adjusted lift
        top = sub.sort_values("p_response", ascending=False).groupby("own_state_id").head(3)
        pref = []
        avoid = []
        for i, e in enumerate(top.itertuples()):
            pref.append(
                {
                    "rule_id": f"{oid}_FREQ_{i+1:02d}",
                    "phase": [int(e.t), int(e.t) + 60],
                    "own_state": e.own_state_id,
                    "opponent_condition": e.opp_state_id,
                    "response": e.response_id,
                    "canonical_actions": [],
                    "next_state": getattr(e, "next_own_state_id", None),
                    "evidence_id": getattr(e, "edge_id", f"freq_{i}"),
                    "selection": "frequency_only",
                }
            )
        skill["preferred_rules"] = pref
        skill["avoid_rules"] = avoid
        # rebuild simple graph edges from frequency selection
        freq_ids = set(getattr(e, "edge_id", None) for e in top.itertuples())
        graph["edges"] = [
            e for e in graph.get("edges") or [] if e.get("edge_id") in freq_ids or str(e.get("edge_id", "")).startswith("synthetic")
        ]
    return skill, graph


def run_stage13(cfg: PipelineConfig) -> dict[str, Any]:
    out_dir = ensure_dir(cfg.stage_dir(13, "13_ablations"))
    full_index = read_json(cfg.stage_dir(12, "12_skills") / "skill_index.json")
    medoids = read_json(cfg.stage_dir(4, "04_openings") / "opening_medoid.json")
    edges_path = cfg.stage_dir(8, "08_transition_value") / "edge_values.parquet"
    edges_df = pd.read_parquet(edges_path) if edges_path.exists() else pd.DataFrame()

    catalog = []
    for opening_id, rel in full_index.items():
        full = _load_full_skill(cfg, opening_id, rel)
        race_dir = full["skill"]["race"].lower()
        dmu = full["skill"]["directional_matchup"]
        medoid_info = medoids.get(opening_id) or {}
        winning_seeds = list(medoid_info.get("winning_trace_seeds") or [])
        # Old/pilot artifacts may not contain winning seeds. Never label a losing
        # medoid as a winning single-trace baseline.
        if not winning_seeds and medoid_info.get("is_win") == 1:
            winning_seeds = [medoid_info]
        primary_trace = winning_seeds[0] if winning_seeds else None

        variants: dict[str, tuple[dict[str, Any], dict[str, Any] | None]] = {}
        variants["ablation_single_trace"] = (
            _single_trace_skill(full, primary_trace),
            None,
        )
        variants["ablation_static_population"] = (_static_population_skill(full), None)
        variants["ablation_flat_adaptive"] = (_flat_adaptive_skill(full), None)
        pos_skill, pos_graph = _positive_only_skill(full)
        variants["ablation_positive_only"] = (pos_skill, pos_graph)
        freq_skill, freq_graph = _frequency_only_skill(full, edges_df)
        variants["ablation_frequency_only"] = (freq_skill, freq_graph)

        for method, (skill, graph) in variants.items():
            dest = ensure_dir(cfg.skill_root / method / race_dir / dmu / opening_id)
            write_json(dest / "skill.json", skill)
            write_json(dest / "evidence.json", full["evidence"] if method != "ablation_single_trace" else {
                "source_trace": primary_trace,
                "note": "single-trace ablation: population statistics withheld",
            })
            if graph is not None:
                write_json(dest / "strategy_graph.json", graph)
            elif method in {"ablation_positive_only", "ablation_frequency_only"}:
                write_json(dest / "strategy_graph.json", full["graph"])
            write_json(dest / "annotation.json", full["annotation"])
            meta = {
                "source_opening": opening_id,
                "method": method,
                "shared_rules": [r.get("rule_id") for r in skill.get("preferred_rules") or []],
                "removed_information": [
                    k for k, v in METHODS[method].items() if v is False
                ],
                "source_trace_ids": [s.get("replay_id") for s in winning_seeds],
                "token_estimate": estimate_tokens(skill),
                "rule_count": len(skill.get("preferred_rules") or [])
                + len(skill.get("avoid_rules") or [])
                + len(skill.get("default_evolution") or []),
                "flags": METHODS[method],
            }
            write_json(dest / "ablation_metadata.json", meta)
            validation_issues = []
            if not skill.get("skill_id") or not skill.get("opening_id"):
                validation_issues.append("missing skill/opening id")
            if graph is not None:
                validation_issues.extend(validate_graph(graph))
            if method == "ablation_single_trace" and primary_trace is None:
                validation_issues.append("no winning trace available")
            write_json(
                dest / "validation_report.json",
                {
                    "ok": not validation_issues,
                    "method": method,
                    "issues": validation_issues,
                },
            )
            catalog.append(
                {
                    "method": method,
                    "skill_id": opening_id,
                    "path": str(dest.relative_to(cfg.repo_root)),
                    **METHODS[method],
                    "token_estimate": meta["token_estimate"],
                    "rule_count": meta["rule_count"],
                }
            )

            if method == "ablation_single_trace":
                seed_index = []
                for seed_no, trace in enumerate(winning_seeds[:5], start=1):
                    seed_skill = _single_trace_skill(full, trace)
                    seed_skill["skill_id"] = f"{opening_id}_SEED_{seed_no:02d}"
                    seed_dir = ensure_dir(dest / f"seed_{seed_no:02d}")
                    write_json(seed_dir / "single_trace_skill.json", seed_skill)
                    write_json(
                        seed_dir / "evidence.json",
                        {
                            "source_trace": trace,
                            "note": "winning trajectory nearest to cluster medoid",
                        },
                    )
                    seed_index.append(
                        {
                            "seed": seed_no,
                            "replay_id": trace.get("replay_id"),
                            "distance_to_medoid": trace.get("distance_to_medoid"),
                            "path": str(seed_dir.relative_to(cfg.repo_root)),
                        }
                    )
                write_json(dest / "seed_index.json", seed_index)

    write_json(out_dir / "ablation_index.json", catalog)
    lines = [
        "# Ablation Catalog",
        "",
        "| Method | Population | Opponent-adaptive | Graph | Negative Path | Value Filtering |",
        "|---|---:|---:|---:|---:|---:|",
        "| Single Trace | No | Limited | No | No | No |",
        "| Static Population | Yes | No | No | No | No |",
        "| Flat Adaptive | Yes | Yes | No | Yes | Yes |",
        "| Graph Positive | Yes | Yes | Yes | No | Yes |",
        "| Graph Signed | Yes | Yes | Yes | Yes | Yes |",
        "| Frequency Only | Yes | Yes | Yes | Optional | No |",
        "",
        f"Generated variant artifacts: {len(catalog)}",
        "",
    ]
    (out_dir / "ablation_catalog.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[stage13] ablation artifacts={len(catalog)}", flush=True)
    return {"catalog": catalog}
