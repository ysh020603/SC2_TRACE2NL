from analysis.readable_skill_v1.common.knowledge_grounding import KnowledgeStore
from analysis.readable_skill_v1.stage03_llm_semantic_annotation import _deterministic_knowledge_sanitize, _merge_opening_defaults, _public_node_projection


def _unit(name, race, flying, targets, attributes=()):
    return {
        "name": name,
        "race": race,
        "is_flying": flying,
        "is_structure": False,
        "weapons": [{"target_type": target} for target in targets],
        "attributes": list(attributes),
        "tech_chain": [f"Example chain for {name}"],
        "minerals": 100,
        "gas": 25,
        "supply": 2,
    }


def _relation(relation_id, subject, obj):
    return {
        "relation_id": relation_id,
        "subject_name": subject,
        "subject_type": "Unit",
        "relation": "counters",
        "object_name": obj,
        "object_type": "Unit",
        "description": [f"{subject} has an advantage over {obj}."],
        "source": [{"kind": "subontology_expansion", "fact_ids": [f"fact-{relation_id}"]}],
        "fact": [{"fact_id": f"fact-{relation_id}"}],
    }


def _store():
    base = {
        "Unit": [
            _unit("Adept", "Protoss", False, ["Ground"], ["Light"]),
            _unit("Stalker", "Protoss", False, ["Any"], ["Armored"]),
            _unit("Banshee", "Terran", True, ["Ground"], ["Light"]),
            _unit("Marine", "Terran", False, ["Any"], ["Light"]),
        ],
        "Upgrade": [],
        "Ability": [],
        "SubOntology": [],
    }
    unrelated = _relation("adept-marine", "Adept", "Marine")
    unrelated["relation"] = "synergizes_with"
    return KnowledgeStore(base, {"relations": [
        _relation("adept-banshee", "Adept", "Banshee"),
        _relation("stalker-banshee", "Stalker", "Banshee"),
        unrelated,
    ]})


def _projection():
    return {
        "method": "full_signed_graph",
        "opening_id": "PvT_O01",
        "race": "Protoss",
        "opponent_race": "Terran",
        "nodes": [{
            "node_id": "N001",
            "node_type": "positive",
            "trajectory_action_cues": ["Adept", "Stalker"],
            "own_state": {"representative_unit_cues": []},
            "opponent_state": {"representative_unit_cues": [{"unit": "Banshee"}]},
        }],
    }


def _annotation(claims=None, direction="Use Stalker pressure only while the observation still matches."):
    return {
        "opening": {},
        "nodes": [{
            "node_id": "N001", "node_type": "positive", "title": "Grounded response",
            "trigger_summary": "Enemy Intelligence has remembered Banshee presence.",
            "own_situation": "Stalker is available in the historical response evidence.",
            "opponent_situation": "Banshee presence is partial and may be stale.",
            "decision_direction": direction, "strategic_reason": "Retain the trajectory direction conditionally.",
            "avoid_direction": "Do not overcommit.", "transition_goal": "Reach a stable posture.",
            "trajectory_interpretation": "The human trajectory paired Stalker investment with this context.",
            "applicability_checks": ["Verify live feasibility."], "knowledge_claims": claims or [],
            "failure_mode": "none_observed", "repair_or_recheck_condition": "Recheck on new intelligence.",
        }],
    }


def test_filters_subontology_counter_when_weapon_cannot_hit_target_domain():
    capsule = _store().capsules_for_projection(_projection())["N001"]
    relation_ids = {x["relation_id"] for x in capsule["supported_relations"]}
    assert "adept-banshee" not in relation_ids
    assert "stalker-banshee" in relation_ids
    assert "adept-marine" not in relation_ids
    assert any(x["reason"] == "weapon_target_domain_mismatch" for x in capsule["rejected_relation_examples"])


def test_accepts_exact_supported_relation_claim_and_rejects_hallucinated_claim():
    store = _store()
    projection = _projection()
    capsules = store.capsules_for_projection(projection)
    supported = {"relation_id": "stalker-banshee", "subject": "Stalker", "relation": "counters", "object": "Banshee"}
    assert not store.validate_annotation(_annotation([supported]), projection, capsules)
    unsupported = {"relation_id": "made-up", "subject": "Adept", "relation": "counters", "object": "Banshee"}
    errors = store.validate_annotation(_annotation([unsupported]), projection, capsules)
    assert any("unsupported_knowledge_claim" in error for error in errors)


def test_rejects_concrete_entity_not_in_node_evidence_or_capsule():
    store = _store()
    projection = _projection()
    capsules = store.capsules_for_projection(projection)
    errors = store.validate_annotation(
        _annotation(direction="Switch to Marine production immediately."), projection, capsules
    )
    assert "N001:ungrounded_entity_mention:Marine" in errors


def test_deterministic_sanitize_removes_only_identified_entity_and_relation():
    annotation = _annotation([
        {"relation_id": "made-up", "subject": "Marine", "relation": "counters", "object": "Banshee"}
    ], direction="Research Stimpack, then retain Stalker production.")
    cleaned = _deterministic_knowledge_sanitize(annotation, [
        "N001:ungrounded_entity_mention:Stimpack",
        "N001:unsupported_knowledge_claim:made-up",
    ])
    node = cleaned["nodes"][0]
    assert "Stimpack" not in node["decision_direction"]
    assert "Stalker" in node["decision_direction"]
    assert node["knowledge_claims"] == []


def test_public_node_projection_removes_internal_graph_ids():
    public = _public_node_projection({
        "node_id": "N001", "next_state_id": "OWN_S02", "source_state_id": "OWN_S01",
        "source_state_ids": ["OWN_S01"], "source_edge_ids": ["E1"],
        "own_state": {"state_id": "OWN_S01", "source_state_ids": ["OWN_S01"], "army_domain": "ground"},
        "opponent_state": {"state_id": "OPP_S01", "source_state_ids": ["OPP_S01"], "army_domain": "air"},
    })
    blob = str(public)
    assert "OWN_S" not in blob and "OPP_S" not in blob and "E1" not in blob
    assert public["own_state"]["army_domain"] == "ground"


def test_opening_defaults_fill_missing_fields_without_overwriting_llm_values():
    merged = _merge_opening_defaults(
        {"opening": {"opening_name": "LLM Name"}, "nodes": []},
        {"opening": {"opening_name": "Fallback", "opening_family": "macro", "strategic_goal": "stable"}},
    )
    assert merged["opening"] == {
        "opening_name": "LLM Name", "opening_family": "macro", "strategic_goal": "stable"
    }
