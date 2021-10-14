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
        self.api_url = "http://brbelm0apps02.corp.jabil.org/AIOService/Estation/GetEquipmentByHostname/"
        self.flash_command = "sudo flash -f -d /dev/sdb ./b28686c2-213e-11ea-b32c-0242ac110002.img"
        self.file_aio = "./modeloAIO/boot/"
        self.file_raspad = "./modeloRaspad/boot/"
        self.sd_file = "/media/pi/boot/"
        ui.comboBox.addItems(["POSTO DE ALL IN ONE","POSTO DE RASPAD"])

    def set_initial_window(self):
        ui.label_infos.setVisible(False)
        ui.button_cancel.setVisible(False)
        ui.button_confirm.setVisible(False)
        ui.button_start.setVisible(True)
        ui.label_gif.setVisible(True)
        ui.comboBox.setVisible(False)
        ui.label_instruction.setText("INSIRA O CARTAO E PRESSIONE O BOTAO PARA INICIAR O DOWNLOAD")
        ui.button_confirm.setText("CONFIRM")
        ui.comboBox.addItems(["POSTO DE ALL IN ONE","POSTO DE RASPAD"])

    def clicked_buttons(self):
        ui.button_start.clicked.connect(start)
        ui.button_cancel.clicked.connect(self.set_initial_window)
        ui.button_confirm.clicked.connect(confirm)
