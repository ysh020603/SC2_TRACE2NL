from __future__ import annotations

import shutil

from .common.io import read_json, write_json, write_text
from .common.method_policy import policy
from .config import PipelineConfig

METHOD_NAMES = {
    "full_signed_graph": "Full Signed Graph", "ablation_single_trace": "Single Trace",
    "ablation_static_population": "Static Population", "ablation_flat_adaptive": "Flat Adaptive",
    "ablation_positive_only": "Positive Only", "ablation_frequency_only": "Frequency Only",
}


def _trim(text: str, max_words: int = 80) -> str:
    words = str(text or "").split()
    return " ".join(words[:max_words]) + ("…" if len(words) > max_words else "")


def _children(projection: dict) -> dict[str, list[str]]:
    if not policy(projection["method"])["graph"]:
        return {node["node_id"]: [] for node in projection.get("nodes", [])}
    by_source = {}
    for node in projection.get("nodes", []):
        for state in node.get("source_state_ids", []):
            by_source.setdefault(state, []).append(node["node_id"])
    result = {}
    for node in projection.get("nodes", []):
        ids = [x for x in by_source.get(node.get("next_state_id"), []) if x != node["node_id"]]
        result[node["node_id"]] = ids[:3]
    return result


def _root_markdown(projection: dict, annotation: dict) -> str:
    opening = annotation["opening"]
    method = projection["method"]
    sections = [
        f"# {opening['opening_name']}", "", "## Skill Identity", "",
        f"- Skill ID: {projection['opening_id']}", f"- Matchup: {projection['race']} vs {projection['opponent_race']}",
        f"- Opening Family: {opening['opening_family']}", f"- Method: {METHOD_NAMES[method]}", "",
        "## Opening Strategy", "", opening["opening_summary"], "", opening["strategic_goal"], "", opening["flexibility_note"], "",
        "## Strategic Characteristics", "", f"- Economy: {opening['economy_character']}", f"- Production: {opening['production_character']}",
        f"- Technology: {opening['technology_character']}", f"- Army direction: {opening['army_character']}", "",
        "## Strategic Priorities", "", "- Preserve the opening's strategic identity without reproducing a fixed sequence.",
        "- Check current Completed, Under Construction, Active Queues, resources, supply, and prerequisites before choosing exact macro actions.",
        "- Match any adaptation against partial Enemy Intelligence and current Threat Flags.",
        "- Re-evaluate economy, production, technology, and army trade-offs at every decision.", "", "## Decision Nodes", "",
    ]
    for node in annotation.get("nodes", []):
        badge = node["node_type"].upper()
        label = "Risk direction" if badge == "NEGATIVE" else "Direction"
        sections.extend([
            f"### [{badge}] {node['node_id']} — {node['title']}", "", "**Trigger situation:**  ", _trim(node["trigger_summary"], 55), "",
            f"**{label}:**  ", _trim(node["decision_direction"] if badge != "NEGATIVE" else node["avoid_direction"], 40), "",
            f"**Read for details:** `{node['node_id']}`", "", "---", "",
        ])
    return "\n".join(sections)


def _node_markdown(node: dict, child_ids: list[str], by_id: dict[str, dict], method: str) -> str:
    badge = node["node_type"].upper()
    summary_direction = node["avoid_direction"] if badge == "NEGATIVE" else node["decision_direction"]
    summary = _trim(f"{node['trigger_summary']} {summary_direction}", 80)
    lines = [f"# {node['node_id']} — {node['title']}", "", "## Node Type", "", badge, "", "## Summary", "", summary, "", "## When This Applies", ""]
    if node.get("opponent_situation"):
        lines.extend(["### Opponent cues", "", f"- {node['opponent_situation']}", "- Treat remembered or observed Enemy Intelligence as partial and uncertain.", ""])
    lines.extend(["### Own cues", "", f"- {node['own_situation']}", "- Use the live observation to check army supply, free supply, resource bank, technology, and current queues.", "- These cues are approximate and do not all need to be true.", ""])
    if badge == "NEGATIVE":
        lines.extend(["## Risk Direction", "", "Historical matched contexts associate this broad direction with worse outcomes; the evidence is associative, not causal.", "", node["avoid_direction"], "", "## Safer Re-evaluation", "", node["exit_or_recheck_condition"], ""])
    else:
        lines.extend(["## Recommended Strategic Direction", "", node["decision_direction"], "", node["strategic_reason"], ""])
    lines.extend(["## What This Does NOT Mean", "", "This node is not an instruction to reproduce a historical action sequence.", "", "Choose exact macro actions from the current live observation, not merely because a unit or structure appeared in historical evidence.", "", "## Transition Goal", "", node["transition_goal"], ""])
    if child_ids:
        lines.extend(["## Possible Next Situations", ""])
        for child_id in child_ids:
            child = by_id[child_id]
            lines.extend([f"### {child_id} — {child['title']}", "", f"**Situation:** {_trim(child['trigger_summary'], 35)}", "", f"**Direction:** {_trim(child['decision_direction'], 30)}", "", f"**Read:** `{child_id}`", ""])
    return "\n".join(lines)


def compile_one(cfg: PipelineConfig, projection: dict, semantic: dict) -> dict:
    method, opening_id = projection["method"], projection["opening_id"]
    annotation = semantic["annotation"]
    matchup, race_dir = opening_id[:3], projection["race"].lower()
    dest = cfg.skill_root / method / race_dir / matchup / opening_id
    dest.mkdir(parents=True, exist_ok=True)
    children = _children(projection)
    ann_by_id = {node["node_id"]: node for node in annotation.get("nodes", [])}
    write_text(dest / "SKILL.md", _root_markdown(projection, annotation))
    index_nodes = {}
    for node_id, node in ann_by_id.items():
        path = dest / "nodes" / f"{node_id}.md"
        write_text(path, _node_markdown(node, children.get(node_id, []), ann_by_id, method))
        summary_direction = node["avoid_direction"] if node["node_type"] == "negative" else node["decision_direction"]
        index_nodes[node_id] = {
            "path": f"nodes/{node_id}.md", "type": node["node_type"], "title": node["title"],
            "summary": _trim(f"{node['trigger_summary']} {summary_direction}", 80),
            "trigger_summary": _trim(node["trigger_summary"], 55), "children": children.get(node_id, []),
        }
    index = {"skill_id": opening_id, "opening_name": annotation["opening"]["opening_name"], "method": method, "root": "SKILL.md", "nodes": index_nodes}
    write_json(dest / "index.json", index)
    prov = dest / "provenance"
    prov.mkdir(exist_ok=True)
    ir_path = cfg.stage_dir(1) / method / f"{opening_id}.json"
    projection_path = cfg.stage_dir(2) / method / f"{opening_id}.json"
    annotation_path = cfg.stage_dir(3) / method / f"{opening_id}.json"
    shutil.copyfile(ir_path, prov / "method_ir.json")
    shutil.copyfile(projection_path, prov / "observation_projection.json")
    shutil.copyfile(annotation_path, prov / "semantic_annotation.json")
    write_json(prov / "source_mapping.json", {node["node_id"]: {"source_state_ids": node.get("source_state_ids", []), "source_edge_ids": node.get("source_edge_ids", [])} for node in projection.get("nodes", [])})
    return {"path": str(dest.relative_to(cfg.skill_root)), "nodes": len(index_nodes), "annotation_source": semantic.get("annotation_source")}


def run(cfg: PipelineConfig) -> dict:
    projection_index = read_json(cfg.stage_dir(2) / "index.json")
    annotation_index = read_json(cfg.stage_dir(3) / "index.json")
    index = {}
    for method, openings in annotation_index.items():
        for opening_id, rel in openings.items():
            projection = read_json(cfg.output_root / projection_index[method][opening_id])
            semantic = read_json(cfg.output_root / rel)
            index.setdefault(method, {})[opening_id] = compile_one(cfg, projection, semantic)
    write_json(cfg.stage_dir(4) / "index.json", index)
    return index
