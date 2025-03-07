import os
import shutil
import json
import sys

# Locations to be copied and pasted
USER_LOCATION = r''
DST_LOCATION = r''

# Script directories
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GAMES_PATH = os.path.join(BASE_DIR, 'games.json')
SETTINGS_PATH = os.path.join(BASE_DIR, 'settings.json')

# collect/spread
mode = ''
user_games = ''
not_list = ['q', 'quit', 'Q', 'Quit', '', ' ']

start_text = '''
╔════════════════ GAME SAVER ════════════════╗
║                                            ║
║  Welcome to Game Saver!                    ║
║                                            ║
║  This tool helps you backup and restore    ║
║  your game save files across computers.    ║
║                                            ║
║  Setup Steps:                              ║
║  1. Add USER_LOCATION in saves.py          ║
║  2. Add DST_LOCATION in saves.py           ║
║  3. Configure games in games_database.json ║
║                                            ║
╚════════════════════════════════════════════╝
'''

# Create all necessary JSON files
def creating_default_files():
    # Verifying if games.json exists
    if os.path.exists(GAMES_PATH):
        print("games.json file loaded!")
    else:
        print("games.json file not found. Creating a default...")
        default_games = [
            {
                "game": "Game Name",
                "path": "\\AppData\\Roaming\\YourGame",
                "last_save": ""
            },
            {
                "game": "Game Name 2",
                "path": "\\Documents\\My Games\\YourGame",
                "last_save": "",
                "important!": "These are two examples, delete 'important!' line after this. Always use double backslash! Leave last_save empty! Separate games by a comma (,) between braces({})! The directory is given after User folder (C:\\Users\\youruser)!"
            }
        ]
        with open(GAMES_PATH, 'w', encoding='utf-8') as arquive:
            json.dump(default_games, arquive, indent=4)
    
    # Verifying if settings.json exists
    if os.path.exists(SETTINGS_PATH):
        print("settings.json file loaded!")
    else:
        print("settings.json file not found. Creating a default...")
        default_settings = {
            "user_location": "C:\\Users\\yourUser",
            "destination_location": "folder where you want the games to be (don't forget double backslash!)",
            "mode": ""
        }
        with open(SETTINGS_PATH, 'w', encoding='utf-8') as arquive:
            json.dump(default_settings, arquive, indent=4)

# Set up mode
def set_mode():
    if not mode:
        while True:
            print('\nSelect mode: (collect/spread)')
            selected_mode = input('mode: ').lower().strip()
            if selected_mode in ['collect', 'spread']:
                return selected_mode
            print('Invalid mode! Please choose either "collect" or "spread"')

# Set up locations
def set_locations():
    global USER_LOCATION
    global DST_LOCATION
    global mode
    
    if not USER_LOCATION and not DST_LOCATION:
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as arquive:
            content = json.load(arquive)
            USER_LOCATION = content['user_location']
            DST_LOCATION = content['destination_location']
            mode = content['mode']
    
    if not USER_LOCATION:
        print('! - User folder is not defined, define it in USER_LOCATION or add here: (q to quit)')
        choice = input('USER_LOCATION: ')
        if choice not in not_list:
            USER_LOCATION = choice
    if not DST_LOCATION:
        print('! - Destination folder is not defined, define it in DST_LOCATION or add here: (q to quit)')
        choice = input('DST_LOCATION: ')
        if choice not in not_list:
            DST_LOCATION = choice

# Read database
def get_game_info():
    with open('./games_database.json', 'r', encoding='utf-8') as arquive:
        data = json.load(arquive)
        return data

# Read user customizable database
def get_extra_games():
    with open(GAMES_PATH, 'r', encoding='utf-8') as arquive:
        data = json.load(arquive)
        return data

# Search for user games
def search_games(games):
    global user_games
    
    game = games[0]
    
    # for game in games:
    #     print(f'{game['game']}: {os.path.exists(os.path.join(USER_LOCATION, game['path']))} ({os.path.join(USER_LOCATION, game['path'])})')

# Save all configured games into specified location
def save():
    game_info = get_game_info()
    extra_games = get_extra_games()
    
    all_games = game_info + extra_games
    search_games(all_games)
    
    print('\nThe following games will be saved:')
    # print(*(f'- {game['game']}' for game in all_games), sep='\n')
    if input('Do you want to continue? (y/n): ') == 'y':
        pass
    else:
        print('Closing operation. See you soon, folks!\n')
        return
    
    for game in game_info:
        print(f'- Copying {game['game']}...')
        
        if not game['path']:
            print(f'Skipping {game['game']} because the path is empty.')
            print('Please, fill up the path at games_database.json!')
            continue
        
        location = USER_LOCATION + game['path']
        destine = os.path.join(DST_LOCATION, 'SAVES', os.path.basename(location))
        
        shutil.copytree(location, destine, dirs_exist_ok=True)
        
        print(f'{os.path.basename(location)} folder copied to {destine}')

# Spread all saves to respective game location
def spread():
    print("We're still working on it... See you soon!\n")

# main
def main():
    creating_default_files()
    print(start_text)
    mode = set_mode()
    set_locations()
    save() if mode == 'collect' else spread()

# first, select the mode: (collect/spread)
# user folder is not defined, define it in USER_LOCATION or add here: (q to quit)
# destination folder is not defined, define it in DST_LOCATION or add here: (q to quit)
# the following games will be saved:
# do you want to continue? (y/n)

# print(*(game['game'] for game in ler()), sep='\n')

if __name__ == '__main__':
    main()
