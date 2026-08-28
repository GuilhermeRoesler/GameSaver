import json

from gamesaver.file_handler import create_default_files, load_json


def test_create_default_files_writes_runtime_files(tmp_path, monkeypatch):
    monkeypatch.setattr('gamesaver.file_handler.GAMES_PATH', str(tmp_path / 'games.json'))
    monkeypatch.setattr('gamesaver.file_handler.SETTINGS_PATH', str(tmp_path / 'settings.json'))
    monkeypatch.setattr('gamesaver.file_handler.HOW_TO_RUN_PATH', str(tmp_path / 'how to run.txt'))
    monkeypatch.setattr('gamesaver.file_handler.SAVES_PATH', str(tmp_path / 'SAVES'))
    monkeypatch.setattr('gamesaver.file_handler.BACKUP_PATH', str(tmp_path / 'Backup'))

    create_default_files()

    assert (tmp_path / 'games.json').exists()
    assert (tmp_path / 'settings.json').exists()
    assert (tmp_path / 'SAVES').is_dir()
    assert (tmp_path / 'Backup').is_dir()
    assert isinstance(load_json(str(tmp_path / 'settings.json')), dict)


def test_create_default_files_is_idempotent(tmp_path, monkeypatch):
    settings_path = tmp_path / 'settings.json'
    settings_path.write_text(json.dumps({"mode": "collect"}), encoding='utf-8')

    monkeypatch.setattr('gamesaver.file_handler.GAMES_PATH', str(tmp_path / 'games.json'))
    monkeypatch.setattr('gamesaver.file_handler.SETTINGS_PATH', str(settings_path))
    monkeypatch.setattr('gamesaver.file_handler.HOW_TO_RUN_PATH', str(tmp_path / 'how to run.txt'))
    monkeypatch.setattr('gamesaver.file_handler.SAVES_PATH', str(tmp_path / 'SAVES'))
    monkeypatch.setattr('gamesaver.file_handler.BACKUP_PATH', str(tmp_path / 'Backup'))

    create_default_files()
    assert load_json(str(settings_path)) == {"mode": "collect"}
