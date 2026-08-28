import os

import pytest

from gamesaver.backup_service import BackupService
from gamesaver.file_utils import format_size
from gamesaver.models import AppSettings, GameEntry
from gamesaver.path_policy import validate_spread_paths
from gamesaver.repositories import SettingsRepository


def test_collect_game_copies_save_folder(tmp_path):
    user_location = tmp_path / "user"
    backup_location = tmp_path / "backup"
    source = user_location / "AppData" / "Roaming" / "Game"
    source.mkdir(parents=True)
    (source / "save.dat").write_text("progress", encoding="utf-8")

    service = BackupService(str(user_location), str(backup_location))
    game = GameEntry(name="Game", path="AppData/Roaming/Game")
    result = service.collect_game(game)

    assert result.success is True
    assert (backup_location / "Game" / "save.dat").exists()


def test_spread_game_restores_save_folder(tmp_path):
    user_location = tmp_path / "user"
    backup_location = tmp_path / "backup"
    source = user_location / "AppData" / "Roaming" / "Game"
    source.mkdir(parents=True)
    (source / "save.dat").write_text("progress", encoding="utf-8")

    service = BackupService(str(user_location), str(backup_location))
    game = GameEntry(name="Game", path="AppData/Roaming/Game")
    collect_result = service.collect_game(game)
    assert collect_result.success is True

    (source / "save.dat").unlink()
    source.rmdir()

    spread_result = service.spread_game(game)
    assert spread_result.success is True
    assert (source / "save.dat").read_text(encoding="utf-8") == "progress"


def test_collect_game_rejects_unsafe_path(tmp_path):
    service = BackupService(str(tmp_path / "user"), str(tmp_path / "backup"))
    game = GameEntry(name="Unsafe", path="AppData")
    result = service.collect_game(game)
    assert result.success is False


def test_get_installed_games_enriches_metadata(tmp_path):
    user_location = tmp_path / "user"
    backup_location = tmp_path / "backup"
    source = user_location / "AppData" / "Roaming" / "Game"
    source.mkdir(parents=True)
    (source / "save.dat").write_text("progress", encoding="utf-8")

    service = BackupService(str(user_location), str(backup_location))
    games = service.get_installed_games([GameEntry(name="Game", path="AppData/Roaming/Game")])

    assert len(games) == 1
    assert games[0].size > 0
    assert games[0].last_save != ""


def test_settings_repository_round_trip(tmp_path):
    settings_path = tmp_path / "settings.json"
    repository = SettingsRepository(str(settings_path))
    settings = AppSettings(
        user_location=str(tmp_path / "user"),
        destination_location=str(tmp_path / "backup"),
        mode="collect",
    )

    repository.save(settings)
    loaded = repository.load()

    assert loaded == settings


def test_format_size():
    assert format_size(512) == "512 B"
    assert format_size(2048) == "2.0 KB"


def test_validate_spread_paths_rejects_outside_backup(tmp_path):
    user_location = str(tmp_path / "user")
    backup_location = str(tmp_path / "backup")
    outside_source = str(tmp_path / "outside")
    destination = os.path.join(user_location, "AppData", "Roaming", "Game")
    os.makedirs(outside_source)
    os.makedirs(user_location)
    os.makedirs(backup_location)

    with pytest.raises(ValueError, match="must stay within backup folder"):
        validate_spread_paths(outside_source, destination, user_location, backup_location)
