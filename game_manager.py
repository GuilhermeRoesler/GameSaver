import os
from typing import List, Dict
from file_handler import load_json, copy_game_save
from constants import GAMES_PATH, DATABASE_PATH

class GameManager:
    def __init__(self, user_location: str, destination_location: str):
        self.user_location = user_location
        self.destination_location = destination_location
        self.database_games = load_json(DATABASE_PATH)
        self.extra_games = load_json(GAMES_PATH)
        self.all_games = self.database_games + self.extra_games
        self.installed_games = self.find_installed_games(self.all_games)
    
    # Collect game saves from user location
    def collect(self) -> None:
        print('The following games were found:')
        print(*(f'- {game['game']}' for game in self.installed_games), sep='\n')
        
        if not self.confirm_save_operation():
            return
        
        self.copy_games()
    
    def copy_games(self) -> None:
        for game in self.installed_games:
            print(f'- Copying {game['game']}...')
            
            game_location = os.path.join(self.user_location, game['path'])
            game_destination = os.path.join(self.destination_location, 'SAVES', os.path.basename(game_location))
            
            if not game['path']:
                print(f'Skipping {game['game']} because the path is empty.')
                print('Please, fill up the path at games_database.json!')
                continue
            
            copy_game_save(game_location, game_destination)
            print(f'{os.path.basename(game_location)} folder copied to {game_destination}')
    
    def spread(self) -> None:
        # Spread saved games to user computer
        print("We're still working on it... See you soon!")
    
    def find_installed_games(self, game_list: List[Dict]) -> List[Dict]:
        found_games = []
        for game in game_list:
            full_path = os.path.join(self.user_location, game['path'])
            if os.path.exists(full_path):
                found_games.append(game)
        return found_games
    
    def get_save_destination(self, game: Dict) -> str:
        game_folder = os.path.basename(game['path'])
        return os.path.join(self.destination_location, 'SAVES', game_folder)
    
    def confirm_save_operation(self) -> bool:
        response = input('Do you want to proceed? (y/n): ').lower().strip()
        return response in ['y', 'yes', '']
