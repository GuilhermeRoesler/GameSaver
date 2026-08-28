from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QGroupBox,
    QFileDialog,
    QComboBox,
)
from PyQt6.QtCore import pyqtSignal


class SettingsWidget(QWidget):
    locations_changed = pyqtSignal()

    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        group = QGroupBox("Settings")
        layout = QVBoxLayout()

        user_layout = QHBoxLayout()
        self.user_location = QLineEdit(self.settings.user_location)
        self.user_location.editingFinished.connect(self._apply_settings)
        browse_user = QPushButton("Browse")
        browse_user.setObjectName("browse_user")
        browse_user.clicked.connect(lambda: self.browse_folder(self.user_location))
        user_layout.addWidget(QLabel("User Location:"))
        user_layout.addWidget(self.user_location)
        user_layout.addWidget(browse_user)

        dest_layout = QHBoxLayout()
        self.dest_location = QLineEdit(self.settings.destination_location)
        self.dest_location.editingFinished.connect(self._apply_settings)
        browse_dest = QPushButton("Browse")
        browse_dest.setObjectName("browse_dest")
        browse_dest.clicked.connect(lambda: self.browse_folder(self.dest_location))
        dest_layout.addWidget(QLabel("Destination:"))
        dest_layout.addWidget(self.dest_location)
        dest_layout.addWidget(browse_dest)

        mode_layout = QHBoxLayout()
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Collect (backup)", "collect")
        self.mode_combo.addItem("Spread (restore)", "spread")
        current_mode = self.settings.mode if self.settings.mode in {"collect", "spread"} else "collect"
        index = self.mode_combo.findData(current_mode)
        self.mode_combo.setCurrentIndex(index if index >= 0 else 0)
        self.mode_combo.currentIndexChanged.connect(self._apply_settings)
        mode_layout.addWidget(QLabel("Mode:"))
        mode_layout.addWidget(self.mode_combo)

        layout.addLayout(user_layout)
        layout.addLayout(dest_layout)
        layout.addLayout(mode_layout)

        group.setLayout(layout)
        main_layout.addWidget(group)

        self.setLayout(main_layout)

    def browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            line_edit.setText(folder)
            self._apply_settings()

    def _apply_settings(self) -> None:
        self.settings.user_location = self.user_location.text().strip()
        self.settings.destination_location = self.dest_location.text().strip()
        mode = self.mode_combo.currentData()
        self.settings.mode = mode if isinstance(mode, str) else "collect"
        self.settings.save()
        self.locations_changed.emit()
