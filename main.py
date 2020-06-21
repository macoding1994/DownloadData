# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import json
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import datetime


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.dirurl = None
        self.dirlist = [] # 去重
        self.marklist = [] # 目标
        self.url = 'https://cmr.earthdata.nasa.gov/search/concepts/{}?pretty=true'
        self.headers = {
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome / 73.0.3683.86 Safari/537.36",
        }

    def show_info(self, str):
        self.textBrowser.append(str)
        self.textBrowser.moveCursor(QTextCursor.End)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        '''生成文件按钮'''
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
        '''显示数据量'''
        self.textBrowser.clear()
        t = threading.Thread(target=self.aa)
        t.setDaemon(True)
        t.start()

    def aa(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        # logs = [json.loads(log['message'])['message'] for log in self.driver.get_log('performance')]
        # mark = self.driver.find_elements_by_xpath(
        #     '//*[@id="granule-results-table"]/div[1]/div/div[2]/div/div[2]/div/a/img')
        for log in self.driver.get_log('performance'):
            data = json.loads(log['message'])['message']
            try:
                pic_url = data.get('params').get('request').get('url')
            except Exception:
                continue
            else:
                try:
                    pic_id = re.match(
                        r'https://cmr.earthdata.nasa.gov/browse-scaler/browse_images/granules/(.*)-ASF\?h=85&w=85',
                        pic_url).group(1)
                    if not pic_url in self.marklist:
                        time.sleep(0.05)
                        self.marklist.append(pic_id)
                        self.show_info('发现ID: {}'.format(pic_id))
                except Exception:
                    continue
        self.show_info('文件数量为{}'.format(len(self.marklist)))
        # for var in mark:
        #     name = var.get_attribute('src').rsplit('/')[-1].rsplit('?')[0]
        #     self.show_info('{}.txt  已发现 '.format(name))
        # self.dirlist = os.listdir(self.dirurl)

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        '''下载'''
        t = threading.Thread(target=self.qiang1)
        t.setDaemon(True)
        t.start()

    def qiang(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        mark = self.driver.find_elements_by_xpath(
            '//*[@id="app"]/div[1]/div/div/section/section/div/div/div[1]/div[2]/div/div/div/div/ul/li/div[2]/a/img')
        url = 'https://cmr.earthdata.nasa.gov/search/concepts/{}.echo10?pretty=true'
        no = len(mark)
        no1 = 0
        for var in mark:
            name = var.get_attribute('src').rsplit('/')[-1].rsplit('?')[0]
            if not '{}.txt'.format(name) in self.dirlist:
                res = requests.get(url.format(name), headers=self.headers)
                if res.status_code == 200:
                    self.show_info('{}---OK'.format('{}'.format(name)))
                    with open('{}/{}.txt'.format(self.dirurl, name), 'w') as f:
                        f.write(res.text)
                else:
                    self.show_info('文件下载有误')
            else:
                self.show_info('{}.txt 已存在'.format(name))
            no1 += 1
            self.show_info('剩余---{}'.format(no - no1))

    def qiang1(self):
        if self.marklist:
            no = len(self.marklist)
            no1 = 0
            self.show_info('开始下载文件')
            self.headers.setdefault('origin','https://search.earthdata.nasa.gov')
            url = 'https://cmr.earthdata.nasa.gov/search/concepts/{}-ASF.umm_json?pretty=true'
            for mark in self.marklist:
                if not '{}.txt'.format(mark) in os.listdir(self.dirurl):
                    try:
                        res = requests.get(url.format(mark),headers=self.headers)
                    except Exception:
                        self.show_info('{}文件请求有误'.format(mark))
                        continue
                    if res.status_code == 200:
                        time.sleep(0.1)
                        self.show_info('{}---OK'.format('{}'.format(mark)))
                        with open('{}/{}.txt'.format(self.dirurl, mark), 'w') as f:
                            f.write(res.text)
                    else:
                        self.show_info('文件下载有误')
                else:
                    time.sleep(0.1)
                    self.show_info('{}.txt 已存在'.format(mark))
                no1 += 1
                time.sleep(0.1)
                self.show_info('剩余---{}'.format(no - no1))


    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        '''开启浏览器'''
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.dirurl}
        options.add_experimental_option('prefs', prefs)
        caps = {
            'browserName': 'chrome',
            'loggingPrefs': {
                'browser': 'ALL',
                'driver': 'ALL',
                'performance': 'ALL',
            },
            'goog:chromeOptions': {
                'perfLoggingPrefs': {
                    'enableNetwork': True,
                },
                'w3c': False,
            },
        }
        self.driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver.exe',desired_capabilities=caps)
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
