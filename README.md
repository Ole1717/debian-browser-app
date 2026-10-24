# Independent Browser for Debian

A lightweight browser app built with PyQt5 and QtWebEngine. It includes a built-in address bar, navigation controls, and multiple search engines:

- Google
- DuckDuckGo
- Bing
- Yandex

This project is designed to be packaged as a `.deb` for Debian-based systems.

## Features

- Simple tabless browser window
- Back / forward / reload navigation
- URL address bar
- Search provider selection
- Fast startup
- Easy Debian packaging

## Requirements

On Debian/Ubuntu:

```bash
sudo apt update
sudo apt install python3 python3-pyqt5 python3-pyqt5.qtwebengine
```

## Run locally

```bash
python3 -m browser_app.main
```

## Debian package build

From the project root:

```bash
sudo apt install build-essential debhelper dh-python python3-dev

dpkg-buildpackage -us -uc
```

This will produce a `.deb` package in the parent directory.

## App installation

```bash
sudo dpkg -i ../browser-app_*.deb
```

## Notes

This is a functional minimal browser, not a complete Chromium fork. It is a clean independent app interface built around QtWebEngine, with search engine switching and a Debian package layout.
