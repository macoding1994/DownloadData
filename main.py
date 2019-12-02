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
        t = threading.Thread(target=self.findno)
        t.setDaemon(True)
        t.start()

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        t = threading.Thread(target=self.qiang)
        t.setDaemon(True)
        t.start()

    def qiang(self):
        length = len(self.dirlist)
        filelist = os.listdir(self.dirurl)
        for url in self.dirlist:
            if not url+'.txt' in filelist:
                res = requests.get(self.url.format(url), headers=self.headers)
                if res.status_code == 200:
                    with open('{}\{}.txt'.format(self.dirurl,url),'w',encoding='utf-8') as f:
                        f.write(res.text)
                    self.show_info('{}.txt  已下载，目前还剩{}未下载'.format(url,length - self.dirlist.index(url) -1))
                else:
                    self.show_info('{}.txt  下载失败，已添加错误列表'.format(url))
                    with open('{}\error.txt'.format(self.dirurl),'a',encoding='utf-8') as f:
                        f.write(url)
            else:
                self.show_info('{}.txt  已下载'.format(url))

    def findno(self):
        while 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            length = self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/section/header/div[3]/div/div/span/span').text
            imglist = self.driver.find_elements_by_xpath('//*[@id="app"]/div[1]/div/div/section/section/div/div/div[1]/div[2]/div/div/div/div/ul/li/div[2]/div[1]/img')
            self.show_info('已发现{}数据包'.format(len(imglist)))
            if not len(imglist) < int(length):
                break
        imglist = self.driver.find_elements_by_xpath(
            '//*[@id="app"]/div[1]/div/div/section/section/div/div/div[1]/div[2]/div/div/div/div/ul/li/div[2]/div[1]/img')
        self.dirlist = []
        for img in imglist:
            self.show_info(img.get_attribute('src').rsplit('/')[-1].rsplit('?')[0])
            self.dirlist.append(img.get_attribute('src').rsplit('/')[-1].rsplit('?')[0])
        else:
            self.show_info('该页面发现{}个数据包'.format(len(self.dirlist)))

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.dirurl}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver.exe')
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