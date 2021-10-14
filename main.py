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

#variables
global host_file, apu_url, flash_command, load_gif, inst_gif, file_raspberry, file_raspad

inst_gif = "./images/instruction_gif.gif"
load_gif = "./images/loading.gif"
host_file  = "/media/pi/boot/hostname" # raspberry name
api_url = "http://brbelm0apps02.corp.jabil.org/AIOService/Estation/GetEquipmentByHostname/" 
flash_command = "sudo flash -f -d /dev/sdb ./b28686c2-213e-11ea-b32c-0242ac110002.img"
file_raspberry = "./modeloAIO/boot/"
file_raspad = "./modeloRaspad/boot/"
sd_file = "/media/pi/boot/"

#list the images options
def config():
    ui.comboBox.addItems(["POSTO DE ALL IN ONE","POSTO DE RASPAD"])

# connect all the buttons
def buttons():
    ui.button_start.clicked.connect(start)
    ui.button_cancel.clicked.connect(init_window)
    ui.button_confirm.clicked.connect(confirm)

def start():
    ui.button_start.setVisible(False)
    ui.label_gif.setVisible(False)
    ui.label_infos.setVisible(True)
    
    try: 
        hostname = if_sd_connect()
        station = api_estation(hostname)
        
        global saved_hostname
        saved_hostname = hostname
        
        ui.button_confirm.setVisible(True)
        ui.button_cancel.setVisible(True)
        ui.label_instruction.setText("CARTAO ENCONTRADO: " + hostname)
        ui.label_infos.setText("POSTO: " + station + "\n\nDESEJA INICIAR O DOWNLOAD?")
        
 
    except Exception as e : 
        ui.label_instruction.setVisible(True)
        ui.button_cancel.setVisible(True)
        ui.button_confirm.setVisible(False)        
        
        if str(e) == "No JSON object could be decoded":
            ui.label_instruction.setText("ERRO DE REDE ENCONTRADO")
            ui.label_infos.setText("AGUARDE E TENTE NOVAMENTE\n\nSE  O PROBLEMA PERSISTIR ENTRE EM CONTATO COM O TIME DE SUPORTE DO ALL IN ONE")
            
        if e.args[0] == 2:
            ui.label_instruction.setText("ERRO DE CARTAO NAO ENCONTRADO")
            ui.label_infos.setText("INSIRA O CARTAO SD CORRETAMENTE\nE TENTE NOVAMENTE")
            
        else:
            ui.label_instruction.setText("UM ERRO INESPERADO OCORREU")
            ui.label_infos.setText(str(e.args))
        
# draw the principal windown  
def init_window():
    if ui.button_cancel.text() == "CANCEL":
        gif_run(inst_gif)
        ui.label_infos.setVisible(False)
        ui.button_cancel.setVisible(False)
        ui.button_confirm.setVisible(False)
        ui.button_start.setVisible(True)
        ui.label_gif.setVisible(True)
        ui.comboBox.setVisible(False)
        ui.label_instruction.setText("INSIRA O CARTAO E PRESSIONE O BOTAO PARA INICIAR O DOWNLOAD")
        ui.button_confirm.setText("CONFIRM")
        
        
def confirm():
    if ui.button_confirm.text() == "CONFIRM":
        start_download()
    elif ui.button_confirm.text() == "OK":
            try:
                #check image select
                image_select = ui.comboBox.currentText()
                if image_select == "POSTO DE ALL IN ONE":
                    copy_files(file_raspberry)
                elif image_select == "POSTO DE RASPAD":
                    copy_files(file_raspad)
                
                card_dir = os.path.exists(host_file )  
                ui.comboBox.setVisible(False)
                ui.label_gif.setVisible(True)
                ui.label_gif.setPixmap(QtGui.QPixmap("./images/download_complete.png"))
                ui.label_instruction.setText("PROCESSO DE GRAVACAO CONCLUIDO\nREMOVA O CARTAO SD PARA ENCERRAR")
                ui.button_confirm.setText("FINALIZAR")
                
            except:
                ui.button_cancel.setVisible(False)
                ui.button_confirm.setVisible(True)
                ui.label_infos.setVisible(True)
                ui.button_confirm.setText("OK")
                ui.label_instruction.setText("ERRO: CARTAO NAO ENCONTRADO")
                ui.label_infos.setText("REMOVA E INSIRA O CARTAO SD\nE TENTE NOVAMENTE")
                
    elif ui.button_confirm.text() == "FINALIZAR":
        init_window()
        
                
def start_download():
    ui.label_infos.setVisible(False)
    ui.label_gif.setVisible(True)
    ui.button_confirm.setVisible(False)
    ui.button_cancel.setVisible(False)
    ui.label_instruction.setText("DOWNLOAD EM ANDAMENTO\nNAO REMOVA O CARTAO SD")
    
    gif_run(load_gif)
    
    # create a new trhead for initialize the flash in sd
    run = threading.Thread(target = flash_image)
    run.start()

def flash_image():
    os.system(flash_command)
    finish_download()
    
def finish_download():
    # unmount and mount sd card after flash
    os.system('sudo sh -c "echo 0 > /sys/devices/platform/soc/3f980000.usb/buspower"')
    time.sleep(5)
    os.system('sudo sh -c "echo 1 > /sys/devices/platform/soc/3f980000.usb/buspower"')
    
    ui.label_instruction.setText("DOWNLOAD ENCERRADO\nSELECIONE O POSTO CORRESPONDENTE: ")
    ui.button_confirm.setVisible(True)
    ui.label_gif.setVisible(False)
    ui.comboBox.setVisible(True)
    ui.button_confirm.setText("OK")
 
# get APIs information  - workstation 
def api_estation(hostname):
    url = api_url + hostname
    json_estation = requests.get(url)
    mnsg = json.loads(json_estation.content)
    return mnsg["Name"]

# check if sd card is connect
def if_sd_connect():
    print("")
    hostname_file  = open(host_file,"r")
    hostname = hostname_file.read(12)
    hostname_file.close()
    return hostname

# starts gif run
def gif_run(gif_img):
    ui.movie = QMovie(gif_img)
    ui.label_gif.setMovie(ui.movie)
    ui.movie.start()
    
def copy_files(image):
    
    root_src_dir = image    
    root_dst_dir = sd_file 

    #copy files to sd card 
    for src_dir, dirs, files in os.walk(root_src_dir): 
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        print(dst_dir)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            print(src_file)        
            dst_file = os.path.join(dst_dir, file_)
            print(dst_file)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)   
            
    # write in file the raspberry name ( hostname)
    hostname_file  = open(host_file ,"w")        
    hostname_file.write(saved_hostname)
    hostname_file.close() 

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    init_window()
    buttons()
    config()

    MainWindow.showFullScreen()
    sys.exit(app.exec_())
