"""Taxonomy re-exports and skill_mining_v2 extensions."""

from __future__ import annotations

from typing import Any

from analysis.skill_mining_v2.config import MACRO_EVENTS

WORKERS = {"SCV", "Probe", "Drone", "MULE"}
SUPPLY = {"SupplyDepot", "Pylon", "Overlord", "SupplyDepotLowered"}
GAS = {"Refinery", "Assimilator", "Extractor"}
BASES = {
    "CommandCenter", "OrbitalCommand", "PlanetaryFortress", "Nexus",
    "Hatchery", "Lair", "Hive",
}
STATIC_DEFENSE = {
    "Bunker", "MissileTurret", "PhotonCannon", "SpineCrawler",
    "SporeCrawler", "ShieldBattery",
}
PROD_BUILDINGS = {
    "Barracks", "Factory", "Starport", "Gateway", "WarpGate",
    "RoboticsFacility", "Stargate", "SpawningPool", "RoachWarren",
    "BanelingNest", "HydraliskDen", "Spire", "UltraliskCavern",
    "InfestationPit", "NydusNetwork", "LurkerDen", "LurkerDenMP",
}
TECH_BUILDINGS = {
    "EngineeringBay", "Armory", "GhostAcademy", "FusionCore", "TechLab",
    "BarracksTechLab", "FactoryTechLab", "StarportTechLab", "Reactor",
    "BarracksReactor", "FactoryReactor", "StarportReactor",
    "CyberneticsCore", "TwilightCouncil", "TemplarArchives", "DarkShrine",
    "RoboticsBay", "FleetBeacon", "Forge", "EvolutionChamber", "GreaterSpire",
}
COMBAT_FAMILY = {
    "Marine": "bio", "Marauder": "bio", "Reaper": "bio", "Ghost": "bio",
    "Medivac": "bio_support", "Hellion": "factory", "Hellbat": "factory",
    "WidowMine": "factory", "SiegeTank": "factory", "Cyclone": "factory",
    "Thor": "factory", "Viking": "air", "VikingFighter": "air",
    "Liberator": "air", "Banshee": "air", "Raven": "air",
    "Battlecruiser": "air", "Zealot": "gateway", "Stalker": "gateway",
    "Sentry": "gateway", "Adepts": "gateway", "Adept": "gateway",
    "HighTemplar": "gateway", "DarkTemplar": "gateway", "Archon": "gateway",
    "Immortal": "robotics", "Colossus": "robotics", "Disruptor": "robotics",
    "Observer": "robotics", "WarpPrism": "robotics", "Phoenix": "stargate",
    "Oracle": "stargate", "VoidRay": "stargate", "Tempest": "stargate",
    "Carrier": "stargate", "Mothership": "stargate",
    "MothershipCore": "stargate", "Zergling": "ling_bane",
    "Baneling": "ling_bane", "Roach": "roach", "Ravager": "roach",
    "Hydralisk": "hydra", "Lurker": "hydra", "LurkerMP": "hydra",
    "Mutalisk": "air", "Corruptor": "air", "BroodLord": "air",
    "Infestor": "tech_unit", "Viper": "tech_unit", "SwarmHost": "tech_unit",
    "Ultralisk": "ultra", "Queen": "queen", "OverlordTransport": "support",
    "Overseer": "support", "NydusWorm": "support",
}
BASE_UPGRADES = {"OrbitalCommand", "PlanetaryFortress", "Lair", "Hive", "WarpGate"}
RACE_ALIASES = {
    "terran": "Terran", "protoss": "Protoss", "zerg": "Zerg",
    "терраны": "Terran", "протоссы": "Protoss", "зерги": "Zerg",
}


def normalize_race(race: Any) -> str | None:
    if race is None:
        return None
    text = str(race).strip()
    return text if text in {"Terran", "Protoss", "Zerg"} else RACE_ALIASES.get(text.lower())


def result_name(ev: dict[str, Any]) -> str:
    return str(ev.get("standard_result_name") or ev.get("name") or "Unknown")


def macro_category(ev: dict[str, Any]) -> str:
    name, event = result_name(ev), ev.get("event")
    if name in WORKERS:
        return "economy_worker"
    if name in SUPPLY:
        return "supply"
    if name in GAS:
        return "economy_gas"
    if name in BASES or name in BASE_UPGRADES:
        return "economy_base_upgrade" if name in BASE_UPGRADES or event == "tech_morph" else "economy_base"
    if name in STATIC_DEFENSE:
        return "static_defense"
    if name in PROD_BUILDINGS:
        return "production_building"
    if name in TECH_BUILDINGS:
        return "tech_building"
    if event == "upgrade_research":
        return "upgrade"
    if name in COMBAT_FAMILY:
        return f"combat_{COMBAT_FAMILY[name]}"
    if event == "production":
        return "combat_other"
    if event == "construction":
        return "construction_other"
    if event == "tech_morph":
        return "tech_morph_other"
    return "other"


def key_token(ev: dict[str, Any], occurrence: int | None = None) -> str | None:
    name, category = result_name(ev), macro_category(ev)
    if category in {"economy_worker", "supply"} or name == "CreepTumor":
        return None
    if category.startswith("combat_"):
        token = f"Combat_{category.split('_', 1)[1]}"
    elif category == "economy_gas":
        token = "Gas"
    elif category == "economy_base":
        token = "Base"
    elif category == "economy_base_upgrade":
        token = f"BaseUpgrade_{name}"
    elif category == "static_defense":
        token = f"Static_{name}"
    elif category == "production_building":
        token = f"Prod_{name}"
    elif category == "tech_building":
        token = f"Tech_{name}"
    elif category == "upgrade":
        token = f"Upgrade_{name}"
    else:
        token = name
    if occurrence and occurrence > 1 and category in {
        "economy_gas", "economy_base", "production_building", "static_defense",
    }:
        token = f"{token}{occurrence}"
    return token


def build_key_sequence(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    sequence: list[dict[str, Any]] = []
    previous = None
    streak = 0
    for ev in events:
        if key_token(ev) is None:
            continue
        name, category = result_name(ev), macro_category(ev)
        key = name if category != "upgrade" else f"up:{name}"
        counts[key] = counts.get(key, 0) + 1
        occurrence = counts[key] if category in {
            "economy_gas", "economy_base", "production_building", "static_defense",
        } else None
        token = key_token(ev, occurrence)
        if token == previous and token and token.startswith("Combat_"):
            streak += 1
            sequence[-1]["count"] = streak
            sequence[-1]["token"] = f"{token}x{streak}"
            continue
        streak, previous = 1, token
        sequence.append({
            "token": token, "count": 1, "second": ev.get("second"),
            "name": name, "category": category,
        })
    return sequence

__all__ = [
    "AIR_UNITS",
    "BASES",
    "BASE_UPGRADES",
    "COMBAT_FAMILY",
    "GAS",
    "GROUND_COMBAT",
    "PROD_BUILDINGS",
    "STATIC_DEFENSE",
    "SUPPLY",
    "TECH_BUILDINGS",
    "WORKERS",
    "build_key_sequence",
    "investment_buckets",
    "is_macro_event",
    "key_token",
    "macro_category",
    "normalize_race",
    "result_name",
]

# Air combat units (subset of COMBAT_FAMILY with air tag)
AIR_UNITS = frozenset(
    name for name, fam in COMBAT_FAMILY.items() if fam in {"air", "stargate", "bio_support"}
)

# Ground combat units (excluding support queens etc.)
GROUND_COMBAT = frozenset(
    name
    for name, fam in COMBAT_FAMILY.items()
    if fam not in {"air", "stargate", "bio_support", "support", "queen"}
)


def is_macro_event(ev: dict[str, Any]) -> bool:
    return ev.get("event") in MACRO_EVENTS


def investment_buckets(name: str | None = None, event: str | None = None) -> str:
    """Map entity/event to coarse investment bucket for response analysis."""
    if event == "upgrade_research":
        return "upgrade"
    if name is None:
        return "other"
    if name in WORKERS or name == "MULE":
        return "economy"
    if name in GAS:
        return "economy"
    if name in BASES or name in BASE_UPGRADES:
        return "expansion"
    if name in PROD_BUILDINGS:
        return "production"
    if name in TECH_BUILDINGS:
        return "technology"
    if name in STATIC_DEFENSE:
        return "defense"
    if name in AIR_UNITS:
        return "air"
    if name in GROUND_COMBAT:
        return "ground"
    if name in COMBAT_FAMILY:
        fam = COMBAT_FAMILY[name]
        if fam in {"air", "stargate"}:
            return "air"
        return "ground"
    if event == "production":
        return "ground"
    if event in {"construction", "tech_morph"}:
        return "technology"
    return "other"


def investment_bucket(ev: dict[str, Any]) -> str:
    """Bucket from a compact build-order event."""
    return investment_buckets(result_name(ev), ev.get("event"))


def action_name(ev: dict[str, Any]) -> str:
    return str(ev.get("name") or ev.get("standard_result_name") or "Unknown")


# allow investment_bucket(name, event) as well as investment_bucket(ev)
_investment_bucket_ev = investment_bucket


def investment_bucket(arg=None, event=None):  # type: ignore[misc]
    if isinstance(arg, dict):
        return _investment_bucket_ev(arg)
    return investment_buckets(arg, event)
