import os
import shutil
import json
from typing import Dict
from constants import GAMES_PATH, SETTINGS_PATH, HOW_TO_RUN_PATH, DEFAULT_SETTINGS, DEFAULT_GAMES, DEFAULT_HOW_TO_RUN, SAVES_PATH, BACKUP_PATH
from utils import printc

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


def validate_copy_paths(source: str, destination: str, user_location: str, destination_location: str) -> None:
    source_real = os.path.realpath(source)
    destination_real = os.path.realpath(destination)
    user_real = os.path.realpath(user_location)
    destination_base = os.path.realpath(destination_location)

    if not os.path.isdir(source_real):
        raise ValueError(f"Source path does not exist or is not a directory: {source}")

    if not source_real.startswith(user_real):
        raise ValueError(f"Source path must stay within user location: {source}")

    destination_parent = os.path.realpath(os.path.dirname(destination_real))
    if not destination_parent.startswith(destination_base):
        raise ValueError(f"Destination must stay within backup folder: {destination}")

def load_json(filepath: str) -> Dict:
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(filepath: str, data: Dict) -> None:
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def save_txt(filepath: str, data: str) -> None:
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(data)

def copy_game_save(source: str, destination: str) -> None:
    printc('yellow', 'Copying files...')
    shutil.copytree(source, destination, dirs_exist_ok=True, symlinks=False)

def ensure_directory_exists(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

def create_default_files() -> None:
    # Create default configuration files if they don't exist
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

def _create_how_to_run_file():
    if os.path.exists(HOW_TO_RUN_PATH):
        print('how to run.txt file loaded!')
        return

    print('how to run.txt file not found. Creating a default...')
    save_txt(HOW_TO_RUN_PATH, DEFAULT_HOW_TO_RUN)

def _create_saves_folder() -> None:
    if not os.path.exists(SAVES_PATH):
        os.mkdir(SAVES_PATH)
        print('Saves folder created!')
        return

def _create_backup_folder() -> None:
    if not os.path.exists(BACKUP_PATH):
        os.mkdir(BACKUP_PATH)
        print('Backup folder created!')
        return
