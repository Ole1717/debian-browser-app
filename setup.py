# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="browser-app",
    version="1.0.0",
    description="Independent Debian browser with multiple search engines",
    packages=["browser_app"],
    install_requires=["PyQt5>=5.15.10"],
    entry_points={
        "console_scripts": [
            "browser-app=browser_app.main:main",
        ]
    },
)
