from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
import os


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__(flags=Qt.WindowStaysOnTopHint)
        version_file = open(os.path.join('.', 'VERSION'))
        version = version_file.read().strip()
        uic.loadUi('AboutDialog.ui', self)
        self.show()
        self.versionLabel.setText("Version: " + version)
