from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QGroupBox,
                            QTableWidget, QTableWidgetItem, QHeaderView,
                            QSizePolicy, QMessageBox, QProgressDialog)
from PyQt6.QtCore import Qt

from ..game_manager import GameManager
from ..models import BackupReport, GameEntry
from .workers import OperationWorker


class GameListWidget(QWidget):
    def __init__(self, settings, game_manager: GameManager):
        super().__init__()

        self.settings = settings
        self.game_manager = game_manager
        self._games: list[GameEntry] = []
        self._worker: OperationWorker | None = None
        self._progress_dialog: QProgressDialog | None = None
        self._cancelled = False

        self.init_ui()
        self.update_games()

    def init_ui(self):
        main_layout = QVBoxLayout()

        group = QGroupBox("Games")
        layout = QVBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search games...")
        self.search_box.textChanged.connect(self.filter_games)

        self.games_table = QTableWidget()
        self.games_table.setColumnCount(4)
        self.games_table.setHorizontalHeaderLabels(['Game', 'Path', 'Size', 'Last Save'])
        self.games_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        header = self.games_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        self.games_table.verticalHeader().setVisible(False)

        self.games_table.setColumnWidth(0, 200)
        self.games_table.setColumnWidth(1, 350)

        self.games_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.games_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.games_table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)

        layout.addWidget(self.search_box)
        layout.addWidget(self.games_table)
        group.setLayout(layout)
        main_layout.addWidget(group)
        self.setLayout(main_layout)

    def update_games(self):
        self.game_manager.update_locations(
            self.settings.user_location,
            self.settings.destination_location,
        )
        self._games = self.game_manager.get_installed_games()
        self.games_table.setRowCount(len(self._games))

        for row, game in enumerate(self._games):
            self.games_table.setItem(row, 0, QTableWidgetItem(game.name))
            self.games_table.setItem(row, 1, QTableWidgetItem(game.path))
            self.games_table.setItem(row, 2, QTableWidgetItem(GameManager.format_game_size(game)))
            self.games_table.setItem(row, 3, QTableWidgetItem(game.last_save))

    def collect_saves(self):
        self._run_operation(
            operation='collect',
            title='Confirm Backup',
            message=lambda count: f"Back up {count} selected game(s)?",
            progress_title='Backing Up Saves',
        )

    def spread_saves(self):
        self._run_operation(
            operation='spread',
            title='Confirm Restore',
            message=lambda count: f"Restore {count} selected game(s)? Existing save files may be overwritten.",
            progress_title='Restoring Saves',
        )

    def _run_operation(self, operation: str, title: str, message, progress_title: str) -> None:
        if self._worker is not None:
            QMessageBox.information(self, "Operation In Progress", "Please wait for the current operation to finish.")
            return

        selected_games = self.get_selected_games()
        if not selected_games:
            QMessageBox.warning(self, "No Selection", "Please select at least one game.")
            return

        reply = QMessageBox.question(
            self,
            title,
            message(len(selected_games)),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        self._cancelled = False
        self._progress_dialog = QProgressDialog(
            progress_title,
            "Cancel",
            0,
            len(selected_games),
            self,
        )
        self._progress_dialog.setWindowTitle("GameSaver")
        self._progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progress_dialog.setMinimumDuration(0)
        self._progress_dialog.setValue(0)
        self._progress_dialog.setAutoClose(False)
        self._progress_dialog.setAutoReset(False)
        self._progress_dialog.canceled.connect(self._cancel_operation)

        self._worker = OperationWorker(
            self.game_manager.backup_service,
            selected_games,
            operation,
        )
        self._worker.progress.connect(self._on_progress)
        self._worker.finished_report.connect(
            lambda report: self._on_finished(report, operation),
        )
        self._worker.start()

    def _cancel_operation(self) -> None:
        self._cancelled = True
        if self._worker is not None and self._worker.isRunning():
            self._worker.requestInterruption()

    def _on_progress(self, current: int, total: int, game_name: str) -> None:
        if self._progress_dialog is None:
            return
        self._progress_dialog.setMaximum(total)
        self._progress_dialog.setValue(current)
        self._progress_dialog.setLabelText(f"Processing {game_name} ({current}/{total})...")

    def _on_finished(self, report: BackupReport, operation: str) -> None:
        if self._progress_dialog is not None:
            self._progress_dialog.close()
            self._progress_dialog = None

        self._worker = None
        self.update_games()
        self._show_report(report, operation)

    def _show_report(self, report: BackupReport, operation: str) -> None:
        action = "backup" if operation == 'collect' else "restore"
        cancelled = [result for result in report.failures if result.message == "Cancelled by user"]
        prefix = "cancelled" if self._cancelled or cancelled else "completed"
        lines = [
            f"{action.title()} {prefix}: {len(report.successes)} succeeded, {len(report.failures)} failed.",
        ]

        if report.failures:
            lines.append("")
            lines.append("Failures:")
            for result in report.failures[:5]:
                lines.append(f"- {result.game_name}: {result.message}")
            if len(report.failures) > 5:
                lines.append(f"- ... and {len(report.failures) - 5} more")

        icon = QMessageBox.Icon.Information
        if self._cancelled or cancelled:
            icon = QMessageBox.Icon.Warning
        elif report.failures and not report.successes:
            icon = QMessageBox.Icon.Critical
        elif report.failures:
            icon = QMessageBox.Icon.Warning

        message_box = QMessageBox(self)
        message_box.setWindowTitle("GameSaver")
        message_box.setIcon(icon)
        message_box.setText("\n".join(lines))
        message_box.exec()

    def get_selected_games(self) -> list[GameEntry]:
        selected_rows = {
            index.row()
            for index in self.games_table.selectionModel().selectedRows()
        }
        selected_games = []
        for row in sorted(selected_rows):
            if self.games_table.isRowHidden(row):
                continue
            if 0 <= row < len(self._games):
                selected_games.append(self._games[row])
        return selected_games

    def filter_games(self):
        search_text = self.search_box.text().lower()
        for row in range(self.games_table.rowCount()):
            game_name = self.games_table.item(row, 0).text().lower()
            self.games_table.setRowHidden(row, search_text not in game_name)
