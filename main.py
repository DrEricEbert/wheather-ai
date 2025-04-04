# main.py

from PySide6.QtWidgets import QApplication
from gui import WeatherApp
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())