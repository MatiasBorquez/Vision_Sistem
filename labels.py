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

class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False


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
        
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.RightButton:
            print("doble")


    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.flag = True
            self.x0 = event.x()
            self.y0 = event.y()


    def mouseReleaseEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.flag = False


    def mouseMoveEvent(self,event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()


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
            
            
    def modifDimImage(self, xdim, ydim):
        self.dimensionXImg = xdim
        self.dimensionYImg = ydim
        
        
    def obtenerRectangulo(self):
        return int(self.x), int(self.y), int(self.w), int(self.h)
            
            
    def modificar(self,dimensionX,dimensionY, factor ):
        self.dimensionX = dimensionX
        self.dimensionY = dimensionY
        self.factor = factor