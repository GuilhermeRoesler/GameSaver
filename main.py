import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from gui.main_window import GameSaverWindow
from settings import Settings
from game_manager import GameManager
from file_handler import create_default_files
from constants import START_TEXT, FINAL_TEXT, STYLES_PATH

isGUI = True

def run() -> None:
    loadGUI() if isGUI else load()

def loadGUI():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('images/icon.png'))
    app.setStyleSheet(load_stylesheet('gui/styles.qss'))
    window = GameSaverWindow()
    window.show()
    sys.exit(app.exec())

def load():
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

def load_stylesheet(file_path):
    with open(STYLES_PATH, 'r') as file:
        return file.read()

if __name__ == '__main__':
    run()
