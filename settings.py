from typing import Dict
from constants import SETTINGS_PATH, USER_DEFAULT_PATH
from file_handler import load_json, save_json

class Settings:
    def __init__(self):
        self.user_location = USER_DEFAULT_PATH
        self.destination_location = USER_DEFAULT_PATH
        self.mode = 'collect'
    
    def load(self) -> None:
        settings = load_json(SETTINGS_PATH)
        self.user_location = settings['user_location']
        self.destination_location = settings['destination_location']
        self.mode = settings['mode']
        # VERIFICAR SE NÃO É O PADRÃO NO JSON
    
    def save(self) -> None:
        settings = {
            'user_location': self.user_location,
            'destination_location': self.destination_location,
            'mode': self.mode
        }
        save_json(SETTINGS_PATH, settings)
    
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