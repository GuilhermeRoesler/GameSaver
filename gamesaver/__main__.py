import argparse
import os
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from .constants import FINAL_TEXT, ICON_PATH, START_TEXT, STYLES_PATH
from .file_handler import create_default_files
from .game_manager import GameManager
from .gui.main_window import GameSaverWindow
from .settings import Settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Backup and restore local game save files.')
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Run in command-line mode instead of the graphical interface.',
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

    print(FINAL_TEXT)
    input('Press Enter to exit...')


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.cli:
        run_cli()
    else:
        run_gui()


if __name__ == '__main__':
    main()
