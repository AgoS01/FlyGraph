import csv
import os
import sqlite3
import sys

import numpy as np
import pyqtgraph as pg
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import *


class FlyGraph(QMainWindow):
    def __init__(self):
        super(FlyGraph, self).__init__()
        uic.loadUi("interface.ui", self)
        self.setObjectName('Flygraph')
        self.setWindowTitle('FlyGraph')
        self.color = ['#000000', '#ff0000']
        self.coords_ = []
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.new_file.clicked.connect(self.nfile)
        self.c2.clicked.connect(self.new_color)
        self.c3.clicked.connect(self.new_color)
        self.start.clicked.connect(self.create)
        self.info.clicked.connect(self.inf)
        self.graphicsView.setBackground('w')
        self.con = sqlite3.connect("file_history.db")
        self.cur = self.con.cursor()
        self.x_num = None
        self.y_num = None
        self.y2_num = None
        self.pen = None
        self.data_inuse = None
        self.nfile()

    def nfile(self):
        self.data = []
        self.filename = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        with open(self.filename, encoding="utf8") as csvfile:
            self.current_file = os.path.abspath(self.filename)
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for index, row in enumerate(reader):
                self.data.append(row)
        dat = (self.filename, self.current_file)
        self.cur.execute("INSERT INTO file_hist(file_name, path) VALUES(?,?)", dat)
        self.con.commit()
        self.x_st.clear()
        self.y_st.clear()
        self.y2_st.clear()
        self.y2_st.addItems(['none'])
        self.x_st.addItems([f"столбец {i}: {self.data[0][i]}" for i in range(len(self.data[0]))])
        self.y_st.addItems([f"столбец {i}: {self.data[0][i]}" for i in range(len(self.data[0]))])
        self.y2_st.addItems([f"столбец {i}: {self.data[0][i]}" for i in range(len(self.data[0]))])

    def inf(self):
        msg = QMessageBox()
        msg.setWindowTitle("info")
        msg.setText("Created by Anatoly Fomin in 2022")
        msg.exec_()

    def new_color(self):
        if self.sender().text() == 'цвет 1':
            self.color[0] = QColorDialog.getColor().name()
            self.c2.setStyleSheet(f'color: {self.color[0]}')
        elif self.sender().text() == 'цвет 2':
            self.color[1] = QColorDialog.getColor().name()
            self.c3.setStyleSheet(f'color: {self.color[1]}')

    def create(self, **kwargs):
        self.x_num = int(str(self.x_st.currentText())[8])
        self.y_num = int(str(self.y_st.currentText())[8])
        self.y2_num = None
        self.graphicsView.addLegend()
        self.graphicsView.showGrid(x=True, y=True)
        if not self.y2_st.currentText() == 'none':
            self.y2_num = int(str(self.y2_st.currentText())[8])
        self.graphicsView.clear()
        self.pen = pg.mkPen(color=self.color[0])
        self.data_inuse = np.array([[i[self.x_num], i[self.y_num]] for i in self.data], float)
        self.graphicsView.plot(self.data_inuse, pen=self.pen, name="график 1")
        try:
            self.pen = pg.mkPen(color=self.color[1])
            self.data_inuse = np.array([[i[self.x_num], i[self.y2_num]] for i in self.data], float)
            self.graphicsView.plot(self.data_inuse, pen=self.pen, name="график 2")
        except:
            Exception  # needed if y2_num is still NoneType
        styles = {'color': 'b', 'font-size': '20px'}
        if self.y2_num:
            self.graphicsView.setLabel('left', self.name2.text() + '  ;  ' + self.name3.text(), **styles)
        else:
            self.graphicsView.setLabel('left', self.name2.text(), **styles)
        self.graphicsView.setLabel('bottom', self.name1.text(), **styles)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FlyGraph()
    ex.show()
    sys.exit(app.exec())
