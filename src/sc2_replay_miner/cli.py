"""CLI entrypoint for sc2-replay-miner."""

from __future__ import annotations

import json
import os
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from sc2_replay_miner import __version__
from sc2_replay_miner.action_exporters import write_action_match_json
from sc2_replay_miner.action_models import ActionParsedReplay
from sc2_replay_miner.action_parser import MacroActionParser
from sc2_replay_miner.event_utils import format_clock
from sc2_replay_miner.exporters import (
    append_jsonl,
    parsed_to_tables,
    write_full_match_json,
    write_full_matches,
    write_json_preview,
    write_parquet_tables,
    write_summary_report,
    write_unknown_names,
)
from sc2_replay_miner.inspect import inspect_replay
from sc2_replay_miner.models import ParsedReplay
from sc2_replay_miner.parser import ReplayParser, default_project_paths
from sc2_replay_miner.standard_actions import DEFAULT_DATABASE
from sc2_replay_miner.taxonomy import load_default_config
from sc2_replay_miner.validation import build_summary_report, load_parse_errors, validate_parsed

app = typer.Typer(
    name="sc2mine",
    help="Extract bilateral macro events and build orders from SC2Replay files.",
    no_args_is_help=True,
)
console = Console()


def _project_root() -> Path:
    root, _ = default_project_paths()
    return root


def _project_config_dir(config_dir: Path | None) -> Path:
    if config_dir:
        return config_dir
    _, default_dir = default_project_paths()
    return default_dir


def _category_paths(category: str) -> tuple[Path, Path, Path]:
    """Return (replays_dir, artifacts_dir, json_dir) for a mirrored category."""
    root = _project_root()
    return (
        root / "data" / "replays" / category,
        root / "data" / "artifacts" / category,
        root / "data" / "full_json" / category,
    )


def _iter_replays(directory: Path) -> list[Path]:
    files = sorted(
        {
            *directory.rglob("*.SC2Replay"),
            *directory.rglob("*.sc2replay"),
        }
    )
    return [p for p in files if p.is_file()]


def _parse_one(args: tuple[str, str]) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Worker entry: return (parsed_dict, error_dict)."""
    replay_path, config_dir = args
    parser = ReplayParser(config_dir=config_dir)
    parsed, err = parser.parse_safe(replay_path)
    if err is not None:
        return None, err.model_dump()
    assert parsed is not None
    return parsed.model_dump(), None


def _parsed_from_dict(data: dict[str, Any]) -> ParsedReplay:
    return ParsedReplay.model_validate(data)


def _parse_action_one(
    args: tuple[str, str, str],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Worker entry for the independent game-events macro parser."""
    replay_path, config_dir, action_database = args
    parser = MacroActionParser(
        config_dir=config_dir,
        action_database=action_database,
    )
    parsed, err = parser.parse_safe(replay_path)
    if err is not None:
        return None, err.model_dump()
    assert parsed is not None
    return parsed.model_dump(), None


@app.callback()
def main() -> None:
    """SC2 Replay Miner CLI."""


@app.command("inspect")
def inspect_cmd(
    replay: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    max_events: int = typer.Option(30, help="How many macro events to print"),
) -> None:
    """Print raw metadata, players, and tracker event samples."""
    inspect_replay(str(replay), max_events=max_events)


@app.command("parse-file")
def parse_file_cmd(
    replay: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    category: str | None = typer.Option(
        None, "--category", "-c", help="Mirrored data category name"
    ),
    artifacts: Path | None = typer.Option(
        None, "--artifacts", "-a", help="Artifacts output directory"
    ),
    json_out: Path | None = typer.Option(
        None, "--json-out", "-j", help="Full-match JSON output directory"
    ),
    config_dir: Path | None = typer.Option(None, "--config-dir"),
) -> None:
    """Parse one replay into artifacts + full-match JSON."""
    if category:
        _, cat_artifacts, cat_json = _category_paths(category)
        artifacts = artifacts or cat_artifacts
        json_out = json_out or cat_json
    artifacts = artifacts or Path("data/artifacts/human_tournament")
    json_out = json_out or Path("data/full_json/human_tournament")

    cfg_dir = _project_config_dir(config_dir)
    config = load_default_config(cfg_dir)
    parser = ReplayParser(config_dir=cfg_dir, config=config)
    parsed, err = parser.parse_safe(replay)
    artifacts.mkdir(parents=True, exist_ok=True)
    json_out.mkdir(parents=True, exist_ok=True)

    if err is not None:
        append_jsonl(artifacts / "parse_errors.jsonl", err.model_dump())
        console.print(f"[red]Parse failed[/red]: {err.exception_type}: {err.message}")
        raise typer.Exit(code=1)

    assert parsed is not None
    issues = validate_parsed(parsed)
    tables = parsed_to_tables([parsed])
    compression = config.get("output", {}).get("compression", "zstd")
    write_parquet_tables(tables, artifacts, compression=compression)
    if config.get("output", {}).get("write_json_preview", True):
        write_json_preview(parsed, artifacts / "preview.json")
    write_unknown_names(parsed.unknown_names, artifacts / "unknown_names.json")
    if config.get("output", {}).get("write_full_match_json", True):
        write_full_match_json(parsed, json_out / f"{parsed.replay.replay_id}.json")

    console.print(f"[green]OK[/green] replay_id={parsed.replay.replay_id}")
    console.print(
        f"players={len(parsed.players)} macros={len(parsed.macro_events)} "
        f"build_orders={len(parsed.build_orders)}"
    )
    console.print(f"artifacts={artifacts}")
    console.print(f"json_out={json_out / f'{parsed.replay.replay_id}.json'}")
    if issues:
        console.print("[yellow]Validation warnings:[/yellow]")
        for issue in issues:
            console.print(f"  - {issue}")


@app.command("parse-dir")
def parse_dir_cmd(
    directory: Path | None = typer.Argument(None, exists=False, dir_okay=True),
    category: str | None = typer.Option(
        None, "--category", "-c", help="Mirrored data category name"
    ),
    artifacts: Path | None = typer.Option(
        None, "--artifacts", "-a", help="Artifacts output directory"
    ),
    json_out: Path | None = typer.Option(
        None, "--json-out", "-j", help="Full-match JSON output directory"
    ),
    workers: int | None = typer.Option(None, "--workers", "-w"),
    config_dir: Path | None = typer.Option(None, "--config-dir"),
) -> None:
    """Batch-parse a directory of replays with ProcessPoolExecutor."""
    if category:
        cat_replays, cat_artifacts, cat_json = _category_paths(category)
        directory = directory or cat_replays
        artifacts = artifacts or cat_artifacts
        json_out = json_out or cat_json
    if directory is None:
        console.print("[red]Provide a directory or --category[/red]")
        raise typer.Exit(code=1)
    if not directory.is_dir():
        console.print(f"[red]Not a directory[/red]: {directory}")
        raise typer.Exit(code=1)
    artifacts = artifacts or Path("data/artifacts/human_tournament")
    json_out = json_out or Path("data/full_json/human_tournament")

    cfg_dir = _project_config_dir(config_dir)
    config = load_default_config(cfg_dir)
    runtime = config.get("runtime", {})
    if workers is None:
        workers = int(runtime.get("workers") or min(8, max(1, (os.cpu_count() or 2) // 2)))
    compression = config.get("output", {}).get("compression", "zstd")

    files = _iter_replays(directory)
    if not files:
        console.print("[red]No .SC2Replay files found[/red]")
        raise typer.Exit(code=1)

    artifacts.mkdir(parents=True, exist_ok=True)
    json_out.mkdir(parents=True, exist_ok=True)
    error_path = artifacts / "parse_errors.jsonl"
    if error_path.exists():
        error_path.unlink()

    console.print(f"Parsing {len(files)} replays with workers={workers}")
    parsed_list: list[ParsedReplay] = []
    errors: list[dict[str, Any]] = []
    tasks = [(str(p), str(cfg_dir)) for p in files]

    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_parse_one, task) for task in tasks]
        for fut in as_completed(futures):
            parsed_dict, err_dict = fut.result()
            if err_dict is not None:
                errors.append(err_dict)
                append_jsonl(error_path, err_dict)
                continue
            assert parsed_dict is not None
            parsed_list.append(_parsed_from_dict(parsed_dict))

    tables = parsed_to_tables(parsed_list)
    write_parquet_tables(tables, artifacts, compression=compression)

    unknown = sorted({n for p in parsed_list for n in p.unknown_names})
    write_unknown_names(unknown, artifacts / "unknown_names.json")
    report = build_summary_report(parsed_list, errors)
    write_summary_report(report, artifacts / "summary_report.json")
    if config.get("output", {}).get("write_full_match_json", True):
        combined_path, _ = write_full_matches(parsed_list, json_out)
        console.print(f"full_matches_json={combined_path}")

    console.print(
        f"[green]Done[/green] success={report['parsed_successfully']} "
        f"failed={len(errors)} rate={report['parse_success_rate']:.2%}"
    )
    console.print(f"artifacts={artifacts}")
    console.print(f"json_out={json_out}")


@app.command("parse-actions-file")
def parse_actions_file_cmd(
    replay: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    json_out: Path = typer.Option(
        Path("data/action_json"),
        "--json-out",
        "-j",
        help="Macro-action JSON output directory",
    ),
    config_dir: Path | None = typer.Option(None, "--config-dir"),
    action_database: Path = typer.Option(
        DEFAULT_DATABASE,
        "--action-database",
        help="SC2 structured database containing canonical Ability names",
    ),
) -> None:
    """Parse one replay's production/build/research commands; exclude micro."""
    cfg_dir = _project_config_dir(config_dir)
    parser = MacroActionParser(
        config_dir=cfg_dir,
        action_database=action_database,
    )
    parsed, err = parser.parse_safe(replay)
    if err is not None:
        console.print(f"[red]Parse failed[/red]: {err.exception_type}: {err.message}")
        raise typer.Exit(code=1)

    assert parsed is not None
    output_path = write_action_match_json(
        parsed,
        json_out / f"{parsed.replay.replay_id}.json",
    )
    per_player = {
        player.player_id: sum(
            1 for action in parsed.macro_actions if action.player_id == player.player_id
        )
        for player in parsed.players
        if not player.is_observer
    }
    console.print(
        f"[green]OK[/green] replay_id={parsed.replay.replay_id} "
        f"macro_actions={len(parsed.macro_actions)}"
    )
    console.print(f"per_player={per_player}")
    console.print(f"json_out={output_path}")


@app.command("parse-actions-dir")
def parse_actions_dir_cmd(
    directory: Path = typer.Argument(..., exists=True, file_okay=False, readable=True),
    json_out: Path = typer.Option(
        Path("data/action_json"),
        "--json-out",
        "-j",
        help="Macro-action JSON output directory",
    ),
    workers: int | None = typer.Option(None, "--workers", "-w"),
    limit: int | None = typer.Option(None, "--limit", min=1),
    seed: int = typer.Option(42, "--seed"),
    config_dir: Path | None = typer.Option(None, "--config-dir"),
    action_database: Path = typer.Option(
        DEFAULT_DATABASE,
        "--action-database",
        help="SC2 structured database containing canonical Ability names",
    ),
) -> None:
    """Batch-parse macro commands from game events without micro or positions."""
    cfg_dir = _project_config_dir(config_dir)
    config = load_default_config(cfg_dir)
    runtime = config.get("runtime", {})
    if workers is None:
        workers = int(runtime.get("workers") or min(8, max(1, (os.cpu_count() or 2) // 2)))

    files = _iter_replays(directory)
    if limit is not None and len(files) > limit:
        random.seed(seed)
        files = sorted(random.sample(files, limit))
    if not files:
        console.print("[red]No .SC2Replay files found[/red]")
        raise typer.Exit(code=1)

    json_out.mkdir(parents=True, exist_ok=True)
    error_path = json_out / "parse_errors.jsonl"
    if error_path.exists():
        error_path.unlink()
    console.print(f"Parsing {len(files)} replays with workers={workers}")

    success = 0
    errors: list[dict[str, Any]] = []
    category_counts: dict[str, int] = {}
    action_total = 0
    standard_mapped = 0
    standard_unmapped = 0
    tasks = [
        (str(path), str(cfg_dir), str(action_database))
        for path in files
    ]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_parse_action_one, task) for task in tasks]
        for future in as_completed(futures):
            parsed_dict, err_dict = future.result()
            if err_dict is not None:
                errors.append(err_dict)
                append_jsonl(error_path, err_dict)
                continue
            assert parsed_dict is not None
            parsed = ActionParsedReplay.model_validate(parsed_dict)
            write_action_match_json(
                parsed,
                json_out / f"{parsed.replay.replay_id}.json",
            )
            success += 1
            action_total += len(parsed.macro_actions)
            for action in parsed.macro_actions:
                category_counts[action.category] = category_counts.get(action.category, 0) + 1
                if action.standard_action_name is None:
                    standard_unmapped += 1
                else:
                    standard_mapped += 1

    summary = {
        "input_directory": str(directory.resolve()),
        "sample_seed": seed if limit is not None else None,
        "requested_limit": limit,
        "total": len(files),
        "success": success,
        "failed": len(errors),
        "success_rate": success / len(files),
        "macro_action_count": action_total,
        "category_counts": category_counts,
        "standard_action_mapped": standard_mapped,
        "standard_action_unmapped": standard_unmapped,
        "micro_actions_included": False,
        "positions_included": False,
        "standard_action_database": str(action_database.resolve()),
    }
    (json_out / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    console.print(
        f"[green]Done[/green] success={success} failed={len(errors)} "
        f"rate={summary['success_rate']:.2%} macro_actions={action_total}"
    )
    console.print(f"json_out={json_out}")


@app.command("show-bo")
def show_bo_cmd(
    replay: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    bo_type: str = typer.Option("strategy_8m", "--type", "-t"),
    config_dir: Path | None = typer.Option(None, "--config-dir"),
) -> None:
    """Print a human-readable bilateral build order."""
    cfg_dir = _project_config_dir(config_dir)
    parser = ReplayParser(config_dir=cfg_dir)
    parsed = parser.parse(replay)

    console.print(f"Replay: {replay.name}")
    console.print(f"Map: {parsed.replay.map_name}")
    console.print(f"Version: {parsed.replay.release_string}")
    duration = parsed.replay.game_length_seconds or 0
    console.print(f"Duration: {format_clock(duration)}")
    console.print()

    for player in sorted(parsed.players, key=lambda p: p.player_id):
        if player.is_observer:
            continue
        mmr = player.mmr if player.mmr is not None else "null"
        console.print(
            f"Player {player.player_id} — {player.play_race} — "
            f"{player.result} — MMR {mmr}"
        )
        rows = [
            b
            for b in parsed.build_orders
            if b.player_id == player.player_id and b.bo_type == bo_type
        ]
        rows.sort(key=lambda b: (b.frame, b.bo_index))
        if not rows:
            console.print("  (empty)")
        for item in rows:
            verb = {
                "building_start": "started",
                "tech_morph": "morphed",
                "upgrade_complete": "completed",
                "unit_born": "born",
                "unit_started": "started",
                "building_complete": "completed",
            }.get(item.category, item.category)
            suffix = ""
            if item.occurrence_index and item.category in {"unit_born", "unit_started"}:
                suffix = f" #{item.occurrence_index}"
            console.print(
                f"{format_clock(item.second)} {item.canonical_name}{suffix} {verb}"
            )
        console.print()


@app.command("report")
def report_cmd(
    artifacts_dir: Path = typer.Argument(
        ..., exists=True, file_okay=False, help="Artifacts directory from parse-dir"
    ),
    output: Path | None = typer.Option(None, "--output", "-o"),
    sample_md: Path | None = typer.Option(None, "--sample-md"),
    sample_n: int = typer.Option(5, "--sample-n"),
    seed: int = typer.Option(42, "--seed"),
) -> None:
    """Generate summary copy and sample_build_orders.md inside an artifacts dir."""
    output = output or (artifacts_dir / "report.json")
    sample_md = sample_md or (artifacts_dir / "sample_build_orders.md")
    summary_path = artifacts_dir / "summary_report.json"
    errors = load_parse_errors(artifacts_dir / "parse_errors.jsonl")
    if summary_path.exists():
        report = json.loads(summary_path.read_text(encoding="utf-8"))
    else:
        report = {
            "note": "summary_report.json missing; only error file scanned",
            "error_count": len(errors),
        }
    write_summary_report(report, output)

    # Build sample markdown from strategy_8m in parquet if available
    import pandas as pd

    replays_path = artifacts_dir / "replays.parquet"
    players_path = artifacts_dir / "players.parquet"
    bos_path = artifacts_dir / "build_orders.parquet"
    lines = ["# Sample Build Orders", ""]
    if replays_path.exists() and players_path.exists() and bos_path.exists():
        replays = pd.read_parquet(replays_path)
        players = pd.read_parquet(players_path)
        bos = pd.read_parquet(bos_path)
        ids = list(replays["replay_id"].unique())
        random.seed(seed)
        sample_ids = ids if len(ids) <= sample_n else random.sample(ids, sample_n)
        for rid in sample_ids:
            rrow = replays[replays["replay_id"] == rid].iloc[0]
            lines.append(f"## {Path(str(rrow['source_file'])).name}")
            lines.append("")
            lines.append(f"- map: {rrow.get('map_name')}")
            lines.append(f"- version: {rrow.get('release_string')}")
            lines.append(f"- duration_s: {rrow.get('game_length_seconds')}")
            lines.append("")
            prows = players[players["replay_id"] == rid]
            for _, player in prows.iterrows():
                if bool(player.get("is_observer")):
                    continue
                mmr = player.get("mmr")
                mmr_s = "null" if pd.isna(mmr) else str(int(mmr))
                lines.append(
                    f"### Player {player['player_id']} — {player.get('play_race')} — "
                    f"{player.get('result')} — MMR {mmr_s}"
                )
                lines.append("")
                brows = bos[
                    (bos["replay_id"] == rid)
                    & (bos["player_id"] == player["player_id"])
                    & (bos["bo_type"] == "strategy_8m")
                ].sort_values(["frame", "bo_index"])
                if brows.empty:
                    lines.append("_empty_")
                else:
                    for _, item in brows.iterrows():
                        lines.append(
                            f"- {format_clock(float(item['second']))} "
                            f"{item['canonical_name']} ({item['category']})"
                        )
                lines.append("")
    else:
        lines.append("_Missing parquet tables; run parse-dir first._")

    sample_md.parent.mkdir(parents=True, exist_ok=True)
    sample_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    console.print(f"Wrote {output}")
    console.print(f"Wrote {sample_md}")


@app.command("version")
def version_cmd() -> None:
    """Show package version."""
    console.print(__version__)


if __name__ == "__main__":
    app()
