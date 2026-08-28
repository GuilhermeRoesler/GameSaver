import os

from constants import USER_DEFAULT_PATH, DESTINATION_DEFAULT_PATH
from models import AppSettings
from repositories import SettingsRepository
from utils import printc, colored_multi


class Settings:
    def __init__(self):
        self._repository = SettingsRepository()
        self._data = AppSettings(
            user_location=USER_DEFAULT_PATH,
            destination_location=DESTINATION_DEFAULT_PATH,
            mode='collect',
        )
        self.load()

    @property
    def user_location(self) -> str:
        return self._data.user_location

    @user_location.setter
    def user_location(self, value: str) -> None:
        self._data.user_location = value

    @property
    def destination_location(self) -> str:
        return self._data.destination_location

    @destination_location.setter
    def destination_location(self, value: str) -> None:
        self._data.destination_location = value

    @property
    def mode(self) -> str:
        return self._data.mode

    @mode.setter
    def mode(self, value: str) -> None:
        self._data.mode = value

    def load(self) -> None:
        self._data = self._repository.load()
        self.check()

    def save(self) -> None:
        self._repository.save(self._data)

    def to_dict(self) -> dict:
        return self._data.to_dict()

    def check(self) -> None:
        while True:
            untouched = 0
            if not self.user_location:
                self._prompt_setting(setting='user_location', error_type='blank')
                untouched += 1
            if not self.destination_location:
                self._prompt_setting(setting='destination_location', error_type='blank')
                untouched += 1
            if not self.mode:
                self._prompt_setting(setting='mode', error_type='blank')
                untouched += 1
            if not os.path.exists(self.user_location):
                self._prompt_setting(setting='user_location', error_type='wrong')
                untouched += 1
            if not os.path.exists(self.destination_location):
                self._prompt_setting(setting='destination_location', error_type='wrong')
                untouched += 1
            if self.mode not in ['collect', 'spread', '']:
                self._prompt_setting(setting='mode', error_type='wrong')
                untouched += 1
            if untouched == 0:
                return

    def _prompt_setting(self, setting: str, error_type: str) -> None:
        if error_type == 'blank':
            print(f'{setting.upper()} is blank, please, fill it up:')
            setattr(self, setting, input(f'{setting.upper()}: '))
        elif error_type == 'wrong':
            if setting == 'mode':
                print('SELECT mode does not exist. Please choose either "collect" or "spread".')
                setattr(self, setting, input(f'{setting.upper()}: '))
            else:
                print(f'{setting.upper()} path does not exist. Please, verify if that\'s right')
                setattr(self, setting, input(f'{setting.upper()}: '))

    def print(self) -> None:
        printc('cyan', '\nCurrent Settings:')
        print(f'{"─" * 40}')

        colors = ['yellow', 'cyan']
        self.user_location = input(colored_multi(colors, ['User location ', f'[{self.user_location}]: '])).strip() or self.user_location
        self.destination_location = input(colored_multi(colors, ['Destination location ', f'[{self.destination_location}]: '])).strip() or self.destination_location
        self.mode = input(colored_multi(colors, ['Mode ', f'[{self.mode}]: '])).strip() or self.mode

        print(f'{"─" * 40}')
        self.check()
        self.save()
