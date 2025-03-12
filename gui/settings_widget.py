from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                            QPushButton, QLabel, QComboBox, QGroupBox, QFileDialog)
from PyQt6.QtCore import pyqtSignal

class SettingsWidget(QWidget):
    locations_changed = pyqtSignal()
    
    def __init__(self, settings):
        super().__init__()
        
        self.settings = settings
        
        self.init_ui()
    
    def init_ui(self):
        # Create main layout for the widget
        main_layout = QVBoxLayout()
        
        # Create and setup the group
        group = QGroupBox("Settings")
        layout = QVBoxLayout()
        
        # User location
        user_layout = QHBoxLayout()
        self.user_location = QLineEdit(self.settings.user_location)
        browse_user = QPushButton("Browse")
        browse_user.clicked.connect(lambda: self.browse_folder(self.user_location))
        user_layout.addWidget(QLabel("User Location:"))
        user_layout.addWidget(self.user_location)
        user_layout.addWidget(browse_user)
        
        # Destination location
        dest_layout = QHBoxLayout()
        self.dest_location = QLineEdit(self.settings.destination_location)
        browse_dest = QPushButton("Browse")
        browse_dest.clicked.connect(lambda: self.browse_folder(self.dest_location))
        dest_layout.addWidget(QLabel("Destination:"))
        dest_layout.addWidget(self.dest_location)
        dest_layout.addWidget(browse_dest)
        
        layout.addLayout(user_layout)
        layout.addLayout(dest_layout)
        
        group.setLayout(layout)
        main_layout.addWidget(group)
        
        self.setLayout(main_layout)
        
    def browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            line_edit.setText(folder)
            self.settings.user_location = self.user_location.text()
            self.settings.destination_location = self.dest_location.text()
            self.locations_changed.emit()
