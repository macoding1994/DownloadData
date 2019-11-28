# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import os
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QApplication

from Ui_main import Ui_MainWindow
from selenium import webdriver
import datetime


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.url = None

    def show_info(self, str):
        self.textBrowser.append(str)
        self.textBrowser.moveCursor(QTextCursor.End)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        if self.lineEdit.text():
            if not os.path.exists(self.lineEdit.text()):
                os.mkdir(self.lineEdit.text())
                self.url = self.lineEdit.text()
            self.show_info('当前路径为：' + os.path.abspath('./{}'.format(self.lineEdit.text())))
            self.url = os.path.abspath('./{}'.format(self.lineEdit.text()))
        else:
            if self.url:
                self.show_info(self.url)
            else:
                self.show_info('请输入文件夹名')




    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        self.driver.find_element_by_xpath('//*[@id="tbody"]/tr[1]/td[1]/a')

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        pass


    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        self.driver = webdriver.Chrome(executable_path='./chromedriver.exe')
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }


def main():
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()