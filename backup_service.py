import os
import shutil

from file_utils import format_timestamp, get_directory_size, get_latest_mtime
from models import BackupReport, GameEntry, OperationResult
from path_policy import (
    is_safe_game_path,
    resolve_backup_destination,
    resolve_spread_paths,
    validate_copy_paths,
    validate_spread_paths,
)


class BackupService:
    def __init__(self, user_location: str, destination_location: str):
        self.user_location = user_location
        self.destination_location = destination_location

    def update_locations(self, user_location: str, destination_location: str) -> None:
        self.user_location = user_location
        self.destination_location = destination_location

    def get_installed_games(self, all_games: list[GameEntry]) -> list[GameEntry]:
        found_games = []
        for game in all_games:
            full_path = os.path.join(self.user_location, game.path)
            if os.path.exists(full_path):
                found_games.append(self.enrich_game_metadata(game))
        return found_games

    def enrich_game_metadata(self, game: GameEntry) -> GameEntry:
        full_path = os.path.join(self.user_location, game.path)
        if not os.path.isdir(full_path):
            return game

        size = get_directory_size(full_path)
        last_save = format_timestamp(get_latest_mtime(full_path))
        return GameEntry(
            name=game.name,
            path=game.path,
            size=size,
            last_save=last_save,
        )

    def collect_game(self, game: GameEntry) -> OperationResult:
        if not game.path:
            return OperationResult(
                game_name=game.name,
                success=False,
                message="Missing path configuration",
            )

        if not is_safe_game_path(game.path):
            return OperationResult(
                game_name=game.name,
                success=False,
                message="Path is too broad or unsafe",
            )

        source, destination = resolve_backup_destination(
            self.user_location,
            self.destination_location,
            game.path,
        )

        try:
            validate_copy_paths(source, destination, self.user_location, self.destination_location)
            self._copy_tree(source, destination)
        except (ValueError, OSError) as error:
            return OperationResult(
                game_name=game.name,
                success=False,
                message=str(error),
                source=source,
                destination=destination,
            )

        return OperationResult(
            game_name=game.name,
            success=True,
            message=f"Backed up into {destination}",
            source=source,
            destination=destination,
        )

    def collect_games(self, games: list[GameEntry]) -> BackupReport:
        return BackupReport(results=[self.collect_game(game) for game in games])

    def spread_game(self, game: GameEntry) -> OperationResult:
        if not game.path:
            return OperationResult(
                game_name=game.name,
                success=False,
                message="Missing path configuration",
            )

        if not is_safe_game_path(game.path):
            return OperationResult(
                game_name=game.name,
                success=False,
                message="Path is too broad or unsafe",
            )

        source, destination = resolve_spread_paths(
            self.user_location,
            self.destination_location,
            game.path,
        )

        try:
            validate_spread_paths(source, destination, self.user_location, self.destination_location)
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            self._copy_tree(source, destination)
        except (ValueError, OSError) as error:
            return OperationResult(
                game_name=game.name,
                success=False,
                message=str(error),
                source=source,
                destination=destination,
            )

        return OperationResult(
            game_name=game.name,
            success=True,
            message=f"Restored into {destination}",
            source=source,
            destination=destination,
        )

    def spread_games(self, games: list[GameEntry]) -> BackupReport:
        return BackupReport(results=[self.spread_game(game) for game in games])

    @staticmethod
    def _copy_tree(source: str, destination: str) -> None:
        shutil.copytree(source, destination, dirs_exist_ok=True, symlinks=False)
