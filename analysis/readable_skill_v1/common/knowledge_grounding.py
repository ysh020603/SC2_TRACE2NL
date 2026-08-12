from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


RELATIONS_ALLOWED_FOR_ANNOTATION = frozenset(
    {"counters", "synergizes_with", "enables_morph", "grants_stat_bonus"}
)


def _normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value or "").lower())


def _fact_ids(relation: dict[str, Any]) -> list[str]:
    ids = {str(f.get("fact_id")) for f in relation.get("fact") or [] if f.get("fact_id")}
    for source in relation.get("source") or []:
        ids.update(str(x) for x in source.get("fact_ids") or [] if x)
    return sorted(ids)


class KnowledgeStore:
    """Curated read-only view over data_sc2_260701.

    The expanded graph is useful but is not trusted blindly. In particular,
    sub-ontology counter expansion is filtered against weapon target domains.
    """

    def __init__(self, base: dict[str, Any], expanded: dict[str, Any]) -> None:
        self.entities: dict[str, dict[str, Any]] = {}
        self.entity_types: dict[str, str] = {}
        self.aliases: dict[str, str] = {}
        for entity_type in ("Unit", "Upgrade", "Ability", "SubOntology"):
            for item in base.get(entity_type) or []:
                name = str(item.get("name") or "")
                if not name:
                    continue
                self.entities[name] = item
                self.entity_types[name] = entity_type
                self.aliases[_normalise(name)] = name

        self.relations: dict[str, dict[str, Any]] = {}
        self.by_subject: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.by_object: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for relation in expanded.get("relations") or []:
            relation_id = str(relation.get("relation_id") or "")
            if not relation_id:
                continue
            self.relations[relation_id] = relation
            self.by_subject[str(relation.get("subject_name") or "")].append(relation)
            self.by_object[str(relation.get("object_name") or "")].append(relation)

    @classmethod
    def load(cls, root: Path) -> "KnowledgeStore":
        root = Path(root)
        base = json.loads((root / "data_base_sc2_260701.json").read_text(encoding="utf-8"))
        expanded = json.loads(
            (root / "relations" / "entity_expanded_relations.json").read_text(encoding="utf-8")
        )
        return cls(base, expanded)

    def canonical(self, value: str) -> str | None:
        return self.aliases.get(_normalise(value))

    def _can_attack(self, attacker: dict[str, Any], target: dict[str, Any]) -> bool:
        if attacker.get("is_structure") and not attacker.get("weapons"):
            return False
        desired = "Air" if target.get("is_flying") else "Ground"
        return any(str(w.get("target_type")) in {"Any", desired} for w in attacker.get("weapons") or [])

    def relation_is_usable(
        self,
        relation: dict[str, Any],
        own_race: str | None = None,
        opponent_race: str | None = None,
    ) -> tuple[bool, str]:
        if relation.get("relation") not in RELATIONS_ALLOWED_FOR_ANNOTATION:
            return False, "relation_not_annotation_safe"
        subject_name = str(relation.get("subject_name") or "")
        object_name = str(relation.get("object_name") or "")
        if subject_name == object_name:
            return False, "self_relation"
        subject = self.entities.get(subject_name) or {}
        obj = self.entities.get(object_name) or {}
        if relation.get("relation") == "counters":
            if self.entity_types.get(subject_name) != "Unit" or self.entity_types.get(object_name) != "Unit":
                return False, "counter_requires_units"
            if own_race and subject.get("race") != own_race:
                return False, "counter_subject_wrong_race"
            if opponent_race and obj.get("race") != opponent_race:
                return False, "counter_object_wrong_race"
            if subject.get("is_structure") or subject.get("is_worker") or obj.get("is_structure") or obj.get("is_worker"):
                return False, "counter_not_combat_composition_relevant"
            if not self._can_attack(subject, obj):
                return False, "weapon_target_domain_mismatch"
            if not _fact_ids(relation):
                return False, "counter_without_evidence"
        if relation.get("relation") == "synergizes_with":
            if self.entity_types.get(subject_name) != "Unit" or self.entity_types.get(object_name) != "Unit":
                return False, "synergy_requires_units"
            if subject.get("is_structure") or subject.get("is_worker") or obj.get("is_structure") or obj.get("is_worker"):
                return False, "synergy_not_combat_composition_relevant"
        return True, ""

    def entity_summary(self, name: str) -> dict[str, Any]:
        item = self.entities[name]
        payload = {
            "name": name,
            "entity_type": self.entity_types[name],
            "race": item.get("race"),
            "attributes": list(item.get("attributes") or []),
            "is_flying": item.get("is_flying"),
            "is_structure": item.get("is_structure"),
            "cost": {
                "minerals": item.get("minerals"),
                "gas": item.get("gas"),
                "supply": item.get("supply"),
            },
            "tech_chain": list(item.get("tech_chain") or [])[:3],
        }
        if self.entity_types[name] == "Upgrade":
            payload["cost"] = item.get("cost")
        if self.entity_types[name] == "Unit":
            payload["weapon_targets"] = sorted(
                {str(w.get("target_type")) for w in item.get("weapons") or [] if w.get("target_type")}
            )
        return payload

    def _canonical_names(self, values: list[Any]) -> list[str]:
        result = []
        for value in values:
            if isinstance(value, dict):
                value = value.get("unit") or value.get("name")
            name = self.canonical(str(value or ""))
            if name and name not in result:
                result.append(name)
        return result

    def _strategy_relevant(self, name: str) -> bool:
        entity_type = self.entity_types.get(name)
        item = self.entities.get(name) or {}
        if entity_type == "Upgrade":
            return True
        if entity_type != "Unit" or item.get("is_worker") or item.get("is_townhall"):
            return False
        if name in {"MULE", "Larva", "Egg", "Cocoon", "Probe", "SCV", "Drone"}:
            return False
        if item.get("is_structure") and (float(item.get("supply") or 0) > 0 or item.get("needs_geyser")):
            return False
        return True

    def _own_mechanic_context(self, race: str | None) -> list[str]:
        result = []
        for name, item in self.entities.items():
            if self.entity_types.get(name) != "Unit" or (race and item.get("race") != race):
                continue
            descriptions = " ".join(str(x) for x in item.get("description") or []).lower()
            is_supply_provider = "supply provider" in descriptions or "provides supply" in descriptions
            if item.get("is_worker") or item.get("is_townhall") or item.get("needs_geyser") or is_supply_provider:
                result.append(name)
        return sorted(result)

    def _tech_chain_context(self, names: list[str], race: str | None) -> list[str]:
        result = []
        for seed in names:
            for chain in (self.entities.get(seed) or {}).get("tech_chain") or []:
                for candidate, item in self.entities.items():
                    if self.entity_types.get(candidate) not in {"Unit", "Upgrade"}:
                        continue
                    if race and item.get("race") not in {None, race}:
                        continue
                    if re.search(rf"(?<![A-Za-z0-9]){re.escape(candidate)}(?![A-Za-z0-9])", str(chain)) and candidate not in result:
                        result.append(candidate)
        return result

    def capsule_for_node(self, projection: dict[str, Any], node: dict[str, Any]) -> dict[str, Any]:
        own_race, opponent_race = projection.get("race"), projection.get("opponent_race")
        own_cues = self._canonical_names(
            list(((node.get("own_state") or {}).get("representative_unit_cues") or []))
            + list(node.get("trajectory_action_cues") or [])
        )
        opponent_cues = self._canonical_names(
            list(((node.get("opponent_state") or {}).get("representative_unit_cues") or []))
        )
        own_cues = [
            n for n in own_cues
            if self._strategy_relevant(n) and (not own_race or self.entities[n].get("race") in {None, own_race})
        ]
        opponent_cues = [
            n for n in opponent_cues if not opponent_race or self.entities[n].get("race") in {None, opponent_race}
        ]
        seed_names = set(own_cues + opponent_cues)
        supported, rejected = [], []
        seen = set()
        for name in sorted(seed_names):
            for relation in self.by_subject.get(name, []) + self.by_object.get(name, []):
                relation_id = str(relation.get("relation_id"))
                if relation_id in seen:
                    continue
                # Only retain relations tied to the human response or observed opponent cue.
                subject, obj = relation.get("subject_name"), relation.get("object_name")
                if relation.get("relation") == "counters":
                    cross_side = (
                        (subject in own_cues and obj in opponent_cues)
                        or (subject in opponent_cues and obj in own_cues)
                    )
                    if not cross_side:
                        continue
                elif not (subject in own_cues and obj in own_cues):
                    continue
                usable, reason = self.relation_is_usable(relation, own_race if subject in own_cues else None, opponent_race if obj in opponent_cues else None)
                if not usable:
                    if reason == "weapon_target_domain_mismatch" and (subject in seed_names or obj in seed_names):
                        rejected.append({"relation_id": relation_id, "reason": reason})
                    continue
                seen.add(relation_id)
                supported.append(
                    {
                        "relation_id": relation_id,
                        "subject": subject,
                        "relation": relation.get("relation"),
                        "object": obj,
                        "description": list(relation.get("description") or [])[:2],
                        "fact_ids": _fact_ids(relation),
                    }
                )

        mechanic_context = self._own_mechanic_context(own_race)
        prerequisite_context = self._tech_chain_context(own_cues, own_race)
        allowed_mentions = set(seed_names).union(mechanic_context, prerequisite_context)
        for relation in supported:
            allowed_mentions.update((relation["subject"], relation["object"]))
        entities = {name: self.entity_summary(name) for name in sorted(allowed_mentions) if name in self.entities}
        supported_mechanics = []
        for name, entity in entities.items():
            for index, chain in enumerate(entity.get("tech_chain") or []):
                supported_mechanics.append({
                    "relation_id": f"entity:{name}:tech_chain:{index}",
                    "subject": name,
                    "relation": "tech_chain",
                    "object": chain,
                    "source": "structured_database",
                })
            if entity.get("cost"):
                supported_mechanics.append({
                    "relation_id": f"entity:{name}:cost",
                    "subject": name,
                    "relation": "cost",
                    "object": entity.get("cost"),
                    "source": "structured_database",
                })
        relation_priority = {"counters": 0, "enables_morph": 1, "grants_stat_bonus": 2, "synergizes_with": 3}
        supported.sort(key=lambda r: (relation_priority.get(str(r.get("relation")), 9), str(r.get("subject")), str(r.get("object"))))
        return {
            "node_id": node.get("node_id"),
            "trajectory_entities": own_cues,
            "observed_enemy_entities": opponent_cues,
            "entities": entities,
            "supported_relations": supported[:12],
            "supported_mechanics": supported_mechanics[:36],
            "allowed_entity_mentions": sorted(allowed_mentions),
            "mechanic_context_entities": mechanic_context,
            "prerequisite_context_entities": prerequisite_context,
            "rejected_relation_count": len(rejected),
            "rejected_relation_examples": rejected[:8],
            "usage_rule": (
                "Human-trajectory signs and directions remain primary. Use these facts only to interpret, constrain, "
                "or qualify that evidence; never invent a preferred/harmful sign from the knowledge base."
            ),
        }

    def capsules_for_projection(self, projection: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return {
            str(node.get("node_id")): self.capsule_for_node(projection, node)
            for node in projection.get("nodes") or []
        }

    def validate_annotation(
        self,
        annotation: dict[str, Any],
        projection: dict[str, Any],
        capsules: dict[str, dict[str, Any]],
    ) -> list[str]:
        errors: list[str] = []
        expected = {str(n.get("node_id")): str(n.get("node_type")) for n in projection.get("nodes") or []}
        actual_nodes = {
            str(n.get("node_id")): n for n in annotation.get("nodes") or [] if isinstance(n, dict)
        }
        if set(actual_nodes) != set(expected):
            errors.append("node_id_set_mismatch")
            return errors
        for node_id, node_type in expected.items():
            node = actual_nodes[node_id]
            if str(node.get("node_type")) != node_type:
                errors.append(f"{node_id}:node_type_changed")
            for field in (
                "trajectory_interpretation",
                "applicability_checks",
                "knowledge_claims",
                "failure_mode",
                "repair_or_recheck_condition",
            ):
                if field not in node:
                    errors.append(f"{node_id}:missing_{field}")
            if not isinstance(node.get("applicability_checks"), list):
                errors.append(f"{node_id}:applicability_checks_not_list")
            if not isinstance(node.get("knowledge_claims"), list):
                errors.append(f"{node_id}:knowledge_claims_not_list")
                continue
            capsule = capsules.get(node_id) or {}
            supported = [
                (str(r.get("relation_id")), r.get("subject"), r.get("relation"), r.get("object"))
                for r in (capsule.get("supported_relations") or []) + (capsule.get("supported_mechanics") or [])
            ]
            normalised_supported = {
                (a, b, c, json.dumps(d, sort_keys=True) if isinstance(d, dict) else d)
                for a, b, c, d in supported
            }
            for claim in node.get("knowledge_claims") or []:
                claim_object = claim.get("object")
                key = (
                    str(claim.get("relation_id")),
                    claim.get("subject"),
                    claim.get("relation"),
                    json.dumps(claim_object, sort_keys=True) if isinstance(claim_object, dict) else claim_object,
                )
                if key not in normalised_supported:
                    errors.append(f"{node_id}:unsupported_knowledge_claim:{key[0]}")
            blob = " ".join(str(node.get(k) or "") for k in (
                "title", "trigger_summary", "own_situation", "opponent_situation", "decision_direction",
                "strategic_reason", "avoid_direction", "transition_goal", "trajectory_interpretation",
                "repair_or_recheck_condition",
            ))
            blob += " " + " ".join(str(x) for x in node.get("applicability_checks") or [])
            allowed = set(capsule.get("allowed_entity_mentions") or [])
            for canonical in self.entities:
                if self.entity_types.get(canonical) not in {"Unit", "Upgrade"}:
                    continue
                if canonical in allowed or len(canonical) < 4:
                    continue
                if re.search(rf"(?<![A-Za-z0-9]){re.escape(canonical)}s?(?![A-Za-z0-9])", blob, re.I):
                    errors.append(f"{node_id}:ungrounded_entity_mention:{canonical}")
            lower = blob.lower()
            if any(term in lower for term in (" counter ", "counters", "strong against", "weak against")):
                if not any(c.get("relation") == "counters" for c in node.get("knowledge_claims") or []):
                    errors.append(f"{node_id}:counter_language_without_claim")
            if node_type == "negative" and str(node.get("failure_mode") or "").strip().lower() in {"", "none", "unknown"}:
                errors.append(f"{node_id}:negative_without_failure_mode")
        return sorted(set(errors))
