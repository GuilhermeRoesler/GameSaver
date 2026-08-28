from PyQt6.QtCore import QThread, pyqtSignal

from ..backup_service import BackupService
from ..models import BackupReport, GameEntry, OperationResult


class OperationWorker(QThread):
    progress = pyqtSignal(int, int, str)
    finished_report = pyqtSignal(object)

    def __init__(
        self,
        service: BackupService,
        games: list[GameEntry],
        operation: str,
    ):
        super().__init__()
        self.service = service
        self.games = games
        self.operation = operation

    def run(self) -> None:
        results: list[OperationResult] = []
        total = len(self.games)

        for index, game in enumerate(self.games, start=1):
            if self.isInterruptionRequested():
                results.extend(self._cancelled_results(self.games[index - 1 :]))
                break

            self.progress.emit(index, total, game.name)
            if self.operation == 'collect':
                results.append(self.service.collect_game(game))
            else:
                results.append(self.service.spread_game(game))

            if self.isInterruptionRequested():
                remaining = self.games[index:]
                if remaining:
                    results.extend(self._cancelled_results(remaining))
                break

        self.finished_report.emit(BackupReport(results=results))

    @staticmethod
    def _cancelled_results(games: list[GameEntry]) -> list[OperationResult]:
        return [
            OperationResult(
                game_name=game.name,
                success=False,
                message="Cancelled by user",
            )
            for game in games
        ]
