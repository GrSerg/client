import sys

from PyQt5 import QtCore, QtWidgets, uic
from gui.main_form import Ui_MainWindow as ui_class

from gui.monitor import Monitor

class MyWindow(QtWidgets.QMainWindow):

    def __init__(self, parent = None):

        super().__init__(parent)
        self.ui = ui_class()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.monitor = Monitor(self)
        self.thread = QtCore.QThread()

        self.monitor.gotData.connect(self.resp)

        self.sign_in()

    def registration(self):
        dialog_reg = uic.loadUi('gui/sign_up.ui')
        self.monitor.moveToThread(self.thread)
        self.thread.started.connect(self.monitor.recv_msg)
        dialog_reg.login.setFocus()

        def reg():
            pass

        dialog_reg.ok.clicked.connect(reg)
        dialog_reg.ok.clicked.connect(dialog_reg.accept)
        dialog_reg.cancel.clicked.connect(dialog_reg.close)
        dialog_reg.cancel.clicked.connect(self.sign_in)
        dialog_reg.exec()

    def sign_in(self):

        dialog = uic.loadUi('gui/sign_in.ui')
        self.monitor.moveToThread(self.thread)
        self.thread.started.connect(self.monitor.recv_msg)
        dialog.login.setFocus()

        def login():
            name = dialog.login.text()
            password = dialog.password.text()
            self.monitor.client.connect_guest(name, password)
            self.thread.start()

        dialog.ok.clicked.connect(login)
        dialog.ok.clicked.connect(dialog.accept)
        dialog.registration.clicked.connect(dialog.close)
        dialog.registration.clicked.connect(self.registration)
        dialog.cancel.clicked.connect(sys.exit)
        dialog.exec()

    def on_createTask_pressed(self):
        dialog = uic.loadUi('gui/task_create.ui')
        dialog.topic.setFocus()

        def task_create():
            pass

        dialog.addTask.clicked.connect(task_create)
        dialog.addTask.clicked.connect(dialog.accept)
        dialog.exec()

    def resp(self):
        pass
        ################################################