import argparse
import logging
import sys

from PyQt6.QtWidgets import QApplication

from .cli_messages import FINAL_TEXT, START_TEXT
from .constants import STYLES_PATH
from .file_handler import create_default_files
from .game_manager import GameManager
from .gui.main_window import GameSaverWindow
from .gui.window_icon import apply_native_window_icon, load_app_icon, resolve_icon_path
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


def configure_windows_app_id() -> None:
    """Give Windows a distinct AppUserModelID so the taskbar shows our icon, not python.exe."""
    if sys.platform != 'win32':
        return
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('GameSaver.Desktop.1')
    except (AttributeError, OSError):
        pass


def run_gui() -> None:
    configure_windows_app_id()
    app = QApplication(sys.argv)
    app.setApplicationName('GameSaver')
    app.setApplicationDisplayName('GameSaver')
    icon = load_app_icon()
    if not icon.isNull():
        app.setWindowIcon(icon)
    app.setStyleSheet(load_stylesheet(STYLES_PATH))
    window = GameSaverWindow()
    if not icon.isNull():
        window.setWindowIcon(icon)
    window.show()
    # Ensure both Qt's QWindow and the native Win32 icons are set for the taskbar.
    handle = window.windowHandle()
    if handle is not None and not icon.isNull():
        handle.setIcon(icon)
    apply_native_window_icon(window, resolve_icon_path())
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
