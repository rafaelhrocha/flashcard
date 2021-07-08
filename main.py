from software_SD_Card import *
from PyQt5.QtGui import QMovie


def config():
    ui.movie = QMovie("./instruction_sd.gif")
    ui.label_gif.setMovie(ui.movie)
    ui.movie.start()

    ui.movie = QMovie("./loading.gif")
    ui.label_load.setMovie(ui.movie)
    ui.movie.start()

    ui.label_confirm.setVisible(False)
    ui.button_no.setVisible(False)
    ui.button_yes.setVisible(False)
    ui.button_download.setVisible(False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    config()

    MainWindow.showFullScreen()
    sys.exit(app.exec_())
