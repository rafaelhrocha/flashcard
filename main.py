from software_SD_Card import *
from PyQt5.QtGui import QMovie


def config():
    ui.movie = QMovie("./instruction_sd.gif")
    ui.label_gif.setMovie(ui.movie)
    ui.movie.start()

    # ui.movie = QMovie("./loading.gif")
    # ui.gif.setMovie(ui.movie)
    # ui.movie.start()

    ui.label_infos.setVisible(False)
    ui.button_cancel.setVisible(False)
    ui.button_confirm.setVisible(False)

def buttons():
    ui.button_start.clicked.connect(start)
    ui.button_cancel.clicked.connect(cancel)
    ui.button_confirm.clicked.connect(confirm)

def start():
    ui.button_start.setVisible(False)
    try: # verifica se o cartao foi inserido
        if_sd_connect()
        ui.label_instruction.setText("CARTÃO ENCONTRADO NO CONECTOR USB")
        ui.label_infos.setVisible(True)
        ui.label_infos.setText("CARTÃO ENCONTRADO : " + hostname + "\nPOSTO: " + station)
        ui.label_gif.setVisible(False)
        ui.button_confirm.setVisible(True)
        ui.button_cancel.setVisible(True)
    except: 
        ui.label_instruction.setText("CARTÃO NÃO ENCONTRADO NO CONECTOR USB")
        ui.label_infos.setVisible(True)
        ui.label_infos.setText("POR FAVOR VERIFIQUE SE\n O CARTÃO ESTÁ CONECTADO CORRETAMENTE")
        ui.label_gif.setVisible(False)
        ui.button_cancel.setVisible(True)

def cancel():
    ui.label_infos.setVisible(False)
    ui.button_cancel.setVisible(False)
    ui.button_confirm.setVisible(False)
    ui.button_start.setVisible(True)
    ui.label_gif.setVisible(True)
    ui.label_instruction.setText("INSIRA O CARTÃO E PRESSIONE O BOTÃO PARA INICIAR O DOWNLOAD")

def confirm():
    if ui.button_confirm.setText == "CONFIRM":
        start_download()


def start_download():
    pass

def api_estation():
    #try:
    #except:
    pass

def if_sd_connect():
    pass

if __name__ == "__main__":
    import sys
    global hostname, station
    station = "INGBOXDIS006"
    hostname = "BRBELRASP191"
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    config()
    buttons()

    MainWindow.showFullScreen()
    sys.exit(app.exec_())
