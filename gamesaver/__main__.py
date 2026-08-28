import argparse
import logging
import os
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from .cli_messages import FINAL_TEXT, START_TEXT
from .constants import ICON_PATH, STYLES_PATH
from .file_handler import create_default_files
from .game_manager import GameManager
from .gui.main_window import GameSaverWindow
from .logging_config import configure_logging, get_logger
from .settings import Settings

logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Backup and restore local game save files.')
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Run in command-line mode instead of the graphical interface.',
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable debug logging.',
    )
    return parser


def load_stylesheet(file_path: str) -> str:
    with open(file_path, encoding='utf-8') as file:
        return file.read()


def run_gui() -> None:
    app = QApplication(sys.argv)
    if os.path.exists(ICON_PATH):
        app.setWindowIcon(QIcon(ICON_PATH))
    app.setStyleSheet(load_stylesheet(STYLES_PATH))
    window = GameSaverWindow()
    window.show()
    sys.exit(app.exec())


def run_cli() -> None:
    create_default_files()
    print(START_TEXT)

    settings = Settings()
    settings.load()
    game_manager = GameManager(settings.user_location, settings.destination_location)

    settings.print()
    if settings.mode in ['collect', '']:
        game_manager.collect()
    elif settings.mode == 'spread':
        game_manager.spread()
    else:
        logger.error('Unknown mode: %s', settings.mode)

    print(FINAL_TEXT)
    input('Press Enter to exit...')


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    configure_logging(logging.DEBUG if args.verbose else logging.INFO)
    if args.cli:
        run_cli()
    else:
        run_gui()


if __name__ == '__main__':
    main()
