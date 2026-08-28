from unittest.mock import patch

from gamesaver.__main__ import build_parser
from gamesaver.game_manager import GameManager
from gamesaver.models import GameEntry
from gamesaver.repositories import GameRepository, SettingsRepository
from gamesaver.settings import Settings


def test_build_parser_defaults_to_gui():
    args = build_parser().parse_args([])
    assert args.cli is False


def test_build_parser_accepts_cli_flag():
    args = build_parser().parse_args(['--cli'])
    assert args.cli is True


def test_game_manager_copy_selected_games(tmp_path, capsys):
    user_location = tmp_path / "user"
    backup_location = tmp_path / "backup"
    source = user_location / "AppData" / "Roaming" / "Game"
    source.mkdir(parents=True)
    (source / "save.dat").write_text("progress", encoding="utf-8")
    backup_location.mkdir()

    game = GameEntry(name="Game", path="AppData/Roaming/Game")

    with patch.object(GameRepository, 'load_all', return_value=[game]):
        manager = GameManager(str(user_location), str(backup_location))
        manager.copy_selected_games([game])

    assert (backup_location / "Game" / "save.dat").exists()
    captured = capsys.readouterr()
    assert "Completed: 1 succeeded, 0 failed." in captured.out


def test_settings_save_and_load(tmp_path, monkeypatch):
    settings_path = tmp_path / "settings.json"
    user_dir = tmp_path / "user"
    backup_dir = tmp_path / "backup"
    user_dir.mkdir()
    backup_dir.mkdir()

    monkeypatch.setattr(
        'gamesaver.settings.SettingsRepository',
        lambda: SettingsRepository(str(settings_path)),
    )
    monkeypatch.setattr(Settings, 'check', lambda self: None)

    settings = Settings()
    settings.user_location = str(user_dir)
    settings.destination_location = str(backup_dir)
    settings.mode = 'spread'
    settings.save()

    loaded = SettingsRepository(str(settings_path)).load()
    assert loaded.user_location == str(user_dir)
    assert loaded.destination_location == str(backup_dir)
    assert loaded.mode == 'spread'
