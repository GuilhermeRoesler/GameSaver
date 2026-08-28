import os

from gamesaver.gui.window_icon import load_app_icon, resolve_icon_path


def test_resolve_icon_path_finds_asset():
    path = resolve_icon_path()
    assert path is not None
    assert os.path.exists(path)
    assert path.lower().endswith(('.ico', '.png'))


def test_load_app_icon_is_not_null(qapp):
    icon = load_app_icon()
    assert not icon.isNull()
