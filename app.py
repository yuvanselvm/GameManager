import sys
from PySide6.QtWidgets import QApplication
from homewidget import HomeWidget

app = QApplication()
home = HomeWidget()

home.show()
sys.exit(app.exec())
