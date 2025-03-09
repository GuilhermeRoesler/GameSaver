import os
from constants import SETTINGS_PATH, USER_DEFAULT_PATH
from file_handler import load_json
from utils import printc, colored_multi

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
        self.check()
    
    def check(self) -> None:
        while True:
            untouched = 0
            if not self.user_location:
                self._prompt_setting(setting='user_location', error_type='blank')
                untouched+=1
            if not self.destination_location:
                self._prompt_setting(setting='destination_location', error_type='blank')
                untouched+=1
            if not self.mode:
                self._prompt_setting(setting='mode', error_type='blank')
                untouched+=1
            if not os.path.exists(self.user_location):
                self._prompt_setting(setting='user_location', error_type='wrong')
                untouched+=1
            if not os.path.exists(self.destination_location):
                self._prompt_setting(setting='destination_location', error_type='wrong')
                untouched+=1
            if self.mode not in ['collect', 'spread', '']:
                self._prompt_setting(setting='mode', error_type='wrong')
                untouched+=1
            if untouched == 0:
                return
    
    def _prompt_setting(self, setting: str, error_type: str) -> None:
        # Prompt user for a specific setting
        if error_type == 'blank':
            print(f'{setting.upper()} is blank, please, fill it up:')
            setattr(self, setting, input(f'{setting.upper()}: '))
        elif error_type == 'wrong':
            if setting == 'mode':
                print(f'SELECT mode does not exist. Please choose either "collect" or "spread".')
                setattr(self, setting, input(f'{setting.upper()}: '))
            else:
                print(f'{setting.upper()} path does not exist. Please, verify if that\'s right')
                setattr(self, setting, input(f'{setting.upper()}: '))
    
    # Ask for user if default is good
    def print(self) -> None:
        printc('cyan', '\nCurrent Settings:')
        print(f'{"─" * 40}')
        
        colors = ['yellow', 'cyan']
        self.user_location = input(colored_multi(colors, ['User location ', f'[{self.user_location}]: '])).strip() or self.user_location
        self.destination_location = input(colored_multi(colors, ['Destination location ', f'[{self.destination_location}]: '])).strip() or self.destination_location
        self.mode = input(colored_multi(colors, ['Mode ', f'[{self.mode}]: '])).strip() or self.mode
        
        print(f'{"─" * 40}')
        self.check()


# def check(self) -> None:
#     required_settings = {
#         'user_location': self.user_location,
#         'destination_location': self.destination_location,
#         'mode': self.mode
#     }
    
#     errors = {
#         'blank': lambda key: not required_settings[key],
#         'wrong_path': lambda key: key in ['user_location', 'destination_location'] and not os.path.exists(required_settings[key]),
#         'wrong_mode': lambda key: key == 'mode' and required_settings[key] not in ['collect', 'spread', '']
#     }
    
#     for setting, value in required_settings.items():
#         for error_type, condition in errors.items():
#             if condition(setting):
#                 self._prompt_setting(setting=setting, error_type=error_type)
#                 break
