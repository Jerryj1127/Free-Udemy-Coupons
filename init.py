#!/usr/bin/env python3
import platform
import os
import getpass
from pathlib import Path

class init:
    """A class with a bunch of initializations and handy functions"""

    def __init__(self):
        self.os_name = platform.system()
        self.os_type = os.name
        self.username = getpass.getuser()

    def clrscr(self):
        if self.os_type == 'nt':
            os.system('cls')
        elif self.os_type == 'posix':
            os.system('clear')

    def chrome_version(self):
        if self.os_name == 'Darwin':
            installpath = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
        elif self.os_name == 'Windows':
            installpath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        elif self.os_name == 'Linux':
            installpath = "/usr/bin/google-chrome"
        else:
            return None
        ch_ver = os.popen(f"{installpath} --version").read().strip('Google Chrome ').strip()
        return ch_ver
    def create_folder(self,path_):
        if not os.path.isdir(path_):
            os.mkdir(path_)
    def getpath(self, folder='Documents'):
        location = os.path.join(Path.home(), folder)
        self.create_folder(location)
        return location

    def get_pdf_path(self, folder='Udemy Reports'):
        location = os.path.join(self.getpath(), folder)
        self.create_folder(location)
        return location


utils = init()