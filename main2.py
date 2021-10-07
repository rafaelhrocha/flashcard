# --------------------------------------------------------------------------
#                           JABIL DO BRASIL - BELO
# 
#   SD Card Download - Suport for flash in SD Card on raspberrys
#   
#
#   Developed by: Automation Team - Factory of future - Jabil Belo
#   Version: 1.0     
#   Last change: 28/07/2021
#   Last change responsible: Rafael Rocha
# --------------------------------------------------------------------------

# imports
from software_SD_Card import *
from PyQt5.QtGui import QMovie # install: sudo apt install python-pyqt5
import requests # install: sudo apt install python-requests
import json
import threading
import shutil
import sys
import time
import os


class Card(Ui_MainWindow):
    def set_variables(self):
        self.intruction_gif = "./images/instruction_gif.gif"
        self.load_gif = "./images/loading.gif"
        self.hostfile = "./images/media/pi/boot/hostname"
        self.api_url = ''
        self.flash_command = ''
        self.file_aio = ''
        self.file_raspad = ''
        self.sd_file = ''

    def set_initial_window(self):
        pass


    