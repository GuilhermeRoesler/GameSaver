import os
from typing import List, Dict
from file_handler import load_json, copy_game_save
from constants import GAMES_PATH, DATABASE_PATH, USER_DEFAULT_PATH, DESTINATION_DEFAULT_PATH
from utils import printc

class GameManager:
    def __init__(self):
        self.user_location = USER_DEFAULT_PATH
        self.destination_location = DESTINATION_DEFAULT_PATH
        self.database_games = load_json(DATABASE_PATH)
        self.extra_games = load_json(GAMES_PATH)
        self.all_games = self.database_games + self.extra_games
        self.installed_games = self.get_installed_games()
    
    # Collect game saves from user location
    def collect(self) -> None:
        printc('green', '\nFound Games:')
        for game in self.installed_games:
            printc('cyan', f'➜  {game["game"]}')
        printc('yellow', f'\nTotal games found: {len(self.installed_games)}')
        
        if not self.confirm_save_operation():
            return
        
        self.copy_installed_games()
    
    def spread(self) -> None:
        # Spread saved games to user computer
        print("We're still working on it... See you soon!")
    
    def copy_installed_games(self) -> None:
        self.copy_selected_games(self.installed_games)
    
    def copy_selected_games(self, games):
        printc('green', '\nStarting backup process...\n')
        for game in games:
            printc('cyan', f'Backing up {game["game"]}...')
            
            game_location = os.path.join(self.user_location, game['path'])
            game_destination = os.path.join(self.destination_location, os.path.basename(game_location))
            
            if not game['path']:
                printc('red', f'⚠ Skipping {game["game"]} - Missing path configuration')
                continue
            
            copy_game_save(game_location, game_destination)
            printc('green', f'✓ Successfully backed up {game["game"]} into {game_destination}')
    
    def get_installed_games(self) -> List[Dict]:
        game_list = self.all_games
        found_games = []
        for game in game_list:
            full_path = os.path.join(self.user_location, game['path'])
            if os.path.exists(full_path):
                found_games.append(game)
        self.installed_games = found_games
        return found_games
    
    def get_save_destination(self, game: Dict) -> str:
        game_folder = os.path.basename(game['path'])
        return os.path.join(self.destination_location, 'SAVES', game_folder)
    
    def confirm_save_operation(self) -> bool:
        response = input('Do you want to proceed? (y/n): ').lower().strip()
        return response in ['y', 'yes', '']
    
    def update_locations(self, user_location, destination_location):
        self.user_location = user_location
        self.destination_location = destination_location
        self.installed_games = self.get_installed_games()
