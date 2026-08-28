from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from file_handler import create_default_files
from game_manager import GameManager
from settings import Settings
from .settings_widget import SettingsWidget
from .game_list_widget import GameListWidget


class GameSaverWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GameSaver")
        self.setMinimumSize(800, 600)
        self.resize(800, 800)

        create_default_files()

        self.settings = Settings()
        self.game_manager = GameManager(
            self.settings.user_location,
            self.settings.destination_location,
        )

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        header = QLabel("GameSaver")
        header.setObjectName("header")
        header.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        self.settings_widget = SettingsWidget(self.settings)
        layout.addWidget(self.settings_widget)

        self.games_widget = GameListWidget(self.settings, self.game_manager)
        layout.addWidget(self.games_widget)

        self.settings_widget.locations_changed.connect(self.update_games_list)

        buttons_layout = QHBoxLayout()
        collect_btn = QPushButton("Collect Saves")
        collect_btn.clicked.connect(self.games_widget.collect_saves)
        spread_btn = QPushButton("Spread Saves")
        spread_btn.clicked.connect(self.spread_saves)

        buttons_layout.addWidget(collect_btn)
        buttons_layout.addWidget(spread_btn)
        layout.addLayout(buttons_layout)

    def update_games_list(self):
        self.game_manager.update_locations(
            self.settings.user_location,
            self.settings.destination_location,
        )
        self.games_widget.update_games()

    def spread_saves(self):
        self.games_widget.spread_saves()
