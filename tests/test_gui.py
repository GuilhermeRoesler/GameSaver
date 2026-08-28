from dataclasses import dataclass

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from gamesaver.backup_service import BackupService
from gamesaver.gui.game_list_widget import GameListWidget
from gamesaver.gui.settings_widget import SettingsWidget
from gamesaver.gui.workers import OperationWorker
from gamesaver.models import GameEntry


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@dataclass
class FakeSettings:
    user_location: str = "/tmp/user"
    destination_location: str = "/tmp/backup"
    mode: str = "collect"
    saved: bool = False

    def save(self) -> None:
        self.saved = True


class FakeGameManager:
    def __init__(self, games: list[GameEntry] | None = None):
        self._games = games or []
        self.user_location = "/tmp/user"
        self.destination_location = "/tmp/backup"
        self.backup_service = BackupService(self.user_location, self.destination_location)

    def update_locations(self, user_location: str, destination_location: str) -> None:
        self.user_location = user_location
        self.destination_location = destination_location
        self.backup_service.update_locations(user_location, destination_location)

    def get_installed_games(self) -> list[GameEntry]:
        return list(self._games)


def test_settings_widget_persists_mode(qapp, qtbot):
    settings = FakeSettings(mode="collect")
    widget = SettingsWidget(settings)
    qtbot.addWidget(widget)

    widget.mode_combo.setCurrentIndex(widget.mode_combo.findData("spread"))
    assert settings.mode == "spread"
    assert settings.saved is True


def test_settings_widget_persists_paths(qapp, qtbot):
    settings = FakeSettings()
    widget = SettingsWidget(settings)
    qtbot.addWidget(widget)

    widget.user_location.setText("/home/player")
    widget.dest_location.setText("/home/player/SAVES")
    widget._apply_settings()

    assert settings.user_location == "/home/player"
    assert settings.destination_location == "/home/player/SAVES"
    assert settings.saved is True


def test_game_list_filter_hides_rows(qapp, qtbot):
    games = [
        GameEntry(name="Alpha Quest", path="AppData/Roaming/Alpha"),
        GameEntry(name="Beta Run", path="AppData/Roaming/Beta"),
    ]
    settings = FakeSettings()
    manager = FakeGameManager(games)
    widget = GameListWidget(settings, manager)  # type: ignore[arg-type]
    qtbot.addWidget(widget)

    assert widget.games_table.rowCount() == 2
    widget.search_box.setText("beta")
    assert widget.games_table.isRowHidden(0) is True
    assert widget.games_table.isRowHidden(1) is False


def test_operation_worker_marks_remaining_as_cancelled(qapp, tmp_path, qtbot):
    user = tmp_path / "user"
    backup = tmp_path / "backup"
    backup.mkdir()

    games = []
    for name in ("One", "Two", "Three"):
        path = user / "AppData" / "Roaming" / name
        path.mkdir(parents=True)
        (path / "save.dat").write_text("ok", encoding="utf-8")
        games.append(GameEntry(name=name, path=f"AppData/Roaming/{name}"))

    service = BackupService(str(user), str(backup))
    worker = OperationWorker(service, games, "collect")

    reports = []
    worker.finished_report.connect(reports.append)

    def interrupt_after_first(*_args):
        # DirectConnection: run in the worker thread so interruption is visible
        # before the next game starts (QueuedConnection races on fast CI).
        worker.requestInterruption()

    worker.progress.connect(
        interrupt_after_first,
        Qt.ConnectionType.DirectConnection,
    )
    worker.start()
    qtbot.waitUntil(lambda: len(reports) == 1, timeout=5000)

    report = reports[0]
    assert len(report.results) == 3
    assert report.results[0].success is True
    assert report.results[1].message == "Cancelled by user"
    assert report.results[2].message == "Cancelled by user"
