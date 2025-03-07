from typing import List, Dict
import os
import json
from constants import GAMES_PATH, SETTINGS_PATH, QUIT_OPTIONS, START_TEXT
from file_handler import load_json
from settings import Settings

class GameSaver:
    def __init__(self):
        self.settings = {}
        self.games = []
    
    def run(self) -> None:
        """Main execution flow of the GameSaver"""
        self.create_default_files()
        # print(START_TEXT)
        self.set_settings()
        # self.execute_selected_mode()
        # print(os.path.join())
    
    def execute_selected_mode(self) -> None:
        """Execute the selected operation mode"""
        if self.mode == 'collect' or '':
            self.collect()
        else:
            self.spread()
    
    def set_mode(self) -> str:
        """Get operation mode from user input"""
        while True:
            print('\nSelect mode: (collect/spread)')
            selected_mode = input('mode: ').lower().strip()
            if selected_mode in ['collect', 'spread']:
                return selected_mode
            print('Invalid mode! Please choose either "collect" or "spread"')
    
    def set_settings(self) -> None:
        """Set up user and destination locations as well as mode"""
        self.settings = load_json(SETTINGS_PATH)
        self._prompt_missing_settings()
    
    def collect(self) -> None:
        """Collect game saves from user location"""
        all_games = self._load_all_games()
        found_games = self._find_existing_games(all_games)
        
        if not self._confirm_save_operation(found_games):
            return
            
            # IMPLEMENTAR LÓGICA COLLECT
        self._copy_game_saves(found_games)
    
    def spread(self) -> None:
        """Spread saved games to user location"""
        print("We're still working on it... See you soon!\n")
    
    def _prompt_missing_settings(self) -> None:
        """Prompt user for missing settings"""
        while True:
            if not self.user_location:
                self._prompt_setting('user')
            if not self.destination_location:
                self._prompt_setting('destination')
            if not self.mode:
                self._prompt_setting('mode')
            error_message = self.verify_settings()
            if error_message:
                for error in error_message:
                    print(error)
            else:
                return
    
    def _prompt_setting(self, setting: str) -> None:
        """Prompt user for a specific setting"""
        if not setting == 'mode':
            print(f'! - {setting.title()} folder is not defined, please add it here: (q to quit)')
            choice = input(f'{setting.upper()}_LOCATION: ')
            if choice not in QUIT_OPTIONS:
                setattr(self, f'{setting}_location', choice)
        else:
            print(f'! - {setting.title()} is not defined, please add it here: (q to quit)')
            choice = input(f'{setting.upper()}: ')
            if choice not in QUIT_OPTIONS:
                setattr(self, 'mode', choice)
    
    def verify_settings(self) -> None:
        error_message = []
        
        if not os.path.exists(self.user_location):
            error_message.append(f'user_location does not exist, please verify if it\'s right. ({self.user_location})')
        if not os.path.exists(self.destination_location):
            error_message.append(f'destination_location does not exist, please verify if it\'s right. ({self.destination_location})')
        if self.mode not in ['collect', 'spread', '']:
            error_message.append(f'mode {self.mode} does not exist. Please choose either "collect" or "spread".')

if __name__ == '__main__':
    game_saver = GameSaver()
    game_saver.run()
