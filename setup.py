import os
from setuptools import setup, find_packages

from websiteWatcher.common.utils import read_file

root_dir = os.path.dirname(os.path.abspath(__file__))
requirementPath = f"{root_dir}/requirements.txt"
install_requires = []  # E.g. ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

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
    long_description=read_file(f"{root_dir}/README.md"),
    install_requires=install_requires,
    setup_requires=["flake8"],
)
