import os
from pathlib import Path

BLOCKED_EXACT_PATHS = {
    "AppData",
    "Documents",
    "Saved Games",
    "Documents/My Games",
    "AppData/Roaming",
    "AppData/Local",
}


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip("/")


def is_safe_game_path(path: str) -> bool:
    normalized = normalize_path(path)
    if not normalized or normalized in BLOCKED_EXACT_PATHS:
        return False
    segments = normalized.split("/")
    if len(segments) == 1 and segments[0] in {"AppData", "Documents", "Saved Games", "Users"}:
        return False
    return True


def resolve_backup_destination(user_location: str, destination_location: str, game_path: str) -> tuple[str, str]:
    game_location = os.path.join(user_location, game_path)
    game_destination = os.path.join(destination_location, os.path.basename(game_location))
    return game_location, game_destination


def resolve_spread_paths(user_location: str, destination_location: str, game_path: str) -> tuple[str, str]:
    game_location, backup_location = resolve_backup_destination(user_location, destination_location, game_path)
    return backup_location, game_location


def validate_copy_paths(source: str, destination: str, user_location: str, destination_location: str) -> None:
    source_real = Path(source).resolve()
    destination_real = Path(destination).resolve()
    user_real = Path(user_location).resolve()
    destination_base = Path(destination_location).resolve()

    if not source_real.is_dir():
        raise ValueError(f"Source path does not exist or is not a directory: {source}")

    if not _is_relative_to(source_real, user_real):
        raise ValueError(f"Source path must stay within user location: {source}")

    destination_parent = destination_real.parent.resolve()
    if not _is_relative_to(destination_parent, destination_base):
        raise ValueError(f"Destination must stay within backup folder: {destination}")


def validate_spread_paths(source: str, destination: str, user_location: str, destination_location: str) -> None:
    source_real = Path(source).resolve()
    destination_real = Path(destination).resolve()
    user_real = Path(user_location).resolve()
    destination_base = Path(destination_location).resolve()

    if not source_real.is_dir():
        raise ValueError(f"Backup source does not exist or is not a directory: {source}")

    if not _is_relative_to(source_real, destination_base):
        raise ValueError(f"Backup source must stay within backup folder: {source}")

    destination_parent = destination_real.parent.resolve()
    if not _is_relative_to(destination_parent, user_real):
        raise ValueError(f"Restore destination must stay within user location: {destination}")


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False
