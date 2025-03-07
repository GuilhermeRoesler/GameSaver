import os
import shutil
import json
from typing import Dict, Any
from constants import GAMES_PATH, SETTINGS_PATH, DEFAULT_SETTINGS, DEFAULT_GAMES

def load_json(filepath: str) -> Dict:
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(filepath: str, data: Dict) -> None:
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def copy_game_save(source: str, destination: str) -> None:
    shutil.copytree(source, destination, dirs_exist_ok=True)

def ensure_directory_exists(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

def create_default_files(self) -> None:
    """Create default configuration files if they don't exist"""
    create_games_file()
    create_settings_file()

def create_games_file(self) -> None:
    if os.path.exists(GAMES_PATH):
        print("games.json file loaded!")
        return
    
    print("games.json file not found. Creating a default...")
    save_json(GAMES_PATH, DEFAULT_GAMES)

def create_settings_file(self) -> None:
    if os.path.exists(SETTINGS_PATH):
        print("settings.json file loaded!")
        return
        
    print("settings.json file not found. Creating a default...")
    save_json(SETTINGS_PATH, DEFAULT_SETTINGS)