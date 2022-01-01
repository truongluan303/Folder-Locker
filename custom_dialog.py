# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog


class PromptDialog(QDialog):

    def __init__(self, master=None, title="Dialog"):
        super().__init__(master)
        self.name_box = None
        self.confirm_label = None
        self.button_box = None
        self.name_label = None
        self.password_label = None
        self.password_box = None
        self.confirm_label = None
        self.confirm_box = None
        self.setup_ui(self)
        self.setWindowTitle(title)
        self.show()



    def get_results(self) -> tuple:
        """
        get the results entered by the user
        :return: a tuple of 3 elements: locker's name, locker's password,
                 and confirm password. Return null if the user cancels
        """
        if self.exec_() == QDialog.Accepted:
            name = str(self.name_box.text()).strip()
            pw = str(self.password_box.text()).strip()
            cpw = str(self.confirm_box.text()).strip()
            return name, pw, cpw
        else:
            return None



    def setup_ui(self, dialog) -> None:
        """
        setup the UI components
        :param dialog: the dialog window
        """
        dialog.setObjectName("Dialog")
        dialog.resize(367, 235)
        dialog.setAutoFillBackground(False)

        self.button_box = QtWidgets.QDialogButtonBox(dialog)
        self.button_box.setGeometry(QtCore.QRect(10, 190, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")

        self.name_label = QtWidgets.QLabel(dialog)
        self.name_label.setGeometry(QtCore.QRect(50, 40, 91, 17))
        self.name_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.name_label.setObjectName("name_label")

        self.password_label = QtWidgets.QLabel(dialog)
        self.password_label.setGeometry(QtCore.QRect(70, 90, 71, 17))
        self.password_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.password_label.setObjectName("password_label")

        self.confirm_label = QtWidgets.QLabel(dialog)
        self.confirm_label.setGeometry(QtCore.QRect(10, 140, 131, 17))
        self.confirm_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.confirm_label.setObjectName("confirm_label")

        self.name_box = QtWidgets.QLineEdit(dialog)
        self.name_box.setGeometry(QtCore.QRect(150, 35, 201, 30))
        self.name_box.setObjectName("name_box")

        self.password_box = QtWidgets.QLineEdit(dialog)
        self.password_box.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_box.setGeometry(QtCore.QRect(150, 85, 201, 30))
        self.password_box.setObjectName("password_box")

        self.confirm_box = QtWidgets.QLineEdit(dialog)
        self.confirm_box.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_box.setGeometry(QtCore.QRect(150, 135, 201, 30))
        self.confirm_box.setObjectName("confirm_box")

        self.re_translate_ui()
        self.button_box.accepted.connect(dialog.accept)
        self.button_box.rejected.connect(dialog.reject)

        QtCore.QMetaObject.connectSlotsByName(dialog)



    def re_translate_ui(self) -> None:
        """
        add text to the UI components
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        self.name_label.setText(_translate("Dialog", "Locker Name"))
        self.password_label.setText(_translate("Dialog", "Password"))
        self.confirm_label.setText(_translate("Dialog", "Confirm Password"))
