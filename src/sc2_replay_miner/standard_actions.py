"""Map sc2reader ability names to canonical Ability names in the SC2 data graph."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path

from sc2_replay_miner.action_models import MacroActionCategory

DEFAULT_DATABASE = (
    Path(__file__).resolve().parents[2]
    / "data_sc2_260701"
    / "data_base_sc2_260701.json"
)

# sc2reader uses friendly replay names; the structured database uses python-sc2
# Ability names. These aliases cover semantic renames that string normalization
# cannot recover.
DIRECT_ALIASES = {
    "ArchonWarpSelection": "MORPH_ARCHON",
    "CalldownMULE": "CALLDOWNMULE_CALLDOWNMULE",
    "EvolveAdrenalGlands": "RESEARCH_ZERGLINGADRENALGLANDS",
    "EvolveCentrifugalHooks": "RESEARCH_CENTRIFUGALHOOKS",
    "EvolveChitinousPlating": "RESEARCH_CHITINOUSPLATING",
    "EvolveGlialReconstitution": "RESEARCH_GLIALREGENERATION",
    "EvolveMetabolicBoost": "RESEARCH_ZERGLINGMETABOLICBOOST",
    "EvolveNeuralParasite": "RESEARCH_NEURALPARASITE",
    "EvolveTunnelingClaws": "RESEARCH_TUNNELINGCLAWS",
    "MorphSwarmHost": "TRAIN_SWARMHOST",
    "ResearchAdeptPiercingAttack": "RESEARCH_ADEPTRESONATINGGLAIVES",
    "ResearchAnionPulseCrystals": "RESEARCH_PHOENIXANIONPULSECRYSTALS",
    "ResearchBansheeSpeed": "RESEARCH_BANSHEEHYPERFLIGHTROTORS",
    "ResearchCloakingField": "RESEARCH_BANSHEECLOAKINGFIELD",
    "ResearchCorvidReactor": "RESEARCH_RAVENCORVIDREACTOR",
    "ResearchDarkTemplarBlinkUpgrade": "RESEARCH_SHADOWSTRIKE",
    "ResearchEvolveGroovedSpines": "RESEARCH_GROOVEDSPINES",
    "ResearchEvolveMuscularAugments": "RESEARCH_MUSCULARAUGMENTS",
    "ResearchGraviticBoosters": "RESEARCH_GRAVITICBOOSTER",
    "ResearchLiberatorAGRangeUpgrade": "FUSIONCORERESEARCH_RESEARCHBALLISTICRANGE",
    "ResearchMedivacIncreaseSpeedBoost": (
        "FUSIONCORERESEARCH_RESEARCHRAPIDREIGNITIONSYSTEM"
    ),
    "ResearchPsiStormTech": "RESEARCH_PSISTORM",
    "ResearchWeaponRefit": "RESEARCH_BATTLECRUISERWEAPONREFIT",
    "Researchoverlordspeed": "RESEARCH_PNEUMATIZEDCARAPACE",
    "TransformToWarpGate": "MORPH_WARPGATE",
    "UpgradeStructureArmor": "RESEARCH_TERRANSTRUCTUREARMORUPGRADE",
}

LEVEL_PATTERNS = (
    (
        re.compile(r"^UpgradeGroundWeapons([123])$"),
        "FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL{}",
    ),
    (
        re.compile(r"^UpgradeGroundArmor([123])$"),
        "FORGERESEARCH_PROTOSSGROUNDARMORLEVEL{}",
    ),
    (
        re.compile(r"^UpgradeAirWeapons([123])$"),
        "CYBERNETICSCORERESEARCH_PROTOSSAIRWEAPONSLEVEL{}",
    ),
    (
        re.compile(r"^UpgradeAirArmor([123])$"),
        "CYBERNETICSCORERESEARCH_PROTOSSAIRARMORLEVEL{}",
    ),
    (
        re.compile(r"^Upgrades?Shields([123])$"),
        "FORGERESEARCH_PROTOSSSHIELDSLEVEL{}",
    ),
    (
        re.compile(r"^UpgradeTerranInfantryWeapons([123])$"),
        "ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL{}",
    ),
    (
        re.compile(r"^UpgradeTerranInfantryArmor([123])$"),
        "ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL{}",
    ),
    (
        re.compile(r"^UpgradeVehicleWeapons([123])$"),
        "ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL{}",
    ),
    (
        re.compile(r"^UpgradeShipWeapons([123])$"),
        "ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL{}",
    ),
    (
        re.compile(r"^ResearchTerranVehicleAndShipArmorsLevel([123])$"),
        "ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL{}",
    ),
    (
        re.compile(r"^EvolveFlyerAttacks([123])$"),
        "RESEARCH_ZERGFLYERATTACKLEVEL{}",
    ),
    (
        re.compile(r"^EvolveFlyerCarapace([123])$"),
        "RESEARCH_ZERGFLYERARMORLEVEL{}",
    ),
)


@dataclass(frozen=True)
class StandardAbility:
    name: str
    result_name: str | None
    result_type: str | None


@dataclass(frozen=True)
class StandardActionMatch:
    name: str | None
    result_name: str | None
    result_type: str | None
    status: str
    confidence: float


def _normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


@lru_cache(maxsize=4)
def _load_abilities(database_path: str) -> tuple[StandardAbility, ...]:
    data = json.loads(Path(database_path).read_text(encoding="utf-8"))
    abilities: list[StandardAbility] = []
    for item in data.get("Ability", []):
        results = [
            relation
            for relation in item.get("relations", [])
            if relation.get("relation") == "action_result"
        ]
        if results:
            for result in results:
                abilities.append(
                    StandardAbility(
                        name=str(item["name"]),
                        result_name=str(result.get("object_name") or "") or None,
                        result_type=str(result.get("object_type") or "") or None,
                    )
                )
        else:
            abilities.append(
                StandardAbility(
                    name=str(item["name"]),
                    result_name=None,
                    result_type=None,
                )
            )
    return tuple(abilities)


class StandardActionMapper:
    """Resolve replay-friendly abilities to canonical data-graph Action names."""

    def __init__(self, database_path: str | Path = DEFAULT_DATABASE) -> None:
        self.database_path = Path(database_path)
        if not self.database_path.is_file():
            raise FileNotFoundError(f"Standard action database not found: {self.database_path}")
        self.abilities = _load_abilities(str(self.database_path.resolve()))
        self.by_name = {ability.name: ability for ability in self.abilities}
        self._cache: dict[
            tuple[str, str, MacroActionCategory], StandardActionMatch
        ] = {}

    def resolve(
        self,
        ability_name: str,
        target_name: str,
        category: MacroActionCategory,
    ) -> StandardActionMatch:
        key = (ability_name, target_name, category)
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        alias = self._explicit_name(ability_name)
        if alias is not None and alias in self.by_name:
            match = self._as_match(self.by_name[alias], "explicit", 1.0)
            self._cache[key] = match
            return match

        match = self._rank_candidates(ability_name, target_name, category)
        self._cache[key] = match
        return match

    @staticmethod
    def _explicit_name(ability_name: str) -> str | None:
        direct = DIRECT_ALIASES.get(ability_name)
        if direct is not None:
            return direct
        for pattern, template in LEVEL_PATTERNS:
            found = pattern.match(ability_name)
            if found:
                return template.format(found.group(1))
        return None

    @staticmethod
    def _as_match(
        ability: StandardAbility,
        status: str,
        confidence: float,
    ) -> StandardActionMatch:
        return StandardActionMatch(
            name=ability.name,
            result_name=ability.result_name,
            result_type=ability.result_type,
            status=status,
            confidence=confidence,
        )

    def _rank_candidates(
        self,
        ability_name: str,
        target_name: str,
        category: MacroActionCategory,
    ) -> StandardActionMatch:
        expected_type = "Upgrade" if category == "upgrade_research" else "Unit"
        target_norm = _normalized(target_name)
        result_aliases = {target_norm}
        if target_norm == "swarmhost":
            result_aliases.add("swarmhostmp")

        result_candidates = [
            ability
            for ability in self.abilities
            if ability.result_type == expected_type
            and _normalized(ability.result_name or "") in result_aliases
        ]
        if result_candidates:
            candidates = result_candidates
        elif category == "upgrade_research":
            candidates = [
                ability
                for ability in self.abilities
                if "RESEARCH" in ability.name
            ]
        else:
            candidates = list(self.abilities)
        scored = [
            (
                self._score(ability_name, category, candidate, bool(result_candidates)),
                candidate,
            )
            for candidate in candidates
        ]
        score, best = max(scored, key=lambda item: (item[0], item[1].name))
        threshold = 0.7 if result_candidates else 0.82
        if score < threshold:
            return StandardActionMatch(
                name=None,
                result_name=None,
                result_type=None,
                status="unmapped",
                confidence=round(score, 4),
            )
        status = "result_and_semantic" if result_candidates else "semantic_fuzzy"
        return self._as_match(best, status, round(min(score, 1.0), 4))

    @staticmethod
    def _score(
        raw_name: str,
        category: MacroActionCategory,
        candidate: StandardAbility,
        result_matched: bool,
    ) -> float:
        raw = _normalized(raw_name)
        standard = _normalized(candidate.name)
        score = SequenceMatcher(None, raw, standard).ratio()
        if raw in standard or standard in raw:
            score = max(score, 0.88)
        if result_matched:
            score += 0.35

        if category == "construction":
            if "build" in standard:
                score += 0.2
            if any(token in standard for token in ("land", "root", "raise")):
                score -= 0.25
        elif category == "production":
            if raw_name.startswith("WarpIn"):
                if "warpgatetrain" in standard or "trainwarp" in standard:
                    score += 0.28
            elif raw_name.startswith("Train"):
                if "train" in standard:
                    score += 0.18
                if "warpgatetrain" in standard:
                    score -= 0.08
            elif raw_name.startswith("MorphTo"):
                if "morph" in standard or "upgradeto" in standard:
                    score += 0.22
            elif raw_name.startswith("Morph"):
                if "larvatrain" in standard or standard.startswith("train"):
                    score += 0.2
                if "burrowup" in standard:
                    score -= 0.2
            elif raw_name.startswith("Build") and "train" in standard:
                score += 0.18
        elif category == "tech_morph":
            if "morph" in standard or "upgradeto" in standard:
                score += 0.22
            if "land" in standard:
                score -= 0.25
        elif category == "upgrade_research" and "research" in standard:
            score += 0.22

        return score
