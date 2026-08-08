"""Stage 02 — SC2 semantic enrichment indexes."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from analysis.skill_mining_v2.common.io import ensure_dir, read_json, write_json
from analysis.skill_mining_v2.config import PipelineConfig


def _index_entities(db: dict[str, Any]) -> dict[str, Any]:
    units = {}
    for u in db.get("Unit") or []:
        name = u.get("name")
        if not name:
            continue
        units[name] = {
            "race": u.get("race"),
            "entity_type": u.get("type") or u.get("entity_type") or "Unit",
            "attributes": u.get("attributes") or [],
        }
    upgrades = {}
    for u in db.get("Upgrade") or []:
        name = u.get("name")
        if not name:
            continue
        upgrades[name] = {"race": u.get("race")}
    abilities = {}
    for a in db.get("Ability") or []:
        name = a.get("name")
        if not name:
            continue
        abilities[name] = {
            "race": a.get("race"),
            "friendly_name": a.get("friendly_name") or a.get("button_name"),
        }
    subont = {}
    for s in db.get("SubOntology") or []:
        name = s.get("name")
        if name:
            subont[name] = {"members": s.get("members") or s.get("unit_names") or []}
    return {
        "units": units,
        "upgrades": upgrades,
        "abilities": abilities,
        "subontology": subont,
    }


def _index_relations(db: dict[str, Any], rel_path) -> dict[str, Any]:
    """Build action_semantic_index from relations + entity fields."""
    by_entity: dict[str, dict[str, list]] = defaultdict(
        lambda: {
            "produces": [],
            "researches": [],
            "counters": [],
            "synergizes_with": [],
            "requires": [],
            "enables_morph": [],
            "grants_stat_bonus": [],
            "ability_requires_unit": [],
            "ability_requires_upgrade": [],
            "action_result": [],
        }
    )

    relations = []
    # relations may live inside db or separate file
    if isinstance(db.get("Relation"), list):
        relations.extend(db["Relation"])
    if rel_path and rel_path.exists():
        try:
            payload = read_json(rel_path)
            if isinstance(payload, dict):
                relations.extend(payload.get("relations") or payload.get("Relation") or [])
            elif isinstance(payload, list):
                relations.extend(payload)
        except Exception as exc:
            print(f"[stage02] warn: cannot load relations ({exc})", flush=True)

    keep = {
        "produces",
        "researches",
        "counters",
        "synergizes_with",
        "enables_morph",
        "grants_stat_bonus",
        "ability_requires_unit",
        "ability_requires_upgrade",
        "action_result",
        "requires",
        "has_ability",
    }
    for rel in relations:
        rtype = rel.get("relation")
        if rtype not in keep:
            continue
        subj = rel.get("subject_name")
        obj = rel.get("object_name")
        if not subj or not obj:
            continue
        key = rtype if rtype in by_entity[subj] else "requires"
        if rtype == "has_ability":
            key = "requires"
        bucket = by_entity[subj][key]
        if obj not in bucket:
            bucket.append(obj)
        # inverse light index for action_result
        if rtype == "action_result":
            by_entity[obj]["requires"].append(subj)

    # compact
    action_index = {}
    for ent, payload in by_entity.items():
        cleaned = {k: v for k, v in payload.items() if v}
        if cleaned:
            action_index[ent] = cleaned
    return action_index


def run_stage02(cfg: PipelineConfig) -> dict[str, Any]:
    out_dir = ensure_dir(cfg.stage_dir(2, "02_semantics"))
    entity_path = out_dir / "entity_index.json"
    action_path = out_dir / "action_semantic_index.json"
    if cfg.resume and entity_path.exists() and action_path.exists():
        print(f"[stage02] resume {out_dir}", flush=True)
        return {
            "entity_index": read_json(entity_path),
            "action_semantic_index": read_json(action_path),
        }

    db = read_json(cfg.sc2_knowledge_path)
    entity_index = _index_entities(db)
    rel_path = cfg.repo_root / "data_sc2_260701" / "relations" / "entity_expanded_relations.json"
    action_index = _index_relations(db, rel_path)

    write_json(entity_path, entity_index)
    write_json(action_path, action_index)
    meta = {
        "n_units": len(entity_index["units"]),
        "n_upgrades": len(entity_index["upgrades"]),
        "n_abilities": len(entity_index["abilities"]),
        "n_semantic_entities": len(action_index),
        "run_id": cfg.run_id,
    }
    write_json(out_dir / "semantics_summary.json", meta)
    print(f"[stage02] entities={meta['n_units']} semantics={meta['n_semantic_entities']}", flush=True)
    return {"entity_index": entity_index, "action_semantic_index": action_index, **meta}
