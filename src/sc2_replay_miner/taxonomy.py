"""Config-driven unit/building taxonomy and morph filtering."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml

Kind = Literal[
    "building",
    "worker",
    "basic_army",
    "key_unit",
    "ignored",
    "unknown",
]


class Taxonomy:
    def __init__(self, config_dir: str | Path):
        self.config_dir = Path(config_dir)
        self._name_to_kind: dict[str, Kind] = {}
        self._basic_army: set[str] = set()
        self._key_units: set[str] = set()
        self._workers: set[str] = set()
        self._buildings: set[str] = set()
        self._ignored: set[str] = set()
        self._tech_morphs: dict[str, set[str]] = {}
        self._ignored_morph_names: set[str] = set()
        self.unknown_names: set[str] = set()
        self._load()

    def _load_yaml(self, path: Path) -> dict[str, Any]:
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        if not isinstance(data, dict):
            raise TypeError(f"Expected mapping in {path}")
        return data

    def _register(self, names: list[str] | None, kind: Kind) -> None:
        for name in names or []:
            self._name_to_kind[str(name)] = kind
            if kind == "building":
                self._buildings.add(name)
            elif kind == "worker":
                self._workers.add(name)
            elif kind == "basic_army":
                self._basic_army.add(name)
            elif kind == "key_unit":
                self._key_units.add(name)
            elif kind == "ignored":
                self._ignored.add(name)

    def _load(self) -> None:
        for race_file in ("units_terran.yaml", "units_protoss.yaml", "units_zerg.yaml"):
            path = self.config_dir / race_file
            if not path.exists():
                continue
            data = self._load_yaml(path)
            self._register(data.get("buildings"), "building")
            self._register(data.get("workers"), "worker")
            self._register(data.get("basic_army"), "basic_army")
            self._register(data.get("key_units"), "key_unit")
            self._register(data.get("ignored"), "ignored")

        morph_path = self.config_dir / "morph_whitelist.yaml"
        if morph_path.exists():
            morph = self._load_yaml(morph_path)
            tech = morph.get("tech_morphs") or {}
            for src, destinations in tech.items():
                self._tech_morphs[str(src)] = {str(x) for x in (destinations or [])}
            ignored = morph.get("ignored_morphs") or []
            self._ignored_morph_names = {str(x) for x in ignored}

    def classify(self, name: str | None) -> Kind:
        if not name:
            return "unknown"
        kind = self._name_to_kind.get(name)
        if kind is not None:
            return kind
        self.unknown_names.add(name)
        return "unknown"

    def is_building(self, name: str | None) -> bool:
        return self.classify(name) == "building"

    def is_worker(self, name: str | None) -> bool:
        return self.classify(name) == "worker"

    def is_ignored(self, name: str | None) -> bool:
        return self.classify(name) == "ignored"

    def is_basic_army(self, name: str | None) -> bool:
        return bool(name) and name in self._basic_army

    def is_key_unit(self, name: str | None) -> bool:
        return bool(name) and name in self._key_units

    def is_tech_morph(self, from_name: str | None, to_name: str | None) -> bool:
        if not from_name or not to_name:
            return False
        allowed = self._tech_morphs.get(from_name)
        return bool(allowed and to_name in allowed)

    def is_ignored_morph_name(self, name: str | None) -> bool:
        return bool(name) and name in self._ignored_morph_names

    def canonical_name(self, name: str | None) -> str:
        if not name:
            return "Unknown"
        return name


def load_default_config(config_dir: str | Path) -> dict[str, Any]:
    path = Path(config_dir) / "default.yaml"
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}
