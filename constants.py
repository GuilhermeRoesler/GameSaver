import os
import sys
from utils import colored

# Paths
BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
GAMES_PATH = os.path.join(BASE_DIR, 'games.json')
SETTINGS_PATH = os.path.join(BASE_DIR, 'settings.json')
DATABASE_PATH = os.path.join(sys._MEIPASS, 'games_database.json') if hasattr(sys, '_MEIPASS') else 'games_database.json'
USER_DEFAULT_PATH = os.path.expanduser('~')
DEFAULT_MODE = 'collect'

# Valid inputs
QUIT_OPTIONS = ['q', 'quit', 'Q', 'Quit', '', ' ']

# Default
DEFAULT_SETTINGS = {
    "user_location": USER_DEFAULT_PATH,
    "destination_location": USER_DEFAULT_PATH,
    "mode": DEFAULT_MODE,
    "explanation": [
        {
            "important": "delete the explanation and leave only the first three values (user_location, destination_location and mode)",
            "user_location": "location of the Users folder, if it is not correct, you can correct it here",
            "destination_location": "folder where you want the saves to be saved. The SAVES folder will be created inside it",
            "mode": "choose between collect or spread. collect gets all the saves, spread spreads them to your computer"
        }
    ]
}
DEFAULT_GAMES = [
    {
        "game": "Game Name",
        "path": "\\AppData\\Roaming\\YourGame",
        "last_save": ""
    },
    {
        "game": "Game Name 2",
        "path": "\\Documents\\My Games\\YourGame",
        "last_save": "",
    },
    {
        "game": "Minecraft",
        "path": "\\AppData\\Roaming\\.minecraft\\versions",
        "last_save": "",
    }
]

START_TEXT = colored('cyan', '''
╔════════════════ GAME SAVER ════════════════╗
║                                            ║
║  Welcome to Game Saver!                    ║
║                                            ║
║  This tool helps you backup and restore    ║
║  your game save files across computers.    ║
║                                            ║
║  Setup Steps:                              ║
║  1. Add user_location, destination_location║
║  and mode in settings.json                 ║
║  2. Configure games inside games.json      ║
║  3. Enjoy and have fun!                    ║
║                                            ║
╚════════════════════════════════════════════╝
''')

FINAL_TEXT = colored('green', '''
╔═════════════════════════════════════╗
║  Operation completed successfully!  ║
╚═════════════════════════════════════╝
''')

# ! - If you have another user location (like another storage or something), you can configure it at settings.json.
# ! - If you want to customize destination folder, same, settings.json.
# ! - If your game does not appear at the found games list, add it at games.json.
# ! - Open JSON files with notepad ;)
