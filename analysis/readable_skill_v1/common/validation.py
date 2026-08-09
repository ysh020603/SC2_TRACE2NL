from __future__ import annotations

import re
from pathlib import Path

from .io import read_json
from .method_policy import allowed_badges, policy
from .obs_vocabulary import load_vocabulary

INTERNAL = ("canonical_actions", "response_id", "edge_id", "own_state_id", "opponent_state_id", "opp_state_id", "OWN_S", "OPP_S", "→")


def validate_skill(skill_dir: Path, method: str, entity_path: Path) -> list[str]:
    errors = []
    index_path = skill_dir / "index.json"
    root_path = skill_dir / "SKILL.md"
    if not index_path.exists() or not root_path.exists():
        return ["missing SKILL.md or index.json"]
    index = read_json(index_path)
    if index.get("method") != method or index.get("root") != "SKILL.md":
        errors.append("index method/root mismatch")
    texts = [root_path.read_text(encoding="utf-8")]
    for node_id, item in (index.get("nodes") or {}).items():
        rel = Path(item.get("path", ""))
        if rel.is_absolute() or ".." in rel.parts or rel.parts[:1] != ("nodes",):
            errors.append(f"unsafe node path: {node_id}")
            continue
        path = skill_dir / rel
        if not path.exists():
            errors.append(f"missing node path: {node_id}")
            continue
        texts.append(path.read_text(encoding="utf-8"))
        if item.get("type", "").upper() not in allowed_badges(method):
            errors.append(f"disallowed badge: {node_id}/{item.get('type')}")
        for child in item.get("children") or []:
            if child not in index["nodes"]:
                errors.append(f"missing child: {node_id}->{child}")
        if not policy(method)["graph"] and item.get("children"):
            errors.append(f"graph child in non-graph method: {node_id}")
    blob = "\n".join(texts)
    lower = blob.lower()
    for token in INTERNAL:
        if token.lower() in lower:
            errors.append(f"internal/action-list leakage: {token}")
    if re.search(r"\b(?:the opponent|enemy)\s+(?:built|ordered)\s+exactly\b", lower):
        errors.append("oracle opponent assertion")
    vocabulary = load_vocabulary(entity_path)
    for name in vocabulary:
        if re.search(rf"\b\d+\s+{re.escape(name)}s?\b", blob, re.I):
            errors.append(f"exact replay-derived count: {name}")
    boundary = {
        "ablation_single_trace": ("population", "[positive]", "[negative]", "preferred", "harmful"),
        "ablation_static_population": ("[positive]", "[negative]", "preferred", "harmful"),
        "ablation_flat_adaptive": ("possible next situations", "graph successor", "multi-hop transition"),
        "ablation_positive_only": ("[negative]", "harmful", "worse outcomes"),
        "ablation_frequency_only": ("[positive]", "preferred", "better outcome", "adjusted lift", "win enrichment"),
    }.get(method, ())
    for term in boundary:
        if term in lower:
            errors.append(f"ablation leakage: {term}")
    return sorted(set(errors))
