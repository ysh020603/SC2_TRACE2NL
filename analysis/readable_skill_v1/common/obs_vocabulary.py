from __future__ import annotations

import re
from pathlib import Path

from .io import read_json

WORKERS = {"Probe", "SCV", "Drone", "MULE"}
SUPPLY = {"Pylon", "SupplyDepot", "Overlord"}
BASES = {"Nexus", "CommandCenter", "OrbitalCommand", "PlanetaryFortress", "Hatchery", "Lair", "Hive"}


def load_vocabulary(entity_path: Path) -> dict[str, dict]:
    data = read_json(entity_path)
    result = {}
    for section in ("units", "upgrades"):
        for name, info in (data.get(section) or {}).items():
            result[name] = dict(info, section=section)
    return result


def split_names(value: object, vocabulary: dict[str, dict]) -> list[str]:
    if not value:
        return []
    text = str(value)
    found = []
    for name in vocabulary:
        if re.search(rf"(?<![A-Za-z0-9]){re.escape(name)}(?![A-Za-z0-9])", text, re.I):
            found.append(name)
    return found


def combat_cues(names: list[str], vocabulary: dict[str, dict], race: str, limit: int = 4) -> list[str]:
    cues = []
    for name in names:
        info = vocabulary.get(name) or {}
        attrs = set(info.get("attributes") or [])
        if info.get("race") != race or name in WORKERS | SUPPLY | BASES or "Structure" in attrs or info.get("section") == "upgrades":
            continue
        if name not in cues:
            cues.append(name)
    return cues[:limit]
