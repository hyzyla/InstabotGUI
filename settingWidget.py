from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QGridLayout, QFormLayout, QDoubleSpinBox, QFrame,
    QTextEdit, QComboBox, QSplitter)


class SettingWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(SettingWidget, self).__init__(*args, **kwargs)

        self.kindLineEdit = QLineEdit(self)
        self.loginLineEdit = QLineEdit(self)
        self.passwordLineEdit = QLineEdit(self)

        self.likePerDay = self.initSpinBox(1200.0)
        self.mediaMaxLike = self.initSpinBox(500.0)
        self.mediaMinLike = self.initSpinBox(20.0)
        self.followerPerDay = self.initSpinBox(600.0)
        self.followTime = self.initSpinBox(18000)
        self.unfollowPerDay = self.initSpinBox(600.0)
        self.commentsPerDay = self.initSpinBox(450.0)

        self.commentsTextEdit = QTextEdit()
        self.commentsTextEdit.setPlainText("great!\nnice\n:)\nawesome\namazing")
        self.tagTextEdit = QTextEdit()
        self.tagBlackTextEdit = QTextEdit()
        self.userBlackTextEdit = QTextEdit()

        self.maxLikeForOneTag = self.initSpinBox(999999.0)
        self.unfollowBreakMin = self.initSpinBox(16.0)
        self.unfollowBreakMax = self.initSpinBox(30.0)

        self.proxy = QLineEdit()

        self.autostartCombobox = QComboBox()
        self.autostartCombobox.addItems(['YES', 'NO'])
        self.autostartTime = self.initSpinBox(10.0)

        self.configUI()

    def initSpinBox(self, value=0.0):
        spinBox = QDoubleSpinBox()
        spinBox.setMaximum(999999.0)
        spinBox.setValue(value)
        spinBox.setDecimals(0)
        return spinBox

    def setParameters(self, parameteres):
        self.kindLineEdit.setText(parameteres.get('kind', ''))
        self.loginLineEdit.setText(parameteres.get('login', ''))
        self.passwordLineEdit.setText(parameteres.get('password', ''))
        self.likePerDay.setValue(parameteres.get('like_per_day', 0.0))
        self.mediaMaxLike.setValue(parameteres.get('media_max_like', 0.0))
        self.mediaMinLike.setValue(parameteres.get('media_min_like', 0.0))
        self.followerPerDay.setValue(parameteres.get('follow_per_day', 0.0))
        self.followTime.setValue(parameteres.get('follow_time', 0.0))
        self.unfollowPerDay.setValue(parameteres.get('unfollow_per_day', 0.0))
        self.commentsPerDay.setValue(parameteres.get('comments_per_day', 0.0))
        commentsLists = parameteres.get('comment_list', [])

        # Dirty hack for different version of program
        if commentsLists and isinstance(commentsLists[0], list):
            self.commentsTextEdit.setPlainText(
                '\n'.join([' '.join(commentList) for commentList in commentsLists]))
        elif commentsLists and isinstance(commentsLists, str):
            self.commentsTextEdit.setPlainText(
                '\n'.join([commentList for commentList in commentsLists]))

        self.tagTextEdit.setPlainText(
             " ".join(["#{}".format(i) for i in parameteres.get('tag_list', [])]))
        self.tagBlackTextEdit.setPlainText(
            " ".join(["#{}".format(i) for i in parameteres.get('tag_blacklist', [])]))
        self.userBlackTextEdit.setPlainText(
            '\n'.join([item for item in parameteres.get('user_blacklist', {})]))
        self.maxLikeForOneTag.setValue(parameteres.get('max_like_for_one_tag', ''))
        self.unfollowBreakMin.setValue(parameteres.get('unfollow_break_min', ''))
        self.proxy.setText(parameteres.get('proxy', ''))
        self.autostartCombobox.setCurrentText(parameteres.get('autostart','YES'))
        self.autostartTime.setValue(parameteres.get('autostart_time', 0.0))


    def configUI(self):

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        #layout.setColumnStretch(1, 1)

        splitter = QSplitter()
        layout.addWidget(splitter)

        leftLayout = QFormLayout()
        rightLayout1 = QFormLayout()
        rightLayout2 = QFormLayout()

        leftLayout.setContentsMargins(0, 0, 0, 0)
        rightLayout1.setContentsMargins(0, 0, 0, 0)
        rightLayout2.setContentsMargins(0, 0, 0, 0)

        leftLayoutWidget = QWidget()
        rightLayout1Widget = QWidget()
        rightLayout2Widget = QWidget()

        leftLayoutWidget.setLayout(leftLayout)
        rightLayout1Widget.setLayout(rightLayout1)
        rightLayout2Widget.setLayout(rightLayout2)

        splitter.addWidget(leftLayoutWidget)
        splitter.addWidget(rightLayout1Widget)
        splitter.addWidget(rightLayout2Widget)

        leftLayout.addRow("", QLabel("Parameters:"))
        leftLayout.addRow("Kind", self.kindLineEdit)
        leftLayout.addRow("Login", self.loginLineEdit)
        leftLayout.addRow("Password", self.passwordLineEdit)
        leftLayout.addRow("Like per day:", self.likePerDay)
        leftLayout.addRow("Media max like:", self.mediaMaxLike)
        leftLayout.addRow("Media min like:", self.mediaMinLike)
        leftLayout.addRow("Follower per day:", self.followerPerDay)
        leftLayout.addRow("Follow time:", self.followTime)
        leftLayout.addRow("Unfollow per day:", self.unfollowPerDay)
        leftLayout.addRow("Coments per day:", self.commentsPerDay)
        leftLayout.addRow("Max like for one tag:", self.maxLikeForOneTag)
        leftLayout.addRow("Unfollow break min:", self.unfollowBreakMin)
        leftLayout.addRow("Unfollow break max:", self.unfollowBreakMax)
        leftLayout.addRow("Auto start", self.autostartCombobox)
        leftLayout.addRow("Auto start time (m):", self.autostartTime)
        leftLayout.addRow("Proxy:", self.proxy)
        leftLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        rightLayout1.addRow("Comments list:", self.commentsTextEdit)
        rightLayout1.addRow("Tag list:", self.tagTextEdit)
        rightLayout1.setRowWrapPolicy(QFormLayout.WrapAllRows)

        rightLayout2.addRow("User black list", self.userBlackTextEdit)
        rightLayout2.addRow("Tag black list:", self.tagBlackTextEdit)
        rightLayout2.setRowWrapPolicy(QFormLayout.WrapAllRows)


    def initLoginForm(self):
        passwordLabel = QLabel("Password:")
        loginLabel = QLabel("Login:")

        frame = QFrame()
        layout = QGridLayout()

        layout.setRowStretch(100, 1)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(loginLabel, 0, 0)
        layout.addWidget(self.loginLineEdit, 1, 0)
        layout.addWidget(passwordLabel, 0, 1)
        layout.addWidget(self.passwordLineEdit, 1, 1)
        frame.setLayout(layout)
        return frame

    def hasLoginAndPassword(self):
        return self.loginLineEdit.text() and self.passwordLineEdit.text()

    def getKind(self):
        return self.kindLineEdit.text()

    def getCredentials(self):
        credentials = {}
        credentials['login'] = self.loginLineEdit.text()
        credentials['password'] = self.passwordLineEdit.text()
        credentials['like_per_day'] = self.likePerDay.value()
        credentials['media_max_like'] = self.mediaMaxLike.value()
        credentials['media_min_like'] = self.mediaMinLike.value()
        credentials['follow_per_day'] = self.followerPerDay.value()
        credentials['follow_time'] = self.followTime.value()
        credentials['unfollow_per_day'] = self.unfollowPerDay.value()
        credentials['comments_per_day'] = self.commentsPerDay.value()
        credentials['comment_list'] = self.commentsTextEdit.toPlainText().split('\n')
        credentials['tag_list'] = [item.replace('#', '') for item in self.tagTextEdit.toPlainText().split()]
        credentials['tag_blacklist'] = [item.replace('#', '') for item in self.tagBlackTextEdit.toPlainText().split()]
        credentials['user_blacklist'] = {item.strip(): '' for item in self.userBlackTextEdit.toPlainText().split('\n')}
        credentials['max_like_for_one_tag'] = self.maxLikeForOneTag.value()
        credentials['unfollow_break_min'] = self.unfollowBreakMin.value()
        credentials['proxy'] = self.proxy.text()

        return credentials

    def getSettings(self):
        credentials = self.getCredentials()
        credentials['kind'] = self.getKind()
        credentials['autostart'] = self.autostartCombobox.currentText()
        credentials['autostart_time'] = self.autostartTime.value()
        return credentials


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = SettingWidget()
    w.show()
    sys.exit(app.exec_())
