import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from main import Ui_MainWindow  # Import from `main.py`, assuming `Ui_MainWindow` is in `main.py`

class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
