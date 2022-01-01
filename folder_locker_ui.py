# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'folder_locker.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

import sys
from locker import LockerManager
from PyQt5 import QtCore, QtGui, QtWidgets
from custom_dialog import PromptDialog
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QMessageBox



class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.label = None
        self.central_widget = None
        self.scroll_area_layout = None
        self.scroll_area = None
        self.scroll_area_contents = None
        self.add_button = None
        self.menu_bar = None
        self.status_bar = None
        self.row_number = 0

        self.__setup_ui(self)

        self._manager = LockerManager()
        self._row_map = dict()
        self._label_map = dict()
        self._open_btn_map = dict()
        self._del_btn_map = dict()
        self._edit_btn_map = dict()
        self.__init_scroll_area()



    def __setup_ui(self, window) -> None:
        """
        setup the non-dynamic UI components
        :param window: the main window
        """
        window.setObjectName("main_window")
        window.setFixedSize(521, 432)
        window.setStyleSheet("background-color: rgb(80, 80, 80); color: rgb(255, 255, 255);")

        self.central_widget = QtWidgets.QWidget(window)
        self.central_widget.setObjectName("central_widget")

        self.scroll_area_contents = QtWidgets.QWidget()
        self.scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 499, 319))
        self.scroll_area_contents.setObjectName("scroll_area_contents")

        self.scroll_area = QtWidgets.QScrollArea(self.central_widget)
        self.scroll_area.setGeometry(QtCore.QRect(9, 60, 501, 321))
        self.scroll_area.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.scroll_area_contents)

        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.scroll_area_contents)
        self.scroll_area_layout.setObjectName("vertical_layout")

        font = QtGui.QFont()
        font.setFamily("Saab")
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)

        self.label = QtWidgets.QLabel(self.central_widget)
        self.label.setGeometry(QtCore.QRect(10, 10, 221, 41))
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(200, 200, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.add_button = QtWidgets.QPushButton(self.central_widget)
        self.add_button.setGeometry(QtCore.QRect(340, 10, 161, 41))
        self.add_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.add_button.setStyleSheet("background-color: rgb(0, 100, 50);")
        self.add_button.setObjectName("add_button")
        self.add_button.clicked.connect(self.__on_add_button_clicked)

        window.setCentralWidget(self.central_widget)

        self.menu_bar = QtWidgets.QMenuBar(window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 521, 22))
        self.menu_bar.setObjectName("menu_bar")

        window.setMenuBar(self.menu_bar)

        self.status_bar = QtWidgets.QStatusBar(window)
        self.status_bar.setObjectName("status_bar")

        window.setStatusBar(self.status_bar)

        self.__re_translate_ui(window)

        QtCore.QMetaObject.connectSlotsByName(window)



    def __re_translate_ui(self, window) -> None:
        """
        add text to the non-dynamic components
        :param window: the main window
        """
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("main_window", "Folder Locker"))
        self.label.setText(_translate("main_window", "Folder Locker"))
        self.add_button.setText(_translate("main_window", "Add New Locker"))



    def __init_scroll_area(self) -> None:
        """
        initialize the scroll area with the lockers
        """
        names = self._manager.get_lockers_names()
        for name in names:
            self.__add_locker_row(name)



    def __add_locker_row(self, name) -> None:
        """
        add a new row/locker to the scroll area
        :param name: the name of the new locker
        """
        row = QtWidgets.QFrame(self.scroll_area)
        self._row_map[name] = row
        grid_layout = QtWidgets.QGridLayout(row)

        name_label = QtWidgets.QLabel()
        name_label.setText(name)
        self._label_map[name] = name_label

        open_button = QtWidgets.QPushButton()
        open_button.setText("Open Folder")
        open_button.setFixedWidth(100)
        open_button.setFixedHeight(30)
        open_button.setStyleSheet("background-color: rgb(20, 30, 100);")
        open_button.clicked.connect(lambda: self.__on_open_button_clicked(open_button))
        self._open_btn_map[open_button] = name

        edit_button = QtWidgets.QPushButton()
        edit_button.setText("Edit")
        edit_button.setFixedWidth(60)
        edit_button.setFixedHeight(30)
        edit_button.setStyleSheet("background-color: rgb(130, 130, 0);")
        edit_button.clicked.connect(lambda: self.__on_edit_button_clicked(edit_button))
        self._edit_btn_map[edit_button] = name

        del_button = QtWidgets.QPushButton()
        del_button.setText("Delete")
        del_button.setFixedWidth(60)
        del_button.setFixedHeight(30)
        del_button.setStyleSheet("background-color: rgb(100, 30, 20);")
        del_button.clicked.connect(lambda: self.__on_delete_button_clicked(del_button))
        self._del_btn_map[del_button] = name

        grid_layout.addWidget(name_label, self.row_number, 0)
        grid_layout.addWidget(open_button, self.row_number, 1)
        grid_layout.addWidget(edit_button, self.row_number, 2)
        grid_layout.addWidget(del_button, self.row_number, 3)

        self.scroll_area_layout.addWidget(row)
        self.row_number += 1



    def __on_add_button_clicked(self) -> None:
        """
        handle the event when the add button is clicked
        """
        dialog = PromptDialog(self, "Enter The New Name and Password")
        response = dialog.get_results()

        if not response:
            return
        name, pw, cpw = response

        if name == "" or pw == "" or cpw == "":
            self.__show_error("Fields cannot be empty!")
            return

        # show error if the password and confirm password don't match
        if pw != cpw:
            self.__show_error("Confirm Password does not match!")
            return

        # try to add the new locker, if not successful then show error
        if not self._manager.add_locker(name, pw):
            self.__show_error("Name already existed!")
            return

        self.__add_locker_row(name)



    def __on_open_button_clicked(self, source) -> None:
        """
        handle the event on the open locker button clicked
        :param source: the source button that was clicked
        """
        locker_id = self._open_btn_map[source]
        locker_name = self._label_map[locker_id].text()
        pw, _ = QInputDialog.getText(self, "Enter Password",
                                     f"Please enter the password for locker \"{locker_name}\"",
                                     QtWidgets.QLineEdit.Password)
        pw = pw.strip()
        if pw == "":
            return

        response = self._manager.open_locker(locker_id, pw)
        if not response:
            return

        success, message = response
        if not success:
            self.__show_error(message)



    def __on_edit_button_clicked(self, source) -> None:
        """
        handle the event on the edit locker button clicked
        :param source: the source button that was clicked
        """
        locker_id = self._edit_btn_map[source]
        locker_name = self._label_map[locker_id].text()
        pw, _ = QInputDialog.getText(self, "Enter Password",
                                     f"Please enter the password for locker \"{locker_name}\"",
                                     QtWidgets.QLineEdit.Password)
        pw = pw.strip()
        if pw == "":
            return

        if self._manager.check_password(locker_id, pw):
            dialog = PromptDialog(self, "Enter The New Name and Password")
            response = dialog.get_results()

            if not response:
                return
            name, pw, cpw = response

            if name == "" or pw == "" or cpw == "":
                self.__show_error("Fields cannot be empty!")
                return

            # show error if the password and confirm password don't match
            if pw != cpw:
                self.__show_error("Confirm Password does not match!")
                return

            # try to add the new locker, if not successful then show error
            if not self._manager.change_name(locker_id, name):
                self.__show_error("Name already existed!")
                return
            self._manager.change_password(locker_id, pw)

            label = self._label_map[locker_id]
            label.setText(name)

        else:
            self.__show_error("Incorrect Password!")



    def __on_delete_button_clicked(self, source) -> None:
        """
        handle the event when the locker delete button is clicked
        :param source: the button that was clicked
        """
        locker_id = self._del_btn_map[source]
        locker_name = self._label_map[locker_id].text()
        pw, _ = QInputDialog.getText(self, "Enter Password",
                                     f"Please enter the password for locker \"{locker_name}\"",
                                     QtWidgets.QLineEdit.Password)
        if not self._manager.check_password(locker_name, pw):
            self.__show_error("Password does not match")
            return

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle("Delete Confirm")
        msg_box.setInformativeText(f"Are you sure you want to delete locker \"{locker_name}\"")
        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        response = msg_box.exec_()

        if response == QMessageBox.No:
            return

        if not self._manager.remove_locker(locker_id):
            self.__show_error("An error occurred when deleting the locker!")
            return
        row = self._row_map[locker_id]
        row.deleteLater()
        self.row_number -= 1



    @staticmethod
    def __show_error(message: str) -> None:
        """
        show a small popup window to inform the error to the user
        :param message: the message to be shown
        """
        err_box = QMessageBox()
        err_box.setIcon(QMessageBox.Critical)
        err_box.setText("Error")
        err_box.setInformativeText(message)
        err_box.exec_()



    def closeEvent(self, event) -> None:
        """
        handle the window close event
        :param event: the close event
        """
        reply = QMessageBox.question(self, "Quit Confirm",
                                     "Are you sure you want to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self._manager.save()
            if not type(event) == bool:
                event.accept()
            else:
                sys.exit()
        else:
            if not type(event) == bool:
                event.ignore()
