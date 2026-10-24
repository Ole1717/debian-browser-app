# Independent Browser for Debian

A lightweight, standalone browser application built with Python and QtWebEngine. It supports multiple search providers, tab navigation, and a clean Debian package layout for installation as a `.deb` package.

## Features

- Independent browser GUI
- Multiple search providers:
  - Google
  - DuckDuckGo
  - Bing
  - Yandex
- Tabbed browsing
- Address bar with URL and search support
- Back / forward / reload / home buttons
- Debian packaging ready

## Requirements

On Debian or Ubuntu:

```bash
sudo apt update
sudo apt install build-essential debhelper dh-python python3-dev python3-setuptools python3-pyqt5 python3-pyqt5.qtwebengine
```

## Run locally

```bash
python3 -m browser_app.main
```

## Build Debian package

```bash
dpkg-buildpackage -us -uc
```

This will generate a `.deb` package in the parent directory.

## Install package

```bash
sudo dpkg -i ../browser-app_*.deb
```

## Notes

This project is intentionally simple and independent: it does not require a bundled browser engine to be written from scratch. It is a polished Qt-based browser app with custom search engine selection and Debian packaging support.
