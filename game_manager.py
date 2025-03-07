from typing import List, Dict
import os

class GameManager:
    def __init__(self, user_location: str, destination_location: str):
        self.user_location = user_location
        self.destination_location = destination_location
        self.games = []
    
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