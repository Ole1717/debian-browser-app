# -*- coding: utf-8 -*-

import sys
from urllib.parse import quote_plus

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView


SEARCH_ENGINES = {
    "Google": "https://www.google.com/search?q={query}",
    "DuckDuckGo": "https://duckduckgo.com/?q={query}",
    "Bing": "https://www.bing.com/search?q={query}",
    "Yandex": "https://yandex.com/search/?text={query}",
}

HOME_URL = "https://www.google.com"


class BrowserTab(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.browser = QWebEngineView()
        self.browser.urlChanged.connect(self.update_address)
        self.browser.titleChanged.connect(self.update_tab_title)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)

    def update_address(self, url):
        if self.window.tabs.currentWidget() is self:
            self.window.address_bar.setText(url.toString())

    def update_tab_title(self, title):
        index = self.window.tabs.indexOf(self)
        if index >= 0:
            if title:
                self.window.tabs.setTabText(index, title[:30])
            else:
                self.window.tabs.setTabText(index, "New tab")

    def load_url(self, url):
        self.browser.setUrl(QUrl(url))


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Independent Browser")
        self.resize(1280, 900)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.setCentralWidget(self.tabs)

        self.toolbar = self.addToolBar("Navigation")
        self.toolbar.setMovable(False)

        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.reload_btn = QPushButton("⟳")
        self.home_btn = QPushButton("Home")
        self.new_tab_btn = QPushButton("+ Tab")

        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter URL or search")
        self.address_bar.returnPressed.connect(self.load_address)

        self.engine_selector = QComboBox()
        self.engine_selector.addItems(list(SEARCH_ENGINES.keys()))
        self.engine_selector.setCurrentText("Google")

        self.go_btn = QPushButton("Go")
        self.go_btn.clicked.connect(self.load_address)

        self.toolbar.addWidget(self.back_btn)
        self.toolbar.addWidget(self.forward_btn)
        self.toolbar.addWidget(self.reload_btn)
        self.toolbar.addWidget(self.home_btn)
        self.toolbar.addWidget(self.new_tab_btn)
        self.toolbar.addWidget(self.address_bar)
        self.toolbar.addWidget(self.engine_selector)
        self.toolbar.addWidget(self.go_btn)

        self.back_btn.clicked.connect(self.go_back)
        self.forward_btn.clicked.connect(self.go_forward)
        self.reload_btn.clicked.connect(self.reload_page)
        self.home_btn.clicked.connect(self.go_home)
        self.new_tab_btn.clicked.connect(self.new_tab)

        self.new_tab()
        self.update_toolbar_state()

    def current_tab(self):
        return self.tabs.currentWidget()

    def create_tab(self, url=HOME_URL):
        tab = BrowserTab(self)
        self.tabs.addTab(tab, "New tab")
        self.tabs.setCurrentWidget(tab)
        tab.load_url(url)
        return tab

    def new_tab(self):
        self.create_tab(HOME_URL)
        self.update_toolbar_state()

    def close_tab(self, index):
        if self.tabs.count() == 1:
            self.close()
            return
        self.tabs.removeTab(index)
        self.update_toolbar_state()

    def on_tab_changed(self, index):
        self.update_toolbar_state()

    def update_toolbar_state(self):
        tab = self.current_tab()
        if tab is None:
            return

        page = tab.browser
        self.back_btn.setEnabled(page.history().canGoBack())
        self.forward_btn.setEnabled(page.history().canGoForward())
        self.address_bar.setText(page.url().toString())

    def go_back(self):
        tab = self.current_tab()
        if tab is not None:
            tab.browser.back()

    def go_forward(self):
        tab = self.current_tab()
        if tab is not None:
            tab.browser.forward()

    def reload_page(self):
        tab = self.current_tab()
        if tab is not None:
            tab.browser.reload()

    def go_home(self):
        tab = self.current_tab()
        if tab is not None:
            tab.load_url(HOME_URL)

    def normalize_url(self, value):
        text = value.strip()
        if not text:
            return HOME_URL

        if "://" in text:
            return text if text.startswith(("http://", "https://")) else "https://" + text

        if "." in text or "/" in text:
            return "https://" + text

        selected_engine = self.engine_selector.currentText()
        base_url = SEARCH_ENGINES[selected_engine]
        query = quote_plus(text)
        return base_url.format(query=query)

    def load_address(self):
        tab = self.current_tab()
        if tab is None:
            return
        url = self.normalize_url(self.address_bar.text())
        tab.load_url(url)
        self.address_bar.setText(url)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Independent Browser")
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())
