import os
from typing import Any

from constants import DATABASE_PATH, DEFAULT_SETTINGS, GAMES_PATH, SETTINGS_PATH
from file_handler import load_json, save_json
from models import AppSettings, GameEntry


def load_json_list(filepath: str) -> list[dict[str, Any]]:
    data = load_json(filepath)
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array in {filepath}")
    return data


class GameRepository:
    def __init__(self, database_path: str = DATABASE_PATH, games_path: str = GAMES_PATH):
        self.database_path = database_path
        self.games_path = games_path

    def load_all(self) -> list[GameEntry]:
        database_games = load_json_list(self.database_path)
        extra_games = load_json_list(self.games_path)
        return [GameEntry.from_dict(game) for game in database_games + extra_games]


class SettingsRepository:
    def __init__(self, settings_path: str = SETTINGS_PATH):
        self.settings_path = settings_path

    def load(self) -> AppSettings:
        if os.path.exists(self.settings_path):
            return AppSettings.from_dict(load_json(self.settings_path))
        return AppSettings(
            user_location=DEFAULT_SETTINGS["user_location"],
            destination_location=DEFAULT_SETTINGS["destination_location"],
            mode=DEFAULT_SETTINGS["mode"],
        )

    def save(self, settings: AppSettings) -> None:
        save_json(self.settings_path, settings.to_dict())
