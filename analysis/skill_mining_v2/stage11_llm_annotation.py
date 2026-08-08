"""Stage 11 — LLM semantic annotation via API_Tools (DeepSeek-V4-flash nothinking)."""

from __future__ import annotations

import json
import re
from typing import Any

from analysis.skill_mining_v2.common.io import ensure_dir, read_json, write_json
from analysis.skill_mining_v2.common.validation import validate_annotation_text
from analysis.skill_mining_v2.config import PipelineConfig


def _extract_json(text: str) -> dict[str, Any]:
    if not text:
        return {}
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            return {}
    return {}


def _sanitize_annotation_language(value: Any) -> Any:
    """Remove causal wording that is disallowed in evidence-only annotations."""
    if isinstance(value, dict):
        return {k: _sanitize_annotation_language(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_sanitize_annotation_language(v) for v in value]
    if not isinstance(value, str):
        return value

    replacements = (
        (r"\btherefore\b,?\s*", ""),
        (r"\bbecause\b", "with"),
        (r"\b(?:cause[sd]?|leads to|results in)\b", "is associated with"),
        (r"\bguarantee[sd]?\b", "is consistent with"),
        (r"\bincreases win rate\b", "is associated with a higher observed win rate"),
        (r"\bimproves win rate by\b", "has an observed win-rate difference of"),
        (r"\bwill win\b", "has favorable observed outcomes"),
        (r"因此", ""),
        (r"必然|导致", "与之相关"),
        (r"保证", "支持"),
    )
    for pattern, replacement in replacements:
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
    return value


def _call_llm(cfg: PipelineConfig, system: str, user: str) -> dict[str, Any]:
    from API_Tools.llm_caller import call_openai_detailed

    result = call_openai_detailed(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        model_key=cfg.llm_model_key,
        temperature=0.3,
        response_format={"type": "json_object"},
    )
    content = result.get("content") or ""
    parsed = _extract_json(content)
    return {
        "raw": content,
        "parsed": parsed,
        "error": result.get("error") or "",
        "model": result.get("model"),
        "model_key": result.get("model_key"),
    }


def _fallback_opening_name(packet: dict[str, Any]) -> dict[str, Any]:
    opening = packet.get("opening") or {}
    flags = [f.get("feature") for f in (opening.get("distinctive_flags") or [])[:4]]
    profile = opening.get("profile") or {}
    intent = []
    if profile.get("inv_expansion", 0) > 0.2:
        intent.append("expand-oriented")
    if profile.get("inv_technology", 0) > 0.15:
        intent.append("tech-oriented")
    if profile.get("inv_production", 0) > 0.25:
        intent.append("production-oriented")
    if profile.get("inv_air", 0) > 0.1:
        intent.append("air-leaning")
    name = " / ".join(intent) if intent else "balanced macro opening"
    return {
        "professional_name": name.title(),
        "data_driven_name": name,
        "macro_family": intent[0] if intent else "macro",
        "strategic_intent": f"Data-driven opening characterized by {', '.join(flags) if flags else 'mixed investments'}.",
        "supporting_facts": flags[:2] or list(profile.keys())[:2],
    }


def _fallback_state_names(packet: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for sid, info in ((packet.get("state_profiles") or {}).get("own") or {}).items():
        if not info:
            continue
        prof = info.get("profile") or {}
        # pick top investment dims
        items = sorted(
            [(k, v) for k, v in prof.items() if "cum_" in k],
            key=lambda x: -float(x[1] or 0),
        )[:3]
        label = " / ".join(k.replace("own_cum_", "") for k, _ in items) or "mixed state"
        out[sid] = {
            "name": label.title(),
            "interpretation": f"State dominated by {label}.",
        }
    for sid, info in ((packet.get("state_profiles") or {}).get("opp") or {}).items():
        if not info:
            continue
        prof = info.get("profile") or {}
        items = sorted(
            [(k, v) for k, v in prof.items() if "cum_" in k],
            key=lambda x: -float(x[1] or 0),
        )[:3]
        label = " / ".join(k.replace("opp_cum_", "") for k, _ in items) or "mixed opponent state"
        out[sid] = {
            "name": "Opp:" + label.title(),
            "interpretation": f"Opponent state dominated by {label}.",
        }
    return out


def _fallback_edges(packet: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for e in (packet.get("preferred_edges") or []) + (packet.get("harmful_edges") or []) + (
        packet.get("default_edges") or []
    ):
        rid = e.get("response_id")
        resp = (packet.get("response_clusters") or {}).get(rid) or {}
        tops = [x.get("name") for x in (resp.get("top_actions") or [])[:5] if isinstance(x, dict)]
        out.append(
            {
                "edge_id": e.get("edge_id"),
                "opponent_condition": e.get("opp_state_id"),
                "response_interpretation": f"Commit toward {', '.join(tops) if tops else rid}",
                "strategic_meaning": (
                    "Associated with comparatively better outcomes in matched contexts."
                    if e.get("edge_label") == "preferred"
                    else (
                        "Associated with comparatively worse outcomes in matched contexts."
                        if e.get("edge_label") == "harmful"
                        else "Common continuation under this opening/state."
                    )
                ),
                "edge_label": e.get("edge_label"),
            }
        )
    return out


def annotate_packet(cfg: PipelineConfig, packet: dict[str, Any], skip_llm: bool) -> dict[str, Any]:
    issues = []
    if skip_llm:
        opening_ann = _fallback_opening_name(packet)
        state_ann = _fallback_state_names(packet)
        edge_ann = _fallback_edges(packet)
        source = "heuristic_fallback"
    else:
        system = (
            "You annotate StarCraft II strategy mining results. "
            "Only explain data evidence. Never claim causality or invent unit/upgrade names. "
            "Return strict JSON."
        )
        # Pass A
        user_a = json.dumps(
            {
                "task": "opening_naming",
                "opening_id": packet.get("opening_id"),
                "opening": packet.get("opening"),
                "medoid": packet.get("medoid"),
                "requirements": [
                    "professional_name",
                    "data_driven_name",
                    "macro_family",
                    "strategic_intent",
                    "supporting_facts (>=2 data facts)",
                ],
            },
            ensure_ascii=False,
        )
        a = _call_llm(cfg, system, user_a)
        opening_ann = a.get("parsed") or _fallback_opening_name(packet)
        if a.get("error"):
            issues.append(f"passA:{a['error']}")

        # Pass B
        user_b = json.dumps(
            {
                "task": "state_naming",
                "states": packet.get("state_profiles"),
            },
            ensure_ascii=False,
        )
        b = _call_llm(cfg, system, user_b)
        state_ann = b.get("parsed") or _fallback_state_names(packet)
        if isinstance(state_ann, dict) and "states" in state_ann:
            state_ann = state_ann["states"]
        if b.get("error"):
            issues.append(f"passB:{b['error']}")

        # Pass C
        user_c = json.dumps(
            {
                "task": "edge_interpretation",
                "preferred": packet.get("preferred_edges")[:10],
                "harmful": packet.get("harmful_edges")[:10],
                "default": packet.get("default_edges")[:10],
                "responses": packet.get("response_clusters"),
                "knowledge": packet.get("sc2_knowledge"),
                "note": "Do NOT decide preferred/harmful; labels already given. Only interpret.",
            },
            ensure_ascii=False,
        )
        c = _call_llm(cfg, system, user_c)
        edge_ann = c.get("parsed")
        if isinstance(edge_ann, dict):
            edge_ann = edge_ann.get("edges") or edge_ann.get("interpretations") or _fallback_edges(packet)
        if not edge_ann:
            edge_ann = _fallback_edges(packet)
        if c.get("error"):
            issues.append(f"passC:{c['error']}")
        source = "llm"

    # Enforce evidence-only wording even when the provider ignores the prompt.
    opening_ann = _sanitize_annotation_language(opening_ann)
    state_ann = _sanitize_annotation_language(state_ann)
    edge_ann = _sanitize_annotation_language(edge_ann)

    # validate language
    blob = json.dumps({"opening": opening_ann, "states": state_ann, "edges": edge_ann}, ensure_ascii=False)
    issues.extend(validate_annotation_text(blob))

    return {
        "opening_id": packet.get("opening_id"),
        "opening_annotation": opening_ann,
        "state_annotations": state_ann,
        "edge_annotations": edge_ann,
        "source": source,
        "issues": issues,
        "run_id": cfg.run_id,
        "model_key": cfg.llm_model_key,
    }


def run_stage11(cfg: PipelineConfig) -> dict[str, Any]:
    out_dir = ensure_dir(cfg.stage_dir(11, "11_annotations"))
    packet_index = read_json(cfg.stage_dir(10, "10_annotation_packets") / "packet_index.json")
    index = {}
    for opening_id, rel in packet_index.items():
        out_path = out_dir / f"annotation_{opening_id}.json"
        if cfg.resume and out_path.exists():
            index[opening_id] = str(out_path.relative_to(cfg.output_root))
            continue
        packet = read_json(cfg.output_root / rel)
        ann = annotate_packet(cfg, packet, skip_llm=cfg.skip_llm)
        write_json(out_path, ann)
        index[opening_id] = str(out_path.relative_to(cfg.output_root))
        print(f"[stage11] annotated {opening_id} source={ann['source']}", flush=True)
    write_json(out_dir / "annotation_index.json", index)
    return {"index": index}
