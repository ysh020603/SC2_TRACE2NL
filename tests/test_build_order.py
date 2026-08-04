from __future__ import annotations

from pathlib import Path

from sc2_replay_miner.build_order import build_core_6m, build_strategy_8m, generate_build_orders
from sc2_replay_miner.models import MacroEventRecord
from sc2_replay_miner.taxonomy import Taxonomy

CONFIG_DIR = Path(__file__).resolve().parents[1] / "configs"


def _event(
    player_id: int,
    frame: int,
    second: float,
    category: str,
    name: str,
    occurrence_index: int = 1,
    is_initial: bool = False,
) -> MacroEventRecord:
    return MacroEventRecord(
        replay_id="abc",
        player_id=player_id,
        frame=frame,
        second=second,
        event_type="Synthetic",
        category=category,
        raw_name=name,
        canonical_name=name,
        occurrence_index=occurrence_index,
        is_initial=is_initial,
    )


def test_core_excludes_workers_and_unit_spam():
    events = [
        _event(1, 100, 10, "building_start", "SupplyDepot"),
        _event(1, 200, 20, "unit_born", "Marine", occurrence_index=1),
        _event(1, 300, 30, "unit_born", "SCV", occurrence_index=13),
        _event(1, 400, 40, "upgrade_complete", "Stimpack"),
        _event(1, 500, 500, "building_start", "Factory"),  # after 6m
    ]
    core = build_core_6m(events, max_seconds=360)
    names = [e.canonical_name for e in core]
    assert names == ["SupplyDepot", "Stimpack"]


def test_strategy_keeps_first_key_units():
    taxonomy = Taxonomy(CONFIG_DIR)
    events = [
        _event(1, 100, 10, "building_start", "Factory"),
        _event(1, 200, 20, "unit_born", "Reaper", occurrence_index=1),
        _event(1, 210, 21, "unit_born", "Reaper", occurrence_index=2),
        _event(1, 220, 22, "unit_born", "Reaper", occurrence_index=3),
        _event(1, 300, 30, "unit_born", "Marine", occurrence_index=1),
        _event(1, 310, 31, "unit_born", "Marine", occurrence_index=2),
    ]
    strategy = build_strategy_8m(events, taxonomy=taxonomy)
    names = [(e.canonical_name, e.occurrence_index) for e in strategy]
    assert ("Factory", 1) in names
    assert ("Reaper", 1) in names
    assert ("Reaper", 2) in names
    assert ("Reaper", 3) not in names
    assert ("Marine", 1) in names
    assert ("Marine", 2) not in names


def test_generate_all_three_types():
    taxonomy = Taxonomy(CONFIG_DIR)
    events = [_event(1, 100, 10, "building_start", "Barracks")]
    bos = generate_build_orders(events, taxonomy)
    assert {b.bo_type for b in bos} == {"core_6m", "strategy_8m", "all_macro"}
