from settings import Settings
from game_manager import GameManager
from file_handler import create_default_files
from constants import START_TEXT, FINAL_TEXT
from utils import colored_multi

def run() -> None:
    # Create games.json and settings.json for user interaction.
    create_default_files()
    
    # Start
    print(START_TEXT)
    
    # Initializa objects and variables
    settings = Settings()
    settings.load()
    game_manager = GameManager(settings.user_location, settings.destination_location)
    
    settings.print()
    if settings.mode in ['collect', '']:
        game_manager.collect()
    elif settings.mode == 'spread':
        game_manager.spread()
    
    # wait for user to read all terminal and finish it. Cancel automatic close
    print(FINAL_TEXT)
    input('Press Enter to exit...')

if __name__ == '__main__':
    run()
