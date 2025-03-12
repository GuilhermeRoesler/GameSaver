from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, 
                            QLineEdit, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy)
from game_manager import GameManager

class GameListWidget(QWidget):
    def __init__(self, settings):
        super().__init__()
        
        self.settings = settings
        self.game_manager = GameManager()
        
        self.init_ui()
        self.update_games()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        group = QGroupBox("Games")
        layout = QVBoxLayout()
        
        # Search/filter
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search games...")
        self.search_box.textChanged.connect(self.filter_games)
        
        # Games table
        self.games_table = QTableWidget()
        self.games_table.setColumnCount(4)
        self.games_table.setHorizontalHeaderLabels(['Game', 'Path', 'Size', 'Last Save'])
        self.games_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Make columns interactive and resizable
        header = self.games_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)  # Game name column
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)      # Save location column
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)      # Size column
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)  # Last save column
        self.games_table.verticalHeader().setVisible(False) # Hides vertical header
        
        # Set minimum column widths
        self.games_table.setColumnWidth(0, 200)  # Game name
        self.games_table.setColumnWidth(1, 350)  # Save location
        
        # Prevent editable and add selection
        self.games_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.games_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.games_table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)
        
        layout.addWidget(self.search_box)
        layout.addWidget(self.games_table)
        group.setLayout(layout)
        main_layout.addWidget(group)
        self.setLayout(main_layout)
    
    def update_games(self):
        self.game_manager.update_locations(self.settings.user_location, self.settings.destination_location)
        games = self.game_manager.get_installed_games()
        self.games_table.setRowCount(len(games))
        
        for row, game in enumerate(games):
            self.games_table.setItem(row, 0, QTableWidgetItem(game['game']))
            self.games_table.setItem(row, 1, QTableWidgetItem(game['path']))
            self.games_table.setItem(row, 2, QTableWidgetItem('0 Kb'))
            self.games_table.setItem(row, 3, QTableWidgetItem(game['last_save']))
    
    def collect_saves(self):
        selected_games = self.get_selected_games()
        self.game_manager.copy_selected_games(selected_games)
    
    def get_selected_games(self):
        selected_rows = self.games_table.selectedItems()
        selected_games = []
        for row in range(self.games_table.rowCount()):
            if self.games_table.item(row, 0).isSelected():
                selected_games.append({
                    'game': self.games_table.item(row, 0).text(),
                    'path': self.games_table.item(row, 1).text(),
                    'last_save': self.games_table.item(row, 3).text()
                })
        return selected_games
    
    def filter_games(self):
        search_text = self.search_box.text().lower()
        for row in range(self.games_table.rowCount()):
            game_name = self.games_table.item(row, 0).text().lower()
            self.games_table.setRowHidden(row, search_text not in game_name)
