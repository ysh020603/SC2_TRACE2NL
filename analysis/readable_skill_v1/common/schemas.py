from __future__ import annotations


def require_keys(payload: dict, keys: set[str], label: str) -> None:
    missing = keys - payload.keys()
    if missing:
        raise ValueError(f"{label} missing fields: {sorted(missing)}")


def validate_ir(payload: dict) -> None:
    require_keys(payload, {"method", "opening_id", "race", "opponent_race", "opening_evidence", "own_states", "opponent_states", "transitions", "allowed_information", "provenance"}, "method IR")


def validate_projection(payload: dict) -> None:
    require_keys(payload, {"method", "opening_id", "opening_projection", "states", "nodes", "provenance"}, "projection")
