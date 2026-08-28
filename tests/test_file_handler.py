import os

import pytest

from gamesaver.file_handler import (
    is_safe_game_path,
    load_json,
    normalize_path,
    save_json,
    validate_copy_paths,
)


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        (r"AppData\Roaming\Game", True),
        ("Documents/My Games/Title", True),
        ("AppData", False),
        ("Documents", False),
        ("Saved Games", False),
        ("AppData/Roaming", False),
        ("", False),
    ],
)
def test_is_safe_game_path(path, expected):
    assert is_safe_game_path(path) is expected


def test_normalize_path():
    assert normalize_path("\\AppData\\Game\\") == "AppData/Game"
    assert normalize_path("AppData/Game/") == "AppData/Game"


def test_save_and_load_json(tmp_path):
    filepath = tmp_path / "data.json"
    payload = {"mode": "collect", "games": 1}

    save_json(str(filepath), payload)

    assert load_json(str(filepath)) == payload


def test_validate_copy_paths_rejects_missing_source(tmp_path):
    user_location = str(tmp_path / "user")
    backup_location = str(tmp_path / "backup")
    os.makedirs(backup_location)

    with pytest.raises(ValueError, match="Source path does not exist"):
        validate_copy_paths(
            str(tmp_path / "user" / "missing"),
            str(tmp_path / "backup" / "game"),
            user_location,
            backup_location,
        )


def test_validate_copy_paths_accepts_valid_paths(tmp_path):
    user_location = str(tmp_path / "user")
    backup_location = str(tmp_path / "backup")
    source = os.path.join(user_location, "AppData", "Roaming", "Game")
    destination = os.path.join(backup_location, "Game")
    os.makedirs(source)
    os.makedirs(backup_location)

    validate_copy_paths(source, destination, user_location, backup_location)


def test_validate_copy_paths_rejects_escape_from_user_location(tmp_path):
    user_location = str(tmp_path / "user")
    backup_location = str(tmp_path / "backup")
    outside_source = str(tmp_path / "outside")
    destination = os.path.join(backup_location, "Game")
    os.makedirs(outside_source)
    os.makedirs(user_location)
    os.makedirs(backup_location)

    with pytest.raises(ValueError, match="must stay within user location"):
        validate_copy_paths(outside_source, destination, user_location, backup_location)
