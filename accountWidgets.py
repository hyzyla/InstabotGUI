from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QDialog, QFrame, QPushButton, QMessageBox, QStyle

from settingWidget import SettingWidget


class AccountDialog(QDialog):

    def __init__(self, *args, parameters=None, **kwargs):
        QDialog.__init__(self, *args, **kwargs)

        self.settingWidget = SettingWidget(self)
        self.acceptButton = QPushButton("Accept")
        self.cancelButton = QPushButton("Cancel")

        self.configUI()
        self.bindWidgets()
        if parameters is not None:
            self.settingWidget.setParameters(parameters)

    def bindWidgets(self):
        self.acceptButton.clicked.connect(self.currentAccept)
        self.cancelButton.clicked.connect(self.reject)
        self.getCredentials = self.settingWidget.getCredentials

    def currentAccept(self):
        # Check login and password
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        if not self.settingWidget.hasLoginAndPassword():
            msg.setText("Login or password is empty!")
            msg.setInformativeText("Please, provide login or password for your account")
            msg.exec_()
            return
        elif self.settingWidget.tagTextEdit.toPlainText() == "":
            msg.setText("Tag list empty!")
            msg.setInformativeText("Please, provide tag list")
            msg.exec_()
            return
        self.accept()

    def configUI(self):
        self.setWindowTitle("Settings")
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        layout = QGridLayout()
        controlFrame = self.configControlFrame()

        layout.addWidget(self.settingWidget, 0, 0)
        layout.addWidget(controlFrame, 1, 0, Qt.AlignRight)

        self.resize(900, 500)
        self.setLayout(layout)

    def configControlFrame(self):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.acceptButton, 0, 0, Qt.AlignRight)
        layout.addWidget(self.cancelButton, 0, 1, Qt.AlignRight)

        frame = QFrame()
        frame.setLayout(layout)

        return frame


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = AccountDialog()
    w.show()
    sys.exit(app.exec_())