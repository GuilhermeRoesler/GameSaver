from .utils import colored

START_TEXT = colored('cyan', '''
╔══════════════════ GAME SAVER ══════════════════╗
║                                                ║
║  Welcome to Game Saver!                        ║
║                                                ║
║  This tool helps you backup and restore        ║
║  your game save files across computers.        ║
║                                                ║
║  Setup Steps:                                  ║
║  1. Add user_location, destination_location    ║
║  and mode in settings.json                     ║
║  2. Configure games inside games.json          ║
║  3. Read full documentation at                 ║
║  https://github.com/GuilhermeRoesler/GameSaver ║
║  4. Enjoy and have fun!                        ║
║                                                ║
╚════════════════════════════════════════════════╝
''')

FINAL_TEXT = colored('green', '''
╔═════════════════════════════════════╗
║  Operation completed successfully!  ║
╚═════════════════════════════════════╝
''')
