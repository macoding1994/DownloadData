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
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer
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

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.dirurl = None
        self.dirlist = []
        self.stationlist = []

        self.url = 'https://www.ndbc.noaa.gov/station_page.php?station={}'
        self.headers = {
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome / 73.0.3683.86 Safari/537.36"
        }
        self.countno = 0
        self.a.connect(self.on_pushButton_5_clicked)

    def show_info(self, str):
        self.countno += 1
        self.textBrowser.append('{}:{}'.format(self.countno, str))
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
        t = threading.Thread(target=self.download)
        t.setDaemon(True)
        t.start()

    def download(self):
        savelist = os.listdir(self.dirurl)
        try:
            with open('{}\\faile.txt'.format(self.dirurl), 'r', encoding='utf-8') as f:
                failelist = f.readlines()
        except Exception:
            failelist = []
        for station in self.stationlist:
            name = station.split(' ')[-1]
            if not (name + '.txt' in savelist or name+'\n' in failelist):
                res = requests.get(self.url.format(name), headers=self.headers)
                if res.status_code == 200:
                    self.success(name, res.text)
                    self.show_info('{}成功'.format(name))
                else:
                    self.faile(name)
                    self.show_info('{}失败'.format(name))
            else:
                self.show_info('{}过滤'.format(name))

    def success(self, station, str):
        with open('{}\{}.txt'.format(self.dirurl, station), 'w', encoding='utf-8') as f:
            f.write(str)

    def faile(self, station):
        with open('{}\\faile.txt'.format(self.dirurl), 'a', encoding='utf-8') as f:
            f.write(str(station) + '\n')

    def qiang(self):
        while self.start:
            try:
                data = self.driver.find_element_by_xpath('//*[@id="tooltipDialog"]/div[1]/div/div/b').text
                if data:
                    self.stationlist.append(data)
                    self.show_info(str(data))
            except Exception:
                pass

    def findno(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        marklist = self.driver.find_elements_by_tag_name('path')
        for mark in marklist:
            if not mark.get_attribute('fill') == 'rgb(255, 0, 0)':
                for _ in range(5):
                    ActionChains(self.driver).move_to_element(mark).perform()
                    time.sleep(0.5)
        else:
            self.a.emit()

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

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        if self.pushButton_5.text() == '数据追踪':
            self.start = True
            t = threading.Thread(target=self.qiang)
            t.setDaemon(True)
            t.start()
            self.pushButton_5.setText('暂停')
        else:
            self.pushButton_5.setText('数据追踪')
            self.start = False
            self.countno = 0
            self.textBrowser.clear()
            self.stationlist = list(set(self.stationlist))
            for station in self.stationlist:
                self.show_info('{}--{}'.format(self.stationlist.index(station), station))


def main():
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
