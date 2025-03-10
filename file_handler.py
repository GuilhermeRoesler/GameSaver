import os
import shutil
import json
from typing import Dict, Any
from constants import GAMES_PATH, SETTINGS_PATH, HOW_TO_RUN_PATH, DEFAULT_SETTINGS, DEFAULT_GAMES, DEFAULT_HOW_TO_RUN
from utils import printc

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
    shutil.copytree(source, destination, dirs_exist_ok=True)

def ensure_directory_exists(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

def create_default_files() -> None:
    # Create default configuration files if they don't exist
    _create_games_file()
    _create_settings_file()
    _create_how_to_run_file()

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
    if os.path.exists(''):
        print('how to run.txt file loaded!')
        return
    
    print('how to run.txt file not found. Creating a default...')
    save_txt(HOW_TO_RUN_PATH, DEFAULT_HOW_TO_RUN)