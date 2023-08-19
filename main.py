import sys
from interfaz import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from mTk import selectFile
import visionLib

class aplicacionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dialogo = Ui_MainWindow()
        self.dialogo.setupUi(self)
        # Medidas de la imagen
        self.ancho = 550
        self.alto = 522
        self.inicializar()

        #Configurar cuando se llama el simulador o la camara
        self.dialogo.simuladorChB.clicked.connect(self.simuladorClicked)
        self.dialogo.capturarImagenButton.clicked.connect(self.capturarImagen)
        self.dialogo.activarColorChB.clicked.connect(self.colorClicked)
        self.dialogo.activarColorChB.clicked.connect(self.habilitarTest)
        self.dialogo.activarPresenciaChB.clicked.connect(self.presenciaClicked)
        self.dialogo.activarPresenciaChB.clicked.connect(self.habilitarTest)
        self.dialogo.SelectImageButton.clicked.connect(self.simuladorImagen)

    def inicializar(self):
        #Desabilitar las ventanas
        self.dialogo.tabWidget.setTabEnabled(1,False)
        self.dialogo.tabWidget.setTabEnabled(2, False)
        self.dialogo.tabWidget.setTabEnabled(3, False)
        self.dialogo.SelectImageButton.setEnabled(False)

    def simuladorClicked(self):
        x = self.dialogo.simuladorChB.isChecked()
        # Deshabilita las camaras al seleccionar el simulador
        if x == True:
            self.dialogo.SelectImageButton.setEnabled(True)
            self.dialogo.capturarImagenButton.setEnabled(False)
            self.dialogo.camarasCBox.setEnabled(False)
            self.dialogo.camarasCBox.clear()
            self.dialogo.cargarImagenTest.setEnabled(False)
            self.dialogo.realizarTestButton.setDisabled(True)
        # habilita las camaras al seleccionar el simulador
        else:
            self.dialogo.SelectImageButton.setEnabled(False)
            self.dialogo.capturarImagenButton.setEnabled(True)
            self.dialogo.camarasCBox.setEnabled(True)
            # lee las camaras disponibles en el sistama
            self.camarasDisponibles = visionLib.leerCamarasDisponibles()
            self.dialogo.camarasCBox.clear()
            self.dialogo.camarasCBox.addItems(self.camarasDisponibles)
            self.dialogo.cargarImagenTest.setDisabled(True)
            self.dialogo.realizarTestButton.setDisabled(False)

    def capturarImagen(self):
        camara = self.dialogo.camarasCBox.currentText()
        self.img, height, widht, bytesPerLine = visionLib.capturarImagenShow(camara)
        self.mostrarImagenes(self.img, height, widht, bytesPerLine)

    def mostrarImagenes(self, img, height, widht, bytesPerLine):
        QImg = QImage(img.data, widht, height, bytesPerLine, QImage.Format_RGB888)
        self.pixmap = QPixmap.fromImage(QImg)
        self.dialogo.imagenCapturadaLabel.setPixmap(self.pixmap)
        self.dialogo.imagenCapturadaLabel.setCursor(Qt.CrossCursor)
        self.dialogo.imagenCapturadaLabel.setFixedWidth(self.ancho)
        self.dialogo.imagenCapturadaLabel.setFixedHeight(self.alto)

        self.dialogo.imagenColorLabel.modifDimImage(widht, height)
        self.pixmap = QPixmap.fromImage(QImg)
        self.dialogo.imagenColorLabel.setPixmap(self.pixmap)
        self.dialogo.imagenColorLabel.setCursor(Qt.CrossCursor)
        self.dialogo.imagenColorLabel.setFixedWidth(self.ancho)
        self.dialogo.imagenColorLabel.setFixedHeight(self.alto)

        self.dialogo.imagenPresenciaLabel.modifDimImage(widht, height)
        self.pixmap = QPixmap.fromImage(QImg)
        self.dialogo.imagenPresenciaLabel.setPixmap(self.pixmap)
        self.dialogo.imagenPresenciaLabel.setCursor(Qt.CrossCursor)
        self.dialogo.imagenPresenciaLabel.setFixedWidth(self.ancho)
        self.dialogo.imagenPresenciaLabel.setFixedHeight(self.alto)

    def colorClicked(self):
        x = self.dialogo.activarColorChB.isChecked()
        if x == True:
            self.dialogo.tabWidget.setTabEnabled(1, True)
        else:
            self.dialogo.tabWidget.setTabEnabled(1, False)

    def presenciaClicked(self):
        x = self.dialogo.activarPresenciaChB.isChecked()
        if x == True:
            self.dialogo.tabWidget.setTabEnabled(2, True)
        else:
            self.dialogo.tabWidget.setTabEnabled(2, False)

    def habilitarTest(self):
        if(self.dialogo.activarColorChB.isChecked() == True or self.dialogo.activarPresenciaChB.isChecked() == True):
            self.dialogo.tabWidget.setTabEnabled(3, True)
        else:
            self.dialogo.tabWidget.setTabEnabled(3, False)

    def simuladorImagen(self):
        ruta = selectFile()
        self.img, height, width, bytesPerLine = visionLib.capturarImagenSim(ruta)
        self.mostrarImagenes(self.img, height, width, bytesPerLine)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialogo = aplicacionWindow()
    dialogo.show()
    sys.exit(app.exec_())