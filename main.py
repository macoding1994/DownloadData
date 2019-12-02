# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import os
import re
import sys
import threading
import time
import requests
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
        self.dirurl = None
        self.dirlist = []

        self.url = 'https://cmr.earthdata.nasa.gov/search/concepts/{}?pretty=true'
        self.headers = {
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome / 73.0.3683.86 Safari/537.36",
            "Origin: https: // search.earthdata.nasa.gov"
        }

    def show_info(self, str):
        self.textBrowser.append(str)
        self.textBrowser.moveCursor(QTextCursor.End)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        if self.lineEdit.text():
            if not os.path.exists(self.lineEdit.text()):
                os.mkdir(self.lineEdit.text())
                self.dirurl = self.lineEdit.text()
            self.show_info('当前路径为：' + os.path.abspath('./{}'.format(self.lineEdit.text())))
            self.dirurl = os.path.abspath('./{}'.format(self.lineEdit.text()))
        else:
            if self.dirurl:
                self.show_info(self.dirurl)
            else:
                self.show_info('请输入文件夹名')


    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        mark = self.driver.find_elements_by_xpath('//*[@id="tbody"]/tr/td/a')
        self.show_info('文件数量为{}'.format(len(mark)))
        self.dirlist = os.listdir(self.dirurl)
        print(self.dirlist)
        with open('{}\{}.txt'.format(self.dirurl,time.time()),'w',encoding='utf-8') as f:
            f.write('{}'.format(self.driver.find_element_by_class_name('granule-details-info__content').text))





    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        t = threading.Thread(target=self.qiang)
        t.setDaemon(True)
        t.start()

    def qiang(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        mark = self.driver.find_elements_by_xpath('//*[@id="tbody"]/tr/td/a')
        for var in mark:
            if not var.get_attribute('href').rsplit('/')[-1] in self.dirlist:
                var.click()
                self.show_info('{}已下载'.format(var.get_attribute('href')))
                time.sleep(2.5)
            else:
                self.show_info('{}已存在'.format(var.get_attribute('href')))




    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.dirurl}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(chrome_options=options,executable_path='./chromedriver.exe')
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