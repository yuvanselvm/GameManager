from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtWidgets import QFileDialog, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import os.path as op , json


class GameEntry(QDialog):
    def __init__(self, hw):
        """ This class helps to add new game entry """
        super().__init__()
        self.hw = hw
        self.setupWindow()
        self.setupLayout()
        self.setupWidgets()

    def setupWindow(self):
        """ Window Setup """
        self.setWindowTitle('Add a Game')
        self.setWindowIcon(QIcon('./icons/game.ico'))
        with open('./data/style_game_entry.qss', 'r') as styles:
            styles = "".join(line for line in styles.readlines())
            self.setStyleSheet(styles)

        scr = self.screen().size()
        # calculating the position of the window
        # centering it - dividing the screen height and width by some value(find by just experimenting)
        window_pos = (scr.width() / 2.7, scr.height() / 2.5)

        HEIGHT = 210
        self.WIDTH = 320

        self.setGeometry(*window_pos, self.WIDTH, HEIGHT)

    def setupLayout(self):
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)

    def setupWidgets(self):
        # Name - Widget
        self.game_name = QLineEdit()
        self.game_name.setFixedSize(self.WIDTH, 30)
        self.game_name.setTextMargins(self.WIDTH/3.1,0,0,0)
        self.game_name.setPlaceholderText("Game Name  *required")
        self.game_name.setMaxLength(35)
        self.game_name.clearFocus()

        # Path - Widget, Layout
        path_widget = QWidget()
        path_widget_layout = QHBoxLayout()
        path_widget.setLayout(path_widget_layout)

        self.game_path = QLineEdit()
        self.game_path.setFixedSize(self.WIDTH / 1.4, 30)
        self.game_path.setTextMargins(15,0,0,0)
        self.game_path.setPlaceholderText("Path to Executable *required")

        browse_btn = QPushButton("Browse")
        browse_btn.setFixedSize(70, 30)
        browse_btn.setObjectName('bordered')
        browse_btn.clicked.connect(self.game_select_dialog)

        path_widget_layout.addWidget(self.game_path)
        path_widget_layout.addWidget(browse_btn)

        # Game Add Btn
        add_btn = QPushButton('Add Game')
        add_btn.setObjectName('defaultBtn')
        add_btn.clicked.connect(self.add_game)
        add_btn.setFixedSize(self.WIDTH, 30)

        self.vlayout.addStretch(1)
        self.vlayout.addWidget(self.game_name)
        self.vlayout.addStretch(1)
        self.vlayout.addWidget(path_widget)
        self.vlayout.addStretch(4)
        self.vlayout.addWidget(add_btn)
        self.vlayout.addStretch(1)

    def game_select_dialog(self):
        game_file_url = QFileDialog.getOpenFileUrl(
            filter="Game Executable (*exe)")[0]
        # [1:] is used to remove the first character ('/') in the str
        game_file_url = game_file_url.path()[1:]
        self.game_path.setText(game_file_url)


    def add_game(self):
        game_name = self.game_name.text().strip()
        game_path = self.game_path.text().strip()

        if game_name != "" and op.isfile(game_path):
            db_name = 'gameentries.json'
            curr_dir = op.abspath(op.curdir)
            db_path = op.join(curr_dir, 'db', db_name)

            with open(db_path, 'r') as db:
                game_entries = "".join(line for line in db.readlines())

            with open(db_path, "w") as db:
                game_entries: dict = json.loads(game_entries)
                game_entries_list: list = game_entries['game_entries']
                game_entry = {
                    'game_name': f"{game_name}",
                    'game_path': f"{game_path}"
    }
                game_entries_list.append(game_entry)
                game_entries["game_entries"] = game_entries_list
                game_entries = json.dumps(game_entries)
                db.write(game_entries)


            self.close()

    # resetting the field
        self.game_name.setText(
            "") if game_name == "" else None
    # resetting the field if the provided executable path is not valid
        self.game_path.setText(
            "") if not op.isfile(game_path) else None


    def closeEvent(self, event):
        self.hw.setEnabled(True)  # enabling home widget
        self.hw.load_entries()
        self.hw.ge_window = None
        event.accept()
