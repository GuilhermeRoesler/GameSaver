import os
import sys

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PACKAGE_DIR)

# Paths
BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else PROJECT_ROOT
DATABASE_PATH = (
    os.path.join(sys._MEIPASS, 'games_database.json')
    if hasattr(sys, '_MEIPASS')
    else os.path.join(PROJECT_ROOT, 'games_database.json')
)
STYLES_PATH = (
    os.path.join(sys._MEIPASS, 'gamesaver', 'gui', 'styles.qss')
    if hasattr(sys, '_MEIPASS')
    else os.path.join(PACKAGE_DIR, 'gui', 'styles.qss')
)
ICON_PATH = (
    os.path.join(sys._MEIPASS, 'images', 'icon.png')
    if hasattr(sys, '_MEIPASS')
    else os.path.join(PROJECT_ROOT, 'images', 'icon.png')
)

GAMES_PATH = os.path.join(BASE_DIR, 'games.json')
SETTINGS_PATH = os.path.join(BASE_DIR, 'settings.json')
SAVES_PATH = os.path.join(BASE_DIR, 'SAVES')

USER_DEFAULT_PATH = os.path.expanduser('~').replace('\\', '/')
DESTINATION_DEFAULT_PATH = SAVES_PATH.replace('\\', '/')
DEFAULT_MODE = 'collect'

# Valid inputs
QUIT_OPTIONS = ['q', 'quit', 'Q', 'Quit', '', ' ']

# Default files
DEFAULT_SETTINGS = {
    "user_location": USER_DEFAULT_PATH,
    "destination_location": DESTINATION_DEFAULT_PATH,
    "mode": DEFAULT_MODE,
}
DEFAULT_GAMES = [
    {
        "game": "Game Name",
        "path": "AppData/Roaming/YourGame",
        "last_save": "",
    },
    {
        "game": "Game Name 2",
        "path": "Documents/My Games/YourGame",
        "last_save": "",
    },
    {
        "game": "Minecraft",
        "path": "AppData/Roaming/.minecraft/versions",
        "last_save": "",
    },
]
