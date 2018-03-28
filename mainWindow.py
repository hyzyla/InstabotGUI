import atexit
import multiprocessing
import pickle
import signal
import sys


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QApplication, QGridLayout, QWidget, QStyle,
                             QPushButton, QFrame)

from account import Account
from accountTable import AccountTable

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.accountTable = AccountTable()
        self.addNewAccountButton = QPushButton("New")
        self.removeAccountButton = QPushButton("Remove")
        self.startAllButton = QPushButton("Start all")

        self.configUI()
        self.bindWidgets()
        self.restoreSession()

    def restoreSession(self):
        # Do nothing when file not found
        try:
            with open('data.pickle', 'rb') as f:
                rows = pickle.load(f)
        except FileNotFoundError:
            return

        # Adding rows to table
        for credentials, stats in zip(*rows):

            account = Account(credentials=credentials)
            account.setStats(stats)
            self.accountTable.addNewRow(account)

    def addNewAccount(self):
        account = Account()
        dlg = account.settingDialog
        if not dlg.exec_():
            return
        self.accountTable.addNewRow(account)
        account.startWorking()

    def bindWidgets(self):
        self.addNewAccountButton.clicked.connect(self.addNewAccount)
        self.removeAccountButton.clicked.connect(self.removeAccount)
        self.startAllButton.clicked.connect(self.startAll)

    def startAll(self):
        self.accountTable.startAll()

    def stopAll(self):
        self.accountTable.stopAll()

    def removeAccount(self):
        self.accountTable.removeCurrent()

    def configUI(self):
        layout = QGridLayout()
        widget = QWidget()
        widget.setLayout(layout)

        controlFrame = self.configControlFrame()
        layout.addWidget(controlFrame, 1, 0)
        layout.addWidget(self.accountTable, 2, 0)

        self.resize(800, 600)
        self.setCentralWidget(widget)
        self.setWindowTitle("InstaBot")
        icon = self.style().standardIcon(QStyle.SP_FileDialogListView)
        self.setWindowIcon(icon)
        self.show()

    def configControlFrame(self):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setColumnStretch(2, 1)
        layout.addWidget(self.addNewAccountButton, 0, 0, Qt.AlignLeft)
        layout.addWidget(self.removeAccountButton, 0, 1, Qt.AlignLeft)
        layout.addWidget(self.startAllButton, 0, 3, Qt.AlignRight)

        frame = QFrame()
        frame.setLayout(layout)
        return frame


def exit_handler(window):
    rows = window.accountTable.rows

    for row in rows:
        row.stopWorking()

    credentialsRows = [r.getSettings() for r in rows]
    statsRow = [r.getStats() for r in rows]
    with open('data.pickle', 'wb') as f:
        pickle.dump([credentialsRows, statsRow], f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    with open("style.qss") as fileStyle:
        style = fileStyle.read()

    app.setStyleSheet(style)
    window = MainWindow()
    atexit.register(lambda: exit_handler(window))
    signal.signal(signal.SIGTERM, lambda: exit_handler(window))
    try:
        sys.exit(app.exec_())
    except:
        exit_handler(window)
