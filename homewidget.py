from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem, QLabel
from PySide6.QtGui import QCursor, Qt, QIcon
from PySide6.QtCore import QSize

from gameentry import GameEntry

import os.path as op, json, subprocess as sp


class HomeWidget(QWidget):
    def __init__(self):
        """ Home Widget Class """
        super().__init__()
        self.ge_window = None # it is declared here bcoz to close game_entry_window when app exits
        self.ge_options = None # it is declared here bcoz to close game_entry_window when app exits
        self.setupWindow()
        self.setupLayout()
        self.setupWidgets()
        self.load_entries()

    def setupWindow(self):
        """ Window Setup """
        self.setWindowTitle('Game Manager')
        self.setWindowIcon(QIcon('./icons/game.ico'))

        with open('./data/style_homewidget.qss', 'r') as styles:
            styles = "".join(line for line in styles.readlines())
            self.setStyleSheet(styles)

        scr = self.screen().size()

        # calculating window position
        # ( centering the window - dividing height and width by 4 works )
        window_pos = (scr.width() // 4, scr.height() // 4) # // used to get int

        HEIGHT = 650
        WIDTH = 450

        self.setGeometry(*window_pos, HEIGHT, WIDTH)

    def setupLayout(self):
        """ Initialize a Vertical Layout """
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)

    def setupWidgets(self):
        """ Makes and Adds Widgets to the vlayout """
        # Default widget for showing game entries it will be replaced by a QListWidget
        self.game_entries = QWidget()
        vlayout = QVBoxLayout()
        self.game_entries.setLayout(vlayout)

        default_game_entry = QLabel('No Game Entries are present. Please ADD one.')
        default_game_entry.setAlignment(Qt.AlignCenter)
        vlayout.addWidget(default_game_entry)


        # Horizontal layout for adding btns
        self.btns = QWidget()
        btns_layout = QHBoxLayout()
        self.btns.setLayout(btns_layout)

        # Cursors
        pointing_cursor = QCursor().shape().PointingHandCursor

        # Add Game Btn - Widget, Connectors
        add_game_btn = QPushButton('')
        add_game_btn.setIcon(QIcon('./icons/add.png'))
        add_game_btn.setIconSize(QSize(70,40))
        add_game_btn.setObjectName('addBtn')
        add_game_btn.setCursor(pointing_cursor)
        add_game_btn.clicked.connect(self.new_game_entry)
        add_game_btn.setFixedSize(75, 65)

        # del Btn - Widget
        self.del_btn = QPushButton('')
        self.del_btn.setIcon(QIcon('./icons/trash.png'))
        self.del_btn.setIconSize(QSize(40,40))
        self.del_btn.setObjectName('deleteBtn')
        self.del_btn.setCursor(pointing_cursor)
        self.del_btn.clicked.connect(self.del_game_entry)
        self.del_btn.setFixedSize(70,70)
        self.del_btn.setEnabled(False)

        # Play Btn - Widget
        self.play_btn = QPushButton()
        self.play_btn.setIcon(QIcon('./icons/play.png'))
        self.play_btn.setIconSize(QSize(90, 90))
        self.play_btn.setObjectName('defaultBtn')
        self.play_btn.setCursor(pointing_cursor)
        self.play_btn.clicked.connect(self.run_game)
        self.play_btn.setFixedSize(70, 70)
        self.play_btn.setEnabled(False)

        # Add Widgets to btns_layout
        btns_layout.addWidget(add_game_btn)
        btns_layout.addWidget(self.del_btn)
        btns_layout.addStretch(25)
        btns_layout.addWidget(self.play_btn)

        # Add Widgets to vlayout
        self.vlayout.addWidget(self.game_entries, 1)
        self.vlayout.addWidget(self.btns, 0)

    def reload_widgets(self, widget):
        self.vlayout.removeWidget(self.game_entries)
        self.vlayout.removeWidget(self.btns)
        self.game_entries = widget
        self.vlayout.addWidget(self.game_entries, 1)
        self.vlayout.addWidget(self.btns, 0)

    def load_entries(self):
        """ Reads and Add game_entries from json file """

        db_name = 'gameentries.json'
        curr_dir = op.abspath(op.curdir)
        db_path = op.join(curr_dir, 'db', db_name)

        # creating db if not present
        if not op.exists(db_path):
            default_stucture = {"game_entries": []}
            with open(db_path, 'w') as db:
                default_stucture = json.dumps(default_stucture)
                db.write(default_stucture)
        else:
            with open(db_path, 'r') as db:
                game_entries = "".join(line for line in db.readlines())
                game_entries = json.loads(game_entries)
                game_entries_list = game_entries['game_entries']

            if len(game_entries_list) > 0:
                if type(self.game_entries) != QListWidget:
                    self.reload_widgets(widget=QListWidget())
                    self.play_btn.setEnabled(True)
                    self.del_btn.setEnabled(True)
                else:
                    self.game_entries.clear()

                for game_entry in game_entries_list:
                    game_name = game_entry['game_name']
                    game_path = game_entry['game_path']
                    game_entry = QListWidgetItem(game_name)
                    game_entry.setTextAlignment(Qt.AlignCenter)
                    game_entry.setData(1, game_path)
                    self.game_entries.addItem(game_entry)

            elif type(self.game_entries) != QWidget:
                game_entries = QWidget()
                vlayout = QVBoxLayout()
                game_entries.setLayout(vlayout)

                default_game_entry = QLabel('No Game Entries are present. Please ADD one.')
                default_game_entry.setAlignment(Qt.AlignCenter)
                vlayout.addWidget(default_game_entry)

                self.reload_widgets(widget=game_entries)
                self.play_btn.setEnabled(False)
                self.del_btn.setEnabled(False)


    def new_game_entry(self):
        """ Shows a game entry window to add a game entry """
        self.ge_window = GameEntry(hw=self)
        self.ge_window.show()
        self.setEnabled(False)  # disabling the home widget

    def del_game_entry(self):
        if self.game_entries.currentRow() != -1:
            db_name = 'gameentries.json'
            curr_dir = op.abspath(op.curdir)
            db_path = op.join(curr_dir, 'db', db_name)

            with open(db_path, 'r') as db:
                game_entries = "".join(line for line in db.readlines())
                game_entries = json.loads(game_entries)
                game_entries_list = game_entries['game_entries']
                del game_entries_list[self.game_entries.currentRow()]

            with open(db_path, 'w') as db:
                game_entries['game_entries'] = game_entries_list
                game_entries = json.dumps(game_entries)
                db.write(game_entries)

            self.load_entries()
        else:
            None

    def run_game(self):
        """ This function runs the selected game with subprocess module and closes this application (optionally)"""
        # selected_game - sg
        if len(self.game_entries.selectedItems()) > 0:
            sg: QListWidgetItem = self.game_entries.selectedItems()[0]
            sg_path = sg.data(1) # data 1 has the game path
            sg_folder_path = op.split(sg_path)[0]
            # subprocess module - sp
            sp.Popen(args='', executable=sg_path, cwd=sg_folder_path)
            self.close()

    def closeEvent(self, event):
        self.ge_options.close() if self.ge_options else None
        self.ge_window.close() if self.ge_window else None
        event.accept()
