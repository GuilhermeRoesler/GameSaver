import os
import shutil
import json
from typing import Any

from constants import (
    BACKUP_PATH,
    DEFAULT_GAMES,
    DEFAULT_HOW_TO_RUN,
    DEFAULT_SETTINGS,
    GAMES_PATH,
    HOW_TO_RUN_PATH,
    SAVES_PATH,
    SETTINGS_PATH,
)
from path_policy import (
    is_safe_game_path,
    normalize_path,
    resolve_backup_destination,
    validate_copy_paths,
    validate_spread_paths,
)

__all__ = [
    "BLOCKED_EXACT_PATHS",
    "copy_game_save",
    "create_default_files",
    "ensure_directory_exists",
    "is_safe_game_path",
    "load_json",
    "normalize_path",
    "resolve_backup_destination",
    "save_json",
    "save_txt",
    "validate_copy_paths",
    "validate_spread_paths",
]

# Backward compatibility for tests importing BLOCKED_EXACT_PATHS from file_handler.
from path_policy import BLOCKED_EXACT_PATHS  # noqa: E402


def load_json(filepath: str) -> Any:
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_json(filepath: str, data: Any) -> None:
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def save_txt(filepath: str, data: str) -> None:
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(data)


def copy_game_save(source: str, destination: str) -> None:
    shutil.copytree(source, destination, dirs_exist_ok=True, symlinks=False)


def ensure_directory_exists(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def create_default_files() -> None:
    _create_games_file()
    _create_settings_file()
    _create_how_to_run_file()
    _create_saves_folder()
    _create_backup_folder()


def _create_games_file() -> None:
    if os.path.exists(GAMES_PATH):
        print("games.json file loaded!")
        return

    print("games.json file not found. Creating a default...")
    save_json(GAMES_PATH, DEFAULT_GAMES)


def _create_settings_file() -> None:
    if os.path.exists(SETTINGS_PATH):
        print("settings.json file loaded!")
        return

    print("settings.json file not found. Creating a default...")
    save_json(SETTINGS_PATH, DEFAULT_SETTINGS)


def _create_how_to_run_file() -> None:
    if os.path.exists(HOW_TO_RUN_PATH):
        print('how to run.txt file loaded!')
        return

    print('how to run.txt file not found. Creating a default...')
    save_txt(HOW_TO_RUN_PATH, DEFAULT_HOW_TO_RUN)


def _create_saves_folder() -> None:
    if not os.path.exists(SAVES_PATH):
        os.mkdir(SAVES_PATH)
        print('Saves folder created!')


def _create_backup_folder() -> None:
    if not os.path.exists(BACKUP_PATH):
        os.mkdir(BACKUP_PATH)
        print('Backup folder created!')
