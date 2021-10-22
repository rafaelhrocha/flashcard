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


class Window_flashcard(Ui_MainWindow):
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
        self.gif_run(self.intruction_gif)

    def gif_run(self, gif_img):
        ui.movie = QMovie(gif_img)
        ui.label_gif.setMovie(ui.movie)
        ui.movie.start()

    def clicked_buttons(self):
        ui.button_start.clicked.connect(self.start_download)
        ui.button_cancel.clicked.connect(self.set_initial_window)
        # ui.button_confirm.clicked.connect(self.confirm)


    def start_download(self):
        ui.button_start.setVisible(False)
        ui.label_gif.setVisible(False)
        ui.label_infos.setVisible(True)
        print("START DOWNLOAD")
        
        try: 
            self.hostname = self.if_sd_connect()
            self.station = self.api_eStation(self.hostname)
            
            ui.button_confirm.setVisible(True)
            ui.button_cancel.setVisible(True)
            ui.label_instruction.setText("CARTAO ENCONTRADO: " + self.hostname)
            ui.label_infos.setText("POSTO: " + self.station + "\n\nDESEJA INICIAR O DOWNLOAD?")

        except Exception as e : 
            print("EXCEPTION: " + str(e))

            ui.button_confirm.setVisible(False)
            ui.label_instruction.setVisible(True)
            ui.button_cancel.setVisible(True)
            
            if str(e) == "No JSON object could be decoded":
                ui.label_instruction.setText("ERROR\nREDE NAO ENCONTRADA")
                ui.label_infos.setText("AGUARDE E TENTE NOVAMENTE\n\nSE  O PROBLEMA PERSISTIR ENTRE EM CONTATO COM O TIME DE SUPORTE DO ALL IN ONE")
                
            if e.args[0] == 2:
                ui.label_instruction.setText("ERROR CARTAO NAO ENCONTRADO")
                ui.label_infos.setText("INSIRA O CARTAO SD CORRETAMENTE\nE TENTE NOVAMENTE")

            else:
                ui.label_instruction.setText("ERROR\n")
                ui.label_infos.setText(str(e.args))

    
                

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    display = Window_flashcard()
    display.set_variables()
    display.set_initial_window()
    display.clicked_buttons()


    MainWindow.showFullScreen()
    sys.exit(app.exec_())