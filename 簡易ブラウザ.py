#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import (QWidget, QLineEdit, QGridLayout, QApplication, QPushButton, QDesktopWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

__program__ = 'PERSEPHONE'


class PersephoneWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        
        initurl = 'https://www.google.co.jp'

        # setting browser
        self.browser = QWebEngineView()
        self.browser.load(QUrl(initurl))        
        self.browser.resize(1000, 600)
        self.browser.move(200, 200)
        self.browser.setWindowTitle(__program__)

        # setting button
        self.back_button = QPushButton('戻る')
        self.back_button.clicked.connect(self.browser.back)        
        self.forward_button = QPushButton('進む')
        self.forward_button.clicked.connect(self.browser.forward)
        self.reload_button = QPushButton('リロード(リフレッシュ)')
        self.reload_button.clicked.connect(self.browser.reload)
        self.url_edit = QLineEdit()
        self.move_button = QPushButton('移動')  # "move" -> "移動"
        self.move_button.clicked.connect(self.loadPage)

        # signal catch from moving web pages.
        self.browser.urlChanged.connect(self.updateCurrentUrl)

        # Connect the enter key press in the URL bar to loadPage method
        self.url_edit.returnPressed.connect(self.loadPage)  # EnterキーでURLを移動

        # setting layout
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.back_button, 1, 0)
        grid.addWidget(self.forward_button, 1, 1)
        grid.addWidget(self.reload_button, 1, 2)
        grid.addWidget(self.url_edit, 1, 3, 1, 10)
        grid.addWidget(self.move_button, 1, 14)
        grid.addWidget(self.browser, 2, 0, 5, 15)
        self.setLayout(grid) 
        self.resize(1200, 800)
        self.center()
        self.setWindowTitle(__program__)
        self.show()

    
    def center(self):
        ''' centering widget
        '''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def loadPage(self):
        ''' move web page which is set at url_edit
        '''
        # Get the text from the URL bar
        url_text = self.url_edit.text().strip()

        # Check if the URL starts with "http" or "https"
        if not url_text.startswith(('http://', 'https://')):
            # If it doesn't, prepend "https://"
            url_text = 'https://' + url_text

        # If the URL starts with "http://", replace it with "https://"
        if url_text.startswith('http://'):
            url_text = 'https://' + url_text[7:]

        # Load the page
        move_url = QUrl(url_text)
        self.browser.load(move_url)
        self.updateCurrentUrl()

    def updateCurrentUrl(self):
        ''' rewriting url_edit when you move different web page.
        '''
        self.url_edit.clear()
        self.url_edit.insert(self.browser.url().toString())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # setWindowIcon is a method for QApplication, not for QWidget
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'icon_persephone.png')
    app.setWindowIcon(QIcon(path))

    ex = PersephoneWindow()
    sys.exit(app.exec_())
