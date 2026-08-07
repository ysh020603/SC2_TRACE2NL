"""Macro-event taxonomy for opening analysis (plan.md §5)."""

from __future__ import annotations

from typing import Any

WORKERS = {"SCV", "Probe", "Drone", "MULE"}
SUPPLY = {"SupplyDepot", "Pylon", "Overlord", "SupplyDepotLowered"}
GAS = {"Refinery", "Assimilator", "Extractor"}
BASES = {
    "CommandCenter",
    "OrbitalCommand",
    "PlanetaryFortress",
    "Nexus",
    "Hatchery",
    "Lair",
    "Hive",
}
STATIC_DEFENSE = {
    "Bunker",
    "MissileTurret",
    "PhotonCannon",
    "SpineCrawler",
    "SporeCrawler",
    "ShieldBattery",
}

PROD_BUILDINGS = {
    "Barracks",
    "Factory",
    "Starport",
    "Gateway",
    "WarpGate",
    "RoboticsFacility",
    "Stargate",
    "SpawningPool",
    "RoachWarren",
    "BanelingNest",
    "HydraliskDen",
    "Spire",
    "UltraliskCavern",
    "InfestationPit",
    "NydusNetwork",
    "LurkerDen",
    "LurkerDenMP",
}

TECH_BUILDINGS = {
    "EngineeringBay",
    "Armory",
    "GhostAcademy",
    "FusionCore",
    "TechLab",
    "BarracksTechLab",
    "FactoryTechLab",
    "StarportTechLab",
    "Reactor",
    "BarracksReactor",
    "FactoryReactor",
    "StarportReactor",
    "CyberneticsCore",
    "TwilightCouncil",
    "TemplarArchives",
    "DarkShrine",
    "RoboticsBay",
    "FleetBeacon",
    "Forge",
    "EvolutionChamber",
    "GreaterSpire",
}

COMBAT_FAMILY = {
    # Terran
    "Marine": "bio",
    "Marauder": "bio",
    "Reaper": "bio",
    "Ghost": "bio",
    "Medivac": "bio_support",
    "Hellion": "factory",
    "Hellbat": "factory",
    "WidowMine": "factory",
    "SiegeTank": "factory",
    "Cyclone": "factory",
    "Thor": "factory",
    "Viking": "air",
    "VikingFighter": "air",
    "Liberator": "air",
    "Banshee": "air",
    "Raven": "air",
    "Battlecruiser": "air",
    # Protoss
    "Zealot": "gateway",
    "Stalker": "gateway",
    "Sentry": "gateway",
    "Adepts": "gateway",
    "Adept": "gateway",
    "HighTemplar": "gateway",
    "DarkTemplar": "gateway",
    "Archon": "gateway",
    "Immortal": "robotics",
    "Colossus": "robotics",
    "Disruptor": "robotics",
    "Observer": "robotics",
    "WarpPrism": "robotics",
    "Phoenix": "stargate",
    "Oracle": "stargate",
    "VoidRay": "stargate",
    "Tempest": "stargate",
    "Carrier": "stargate",
    "Mothership": "stargate",
    "MothershipCore": "stargate",
    # Zerg
    "Zergling": "ling_bane",
    "Baneling": "ling_bane",
    "Roach": "roach",
    "Ravager": "roach",
    "Hydralisk": "hydra",
    "Lurker": "hydra",
    "LurkerMP": "hydra",
    "Mutalisk": "air",
    "Corruptor": "air",
    "BroodLord": "air",
    "Infestor": "tech_unit",
    "Viper": "tech_unit",
    "SwarmHost": "tech_unit",
    "Ultralisk": "ultra",
    "Queen": "queen",
    "OverlordTransport": "support",
    "Overseer": "support",
    "NydusWorm": "support",
}

BASE_UPGRADES = {"OrbitalCommand", "PlanetaryFortress", "Lair", "Hive", "WarpGate"}

RACE_ALIASES = {
    "terran": "Terran",
    "protoss": "Protoss",
    "zerg": "Zerg",
    "терраны": "Terran",
    "протоссы": "Protoss",
    "зерги": "Zerg",
}


def normalize_race(race: Any) -> str | None:
    if race is None:
        return None
    text = str(race).strip()
    if text in {"Terran", "Protoss", "Zerg"}:
        return text
    return RACE_ALIASES.get(text.lower())


def result_name(ev: dict[str, Any]) -> str:
    return str(ev.get("standard_result_name") or ev.get("name") or "Unknown")


def macro_category(ev: dict[str, Any]) -> str:
    name = result_name(ev)
    event = ev.get("event")
    if name in WORKERS or (event == "production" and name in WORKERS):
        return "economy_worker"
    if name in SUPPLY:
        return "supply"
    if name in GAS:
        return "economy_gas"
    if name in BASES or name in BASE_UPGRADES:
        if name in BASE_UPGRADES or event == "tech_morph":
            return "economy_base_upgrade"
        return "economy_base"
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
    """Token for key strategic sequence; workers/supply compressed away."""
    name = result_name(ev)
    cat = macro_category(ev)
    if cat in {"economy_worker", "supply"}:
        return None
    if name == "CreepTumor":
        return None
    if cat.startswith("combat_"):
        fam = cat.split("_", 1)[1]
        token = f"Combat_{fam}"
    elif cat == "economy_gas":
        token = "Gas"
    elif cat == "economy_base":
        token = "Base"
    elif cat == "economy_base_upgrade":
        token = f"BaseUpgrade_{name}"
    elif cat == "static_defense":
        token = f"Static_{name}"
    elif cat == "production_building":
        token = f"Prod_{name}"
    elif cat == "tech_building":
        token = f"Tech_{name}"
    elif cat == "upgrade":
        token = f"Upgrade_{name}"
    else:
        token = name
    if occurrence is not None and occurrence > 1 and cat in {
        "economy_gas",
        "economy_base",
        "production_building",
        "static_defense",
    }:
        return f"{token}{occurrence}"
    return token


def build_key_sequence(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    seq: list[dict[str, Any]] = []
    prev_token = None
    streak = 0
    for ev in events:
        base = key_token(ev)
        if base is None:
            continue
        # occurrence for compressible classes
        name = result_name(ev)
        cat = macro_category(ev)
        key = name if cat != "upgrade" else f"up:{name}"
        counts[key] = counts.get(key, 0) + 1
        token = key_token(ev, counts[key] if cat in {
            "economy_gas",
            "economy_base",
            "production_building",
            "static_defense",
        } else None)
        if token is None:
            continue
        # compress consecutive identical combat tokens
        if token == prev_token and token.startswith("Combat_"):
            streak += 1
            seq[-1]["count"] = streak
            seq[-1]["token"] = f"{token}x{streak}"
            continue
        streak = 1
        prev_token = token
        seq.append(
            {
                "token": token,
                "count": 1,
                "second": ev.get("second"),
                "name": name,
                "category": cat,
            }
        )
    return seq
