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
from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QApplication
from selenium.webdriver.support.wait import WebDriverWait

from Ui_main import Ui_MainWindow
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import datetime


class MainWindow(QMainWindow, Ui_MainWindow):
    a = pyqtSignal()
    b = pyqtSignal()
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.dirurl = None
        self.dirlist = []
        self.stationlist = []

        self.url = 'https://cmr.earthdata.nasa.gov/search/concepts/{}?pretty=true'
        self.headers = {
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome / 73.0.3683.86 Safari/537.36",
            "Origin: https: // search.earthdata.nasa.gov"
        }
        self.a.connect(self.findno1)
        self.b.connect(self.findno2)

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
        t = threading.Thread(target=self.findno)
        t.setDaemon(True)
        t.start()

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        t = threading.Thread(target=self.qiang)
        t.setDaemon(True)
        t.start()

    def qiang(self):
        while 1:
            try:
                print(self.driver.find_element_by_xpath('//*[@id="tooltipDialog"]/div[1]/div/div/b').text)
            except Exception:
                pass

    def findno(self):
        self.stationlist = []
        self.driver.switch_to.window(self.driver.window_handles[-1])
        marklist = self.driver.find_elements_by_tag_name('path')
        for mark in marklist:
            if not mark.get_attribute('fill') == 'rgb(255, 0, 0)':
                ActionChains(self.driver).move_to_element(mark).perform()
                self.mark = True
                self.a.emit()
                time.sleep(2)
        else:
            self.mark = False
            with open('station.txt','a') as f:
                for station in self.stationlist:
                    f.write(str(station) + '\n')
            self.show_info('站点已添加')

    def findno1(self):
        while self.mark:
            try:
                data = self.driver.find_element_by_xpath('//*[@id="tooltipDialog"]/div[1]/div/div/b').text
                if data:
                    self.stationlist.append(data)
            except Exception:
                pass

    def findno2(self):
        self.mark = False

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.dirurl}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver.exe')
        self.driver.implicitly_wait(3)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        self.driver.get('https://www.ndbc.noaa.gov/')


def main():
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()