import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="WebsiteWatcher",
    version="0.0.1",
    author="Yu-Yueh Liu",
    author_email="yu-yueh@hotmail.com",
    description=("WebsiteWatcher is a Python CLI tool for running a website watcher."),
    keywords="python website watcher cli",
    packages=find_packages(
        include=[
            "websiteWatcher",
            "websiteWatcher.common",
            "websiteWatcher.settings",
            "websiteWatcher.watchers",
        ]
    ),
    long_description=read("README.md"),
    install_requires=[
        "beautifulsoup4==4.6.0",
        "selenium==3.141.0",
        "sendgrid==6.4.6",
        "toml==0.10.1",
        "ConfigArgParse==0.11.0",
    ],
    setup_requires=["flake8"],
    entry_points={
        "console_scripts": ["websiteWatcher=websiteWatcher.watcher_cli:main"]
    },
)
