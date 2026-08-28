from typing import Any, Sequence

from .backup_service import BackupService
from .constants import USER_DEFAULT_PATH, DESTINATION_DEFAULT_PATH
from .file_utils import format_size
from .models import GameEntry
from .repositories import GameRepository
from .utils import printc


class GameManager:
    def __init__(
        self,
        user_location: str | None = None,
        destination_location: str | None = None,
    ):
        self._repository = GameRepository()
        self._service = BackupService(
            user_location or USER_DEFAULT_PATH,
            destination_location or DESTINATION_DEFAULT_PATH,
        )
        self.all_games = self._repository.load_all()
        self.installed_games = self._service.get_installed_games(self.all_games)

    @property
    def user_location(self) -> str:
        return self._service.user_location

    @property
    def destination_location(self) -> str:
        return self._service.destination_location

    @property
    def backup_service(self) -> BackupService:
        return self._service

    def collect(self) -> None:
        printc('green', '\nFound Games:')
        for game in self.installed_games:
            printc('cyan', f'➜  {game.name}')
        printc('yellow', f'\nTotal games found: {len(self.installed_games)}')

        if not self.confirm_save_operation():
            return

        self.copy_installed_games()

    def spread(self) -> None:
        printc('green', '\nInstalled games available for restore:')
        for game in self.installed_games:
            printc('cyan', f'➜  {game.name}')
        printc('yellow', f'\nTotal games found: {len(self.installed_games)}')

        if not self.confirm_save_operation():
            return

        self._print_report(self._service.spread_games(self.installed_games))

    def copy_installed_games(self) -> None:
        self.copy_selected_games(self.installed_games)

    def copy_selected_games(self, games: Sequence[GameEntry | dict[str, Any]]) -> None:
        entries = [self._as_game_entry(game) for game in games]
        if not entries:
            printc('yellow', 'No games selected for backup.')
            return

        printc('green', '\nStarting backup process...\n')
        report = self._service.collect_games(entries)
        self._print_report(report)

    def spread_selected_games(self, games: Sequence[GameEntry | dict[str, Any]]) -> None:
        entries = [self._as_game_entry(game) for game in games]
        if not entries:
            printc('yellow', 'No games selected for restore.')
            return

        printc('green', '\nStarting restore process...\n')
        report = self._service.spread_games(entries)
        self._print_report(report)

    def get_installed_games(self) -> list[GameEntry]:
        self.installed_games = self._service.get_installed_games(self.all_games)
        return self.installed_games

    def confirm_save_operation(self) -> bool:
        response = input('Do you want to proceed? (y/n): ').lower().strip()
        return response in ['y', 'yes', '']

    def update_locations(self, user_location: str, destination_location: str) -> None:
        self._service.update_locations(user_location, destination_location)
        self.installed_games = self.get_installed_games()

    def _print_report(self, report) -> None:
        for result in report.results:
            if result.success:
                printc('green', f'✓ {result.game_name}: {result.message}')
            else:
                printc('red', f'⚠ {result.game_name}: {result.message}')

        printc(
            'yellow',
            f'\nCompleted: {len(report.successes)} succeeded, {len(report.failures)} failed.',
        )

    @staticmethod
    def _as_game_entry(game: GameEntry | dict[str, Any]) -> GameEntry:
        if isinstance(game, GameEntry):
            return game
        return GameEntry.from_dict(game)

    @staticmethod
    def format_game_size(game: GameEntry) -> str:
        return format_size(game.size)
