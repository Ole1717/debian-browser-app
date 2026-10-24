# -*- coding: utf-8 -*-

import sys
from urllib.parse import quote_plus
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QComboBox, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView


SEARCH_ENGINES = {
    "Google": "https://www.google.com/search?q={query}",
    "DuckDuckGo": "https://duckduckgo.com/?q={query}",
    "Bing": "https://www.bing.com/search?q={query}",
    "Yandex": "https://yandex.com/search/?text={query}",
}


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Independent Browser")
        self.resize(1280, 900)

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        self.toolbar = QWidget()
        self.toolbar_layout = QHBoxLayout(self.toolbar)

        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.reload_btn = QPushButton("⟳")
        self.home_btn = QPushButton("Home")

        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter URL or search")
        self.address_bar.returnPressed.connect(self.load_input)

        self.engine_selector = QComboBox()
        self.engine_selector.addItems(SEARCH_ENGINES.keys())
        self.engine_selector.setCurrentText("Google")

        self.go_btn = QPushButton("Go")
        self.go_btn.clicked.connect(self.load_input)

        self.toolbar_layout.addWidget(self.back_btn)
        self.toolbar_layout.addWidget(self.forward_btn)
        self.toolbar_layout.addWidget(self.reload_btn)
        self.toolbar_layout.addWidget(self.home_btn)
        self.toolbar_layout.addWidget(self.address_bar)
        self.toolbar_layout.addWidget(self.engine_selector)
        self.toolbar_layout.addWidget(self.go_btn)

        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.reload_btn.clicked.connect(self.browser.reload)
        self.home_btn.clicked.connect(self.go_home)

        self.addToolBar(self.toolbar)

        self.address_bar.setText("https://www.google.com")
        self.browser.setUrl(QUrl("https://www.google.com"))

    def normalize_url(self, value):
        text = value.strip()
        if not text:
            return "https://www.google.com"

        if "://" in text:
            return text if text.startswith(("http://", "https://")) else "https://" + text

        if "." in text or "/" in text:
            return "https://" + text

        selected_engine = self.engine_selector.currentText()
        base_url = SEARCH_ENGINES[selected_engine]
        query = quote_plus(text)
        return base_url.format(query=query)

    def load_input(self):
        url = self.normalize_url(self.address_bar.text())
        self.browser.setUrl(QUrl(url))
        self.address_bar.setText(url)

    def go_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.address_bar.setText("https://www.google.com")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Independent Browser")
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())
