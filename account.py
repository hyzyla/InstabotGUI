import queue
import time
from multiprocessing import Process, Queue
import threading

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from instabotpy.instabot import InstaBot

from accountWidgets import AccountDialog
from statmodule import Last24Stat, TotalDone, TotalChange


def runInstaBot(params):
    queue = params['queue']
    try:
        bot = InstaBot(**params)
        bot.new_auto_mod()
    except:
        queue.put_nowait("Exception")


class AccountThread(QThread):
    messageAppeared = pyqtSignal(str)
    stopped = pyqtSignal()
    interrupted = pyqtSignal()

    def __init__(self, params, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.params = params
        self.queue = Queue()
        self.params['queue'] = self.queue
        # mod for queue
        self.params['log_mod'] = 2
        self.isRunning = False
        self.process = None

    def stop(self):

        self.process.terminate()
        self.isRunning = False

    def run(self):
        self.isRunning = True
        self.process = Process(target=runInstaBot, args=(self.params,), daemon=True)
        self.process.start()
        while self.isRunning and self.process.is_alive():
            time.sleep(0.3)
            try:
                msg = self.queue.get_nowait()
                self.processMessage(msg)
            except queue.Empty:
                pass
        if not self.isRunning:
            self.stopped.emit()
        else:
            self.interrupted.emit()

    def processMessage(self, msg):
        if 'Liked' in msg:
            self.messageAppeared.emit('like')
        elif 'Followed' in msg:
            self.messageAppeared.emit('follow')
        elif 'Write:' in msg:
            self.messageAppeared.emit('comment')
        elif 'Unfollow' in msg:
            self.messageAppeared.emit('unfollow')
        elif 'login success!' in msg:
            self.messageAppeared.emit("Login success")
        elif 'Followers count:' in msg:
            self.messageAppeared.emit(msg)
        elif "Login error!" in msg:
            self.process.terminate()#.isRunning.messageAppeared.emit("Login error")
        elif "Exception" in msg:
            self.process.terminate()#messageAppeared.emit("Exception")


class FakeAccountThread:
    isRunning = False

    def stop(self):
        self.isRunning = False

class Account(QObject):
    def __init__(self, *args, credentials=None, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.status = "undefined" if not credentials else "OFF"
        # Need for imitation work without real thread
        self.workingThread = FakeAccountThread()
        self.waitingThread = threading.Timer(0, lambda x: x)

        self.followsDoneStat = Last24Stat()
        self.unfollowsDoneStat = Last24Stat()
        self.likesDoneStat = TotalDone()
        self.commentsDoneStat = TotalDone()
        self.followersStat = TotalChange()
        self.avarageLikePerPost = 0

        self.settingDialog = AccountDialog(parameters=credentials)
        self.getCredentials = self.settingDialog.getCredentials
        self.getKind = self.settingDialog.settingWidget.getKind
        self.getSettings = self.settingDialog.settingWidget.getSettings

    def setTableAndItem(self, table, item):
        self.parentTable = table
        self.tableItem = item

    def startWorking(self):

        self.waitingThread.cancel()
        credentials = self.settingDialog.getCredentials()
        credentials.pop('kind', None)
        self.workingThread = AccountThread(params=credentials)
        self.workingThread.interrupted.connect(lambda: self.stopWorking(restart=True))
        self.workingThread.stopped.connect(lambda: self.stopWorking())
        self.workingThread.messageAppeared.connect(self.handleMessegeFromThread)
        self.workingThread.start()
        self.status = "Connecting..."
        self.updateTableRow()

    def stopWorking(self, restart=False):
        self.workingThread.stop()
        time.sleep(0.6)
        # This two lines allows a pickling data.
        # First we delete Thread object and then add fake class with isWorking=False attribute
        # del self.workingThread
        self.workingThread = FakeAccountThread()
        self.workingThread.stop()
        self.status = "OFF"
        if restart:
            self.handleRestart()
        self.updateTableRow()

    def handleRestart(self):
        if self.settingDialog.settingWidget.autostartCombobox.currentText() == "YES":
            autostartTime = self.settingDialog.settingWidget.autostartTime.value()
            self.waitingThread.cancel()
            self.waitingThread = threading.Timer(autostartTime * 60, self.startWorking)
            self.waitingThread.daemon = True
            self.waitingThread.start()
            self.status = "Waiting..."

    def handleMessegeFromThread(self, msg):
        if msg == 'like':
            self.likesDoneStat.increase()
        elif msg == 'follow':
            self.followsDoneStat.increase()
        elif msg == 'unfollow':
            self.unfollowsDoneStat.increase()
        elif msg == 'comment':
            self.commentsDoneStat.increase()
        elif 'Followers count:' in msg:
            self.followersStat.set(int(msg.split(': ')[1]))
        elif 'Login success' in msg:
            self.status = "ON"
        # elif "Login error" in msg:
        #     self.stopWorking(restart=True)
        #     #self.showErrorMsg("Login error. Check your credentials.")
        # elif "Exception" in msg:
        #     self.stopWorking(restart=True)
        else:
            return

        self.updateTableRow()

    def updateTableRow(self):
        self.parentTable.updateRow(self.tableItem.row())

    def showErrorMsg(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.exec_()
        return

    def handleStatusButtonClicked(self):
        if self.workingThread.isRunning:
            self.stopWorking()
        else:
            self.startWorking()

    def setStats(self, stat):
        self.followsDoneStat, self.unfollowsDoneStat, self.likesDoneStat, self.commentsDoneStat, self.followersStat, self.avarageLikePerPost = stat

    def getStats(self):
        return self.followsDoneStat, self.unfollowsDoneStat, self.likesDoneStat, self.commentsDoneStat, self.followersStat, self.avarageLikePerPost