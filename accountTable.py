from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem
from multiprocessing.pool import ThreadPool

from account import Account

COLUMNS = {
    "KIND": 0,
    "NAME": 1,
    "STATUS": 2,
    "FOLLOWS": 3,
    "UNFOLLOWS": 4,
    "LIKES": 5,
    "COMMENTS": 6,
    "FOLLOWER": 7,
    "AVERAGE LIKES": 8,
}


class AccountTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        QTableWidget.__init__(self, 0, 9, *args, **kwargs)
        self.configUI()
        self.rows = []

    def startAll(self):
        for row in range(self.rowCount()):
            item = self.item(row, COLUMNS["NAME"])
            account = item.data(Qt.UserRole)
            if account.workingThread.isRunning:
                continue
            account.startWorking()

    def addNewRow(self, account):

        firstRow = 0

        self.insertRow(firstRow)
        self.rows.append(account)

        self.setFirstColumn(firstRow, account)
        self.updateRow(firstRow)

    def setFirstColumn(self, row, account):

        name = account.getCredentials()['login']
        nameItem = QTableWidgetItem(name)
        nameItem.setData(Qt.UserRole, account)

        account.setTableAndItem(self, nameItem)

        self.setItem(row, COLUMNS['NAME'], nameItem)

    def updateRow(self, row: int):
        self.setSortingEnabled(False)
        # Getting account object from name column
        nameItem = self.item(row, COLUMNS['NAME'])
        account = nameItem.data(Qt.UserRole)

        # Setting all other columns
        #  Status button

        # Kind
        kindItem = QTableWidgetItem(account.getKind())
        self.setItem(row, COLUMNS['KIND'], kindItem)

        # Status
        statusItem = QTableWidgetItem(account.status)
        statusItem.setTextAlignment(Qt.AlignCenter)
        if account.status == "OFF":
            statusItem.setForeground(QColor("red"))
        elif account.status == "ON":
            statusItem.setForeground(QColor("green"))
        elif account.status == "Connecting...":
            statusItem.setForeground(QColor("orange"))
        elif account.status == "Waiting...":
            statusItem.setForeground(QColor("blue"))
        self.setItem(row, COLUMNS["STATUS"], statusItem)

        # Follows done
        followDoneItem = QTableWidgetItem('{}'.format(account.followsDoneStat.get()))
        self.setItem(row, COLUMNS['FOLLOWS'], followDoneItem)

        # unfollow done
        unfollowDoneItem = QTableWidgetItem('{}'.format(account.unfollowsDoneStat.get()))
        self.setItem(row, COLUMNS['UNFOLLOWS'], unfollowDoneItem)

        # likes done
        likesDoneItem = QTableWidgetItem('{} {:+}'.format(*account.likesDoneStat.get()))
        self.setItem(row, COLUMNS['LIKES'], likesDoneItem)

        # likes done
        commentsDoneItem = QTableWidgetItem('{} {:+}'.format(*account.commentsDoneStat.get()))
        self.setItem(row, COLUMNS['COMMENTS'], commentsDoneItem)

        # likes done
        followersItem = QTableWidgetItem('{} {:+}'.format(*account.followersStat.get()))
        self.setItem(row, COLUMNS['FOLLOWER'], followersItem)

        self.sortItems(0)
        self.resizeRowsToContents()

    def removeCurrent(self):
        indexes = self.selectionModel().selectedRows()
        for index in reversed(indexes):
            item = self.item(index.row(), COLUMNS['NAME'])

            account = item.data(Qt.UserRole)
            account.waitingThread.cancel()
            self.rows.remove(account)
            self.removeRow(index.row())

    def configUI(self):
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        labels = ["KIND", "NAME", "STATUS", "FOLLOWS", "UNFOLLOWS", "LIKES", "COMMENTS",
                  "FOLLOWER", "AVERAGE LIKES\nPER POST"]
        self.setHorizontalHeaderLabels(labels)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setHighlightSections(False)
        self.itemDoubleClicked.connect(self.handleItemDoubleClicked)
        self.itemClicked.connect(self.handleItemClicked)

    def handleItemClicked(self, item):
        row = item.row()
        column = item.column()
        item = self.item(row, COLUMNS["NAME"])
        account = item.data(Qt.UserRole)
        if column == 2:
            account.handleStatusButtonClicked()

    def handleItemDoubleClicked(self, item):
        row = item.row()
        column = item.column()
        item = self.item(row, COLUMNS["NAME"])
        account = item.data(Qt.UserRole)

        if column in [0, 1]:

            account.stopWorking()
            dlg = account.settingDialog
            if not dlg.exec_():
                return
            account.startWorking()
            self.setFirstColumn(row, account)
            self.updateRow(row)



