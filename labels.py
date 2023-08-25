# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 09:24:55 2021

@author: A.Martinez
"""

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QRect, Qt, QPoint
from PyQt5.QtGui import QPainter, QPen

class painterX(QPainter):    
    pass

# Creo una subclase de QLabel para poder crear una etiqueta personalizada para poder mostrar imagenes y que el usuario pueda
# seleccionar partes de la imagen con el mause
class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    # Inicializo las instancias con los valores predeterminados del cuadro de la ui y otras instancias necesarias
    def __init__(self,x):
        super().__init__()
        self.dimensionX = 550
        self.dimensionY = 522
        self.dimensionXImg = 500
        self.dimensionYImg = 500
        self.listaRect = []
        self.factor = 1
        self.rect = 0
        self.flag2 = False
        self.begin = QPoint()
        self.end = QPoint()

        # Controlador de evento click, esta funcion espera doble click derecho
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.RightButton:
            print("doble")

    # Controlador de evento click, esta funcion espera a presionar el click izquierdo y toma los valores donde se realiza
    # Termina cuando suelta y se activa la funcion mouseReleaseEvent
    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.flag = True
            self.x0 = event.x()
            self.y0 = event.y()

    # Controlador de evento click, esta funcion espera a soltar el click izquierdo, cambia el valor de bandera
    def mouseReleaseEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.flag = False

    # Captura el movimiento del mouse solo cuando la bandera es true, es decir cuando se mantiene presionado el click derecho
    def mouseMoveEvent(self,event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    # Este método dibuja un rectángulo rojo en la etiqueta utilizando las coordenadas almacenadas en los atributos x0, y0, x1 e y1.
    # También calcula las coordenadas del rectángulo en relación con las dimensiones de la imagen.
    def paintEvent(self, event):
        super().paintEvent(event)
        self.rect =QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))

        painter = painterX(self)
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        painter.drawRect(self.rect)
        
        xRatio = self.dimensionXImg / self.dimensionX
        yRatio = self.dimensionYImg / self.dimensionY
        self.x = self.rect.x() * xRatio
        self.y = self.rect.y() * yRatio
        self.w = self.rect.width() * xRatio
        self.h = self.rect.height() * yRatio
        # print(self.x,self.y,self.x+self.w,self.y+self.h)
        # print(self.rect)
            
    # Permiten modificar las dimensiones de la imagen
    def modifDimImage(self, xdim, ydim):
        self.dimensionXImg = xdim
        self.dimensionYImg = ydim
        
    # Devuelve las coordenadas del rectángulo dibujado
    def obtenerRectangulo(self):
        return int(self.x), int(self.y), int(self.w), int(self.h)
            
    # Modifica las dimensiones de la etiqueta y el factor de escala
    def modificar(self,dimensionX,dimensionY, factor ):
        self.dimensionX = dimensionX
        self.dimensionY = dimensionY
        self.factor = factor