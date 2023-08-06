import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, qApp, \
QDialog, QAction, QMenu, QInputDialog, QFileDialog, QMessageBox, QMainWindow, \
QLabel, QGridLayout, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from models import *
import scipy.io as sio
import random
import numpy as np
import tensorflow as tf
import AngelEncoder

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setMinimumSize(QSize(800, 350))
        self.setWindowTitle("PypeLearn - ML for time series")

        selectFile = QAction("Open File", self)
        selectFile.setShortcut('Cmd+O')
        selectFile.triggered.connect(self.openFileNamesDialog)

        saveFile = QAction("Save File", self)
        saveFile.setShortcut('Cmd+S')
        saveFile.triggered.connect(self.saveFileDialog)

        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Cmd+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        sliceWindowsButton = QAction('Slice Windows', self)
        sliceWindowsButton.setShortcut('Cmd+W')
        sliceWindowsButton.triggered.connect(self.sliceWindows)

        angelEncoderMenu = QMenu('Angel Encoder', self)
        angelEncoderEncode = QAction('Forward Pass', self)
        angelEncoderEncode.setShortcut('Cmd+T')
        angelEncoderEncode.triggered.connect(self.useAngelEncoder)
        
        angelEncoderDecode = QAction('Backward Pass', self)
        angelEncoderDecode.setShortcut('Cmd+R')
        angelEncoderDecode.triggered.connect(self.useAngelDecoder)

        ARMenu = QMenu('Autoregression Models', self)
        ARVARMAX = QAction('VARMAX', self)
        ARVARMAX.setShortcut('Cmd+G')
        ARVARMAX.triggered.connect(self.useGPLVM)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('File')
        modelMenu = menubar.addMenu('Model')
        trainMenu = menubar.addMenu('Train')

        fileMenu.addAction(selectFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(exitAct)

        modelMenu.addMenu(angelEncoderMenu)
        angelEncoderMenu.addAction(angelEncoderEncode)
        angelEncoderMenu.addAction(angelEncoderDecode)
        modelMenu.addAction(sliceWindowsButton)
        modelMenu.addMenu(ARMenu)
        ARMenu.addAction(ARVARMAX)

        self.layout = Window(self)
        self.layout.move(400, 15)
        self.layout.resize(400, 300)

        self.table = Table(self)


    def openFileNamesDialog(self):
        """Opens file when button clicked
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Select File", "",
        "CSV Files\ (*.csv)",options=options)
        if files:
            print(files)
            tempData = []
            for _file in files:
                #pass #implement readFile function here to parse the CSV into a dataframe style thing
                tempData.append(np.genfromtxt(_file, skip_header=1, dtype=None, delimiter=',', usecols=(1,2)))
            # print(tempData)
            self.data = np.asanyarray(tempData)
            self.layout.data = self.data
        else:
            QMessageBox.about(self, "No file selected!", "You have not selected a file.")

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save File","",\
        "Text Files (*.csv)", options=options)
        if fileName:
            print(fileName)

    def sliceWindows(self, stepsize=10, width=70):
        self.slicedData = np.swapaxes(np.dstack(self.data[i:1+i-70 or None:10] for i in range(0,70)), 1, 2)

    def useAngelEncoder(self):
        pass

    def useAngelDecoder(self):
        pass

    def useGPLVM(self):
        pass

    def useNARX(self):
        pass

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):

        #TODO THIS ISN'T WORKING, FIND A FIX TOMORROW 

        # print(self.data)
        # random data
        #data = [random.random() for i in range(10)]
        # instead of ax.hold(False)
        self.figure.clear()
        # create an axis
        ax = self.figure.add_subplot(111)
        # discards the old graph
        # ax.hold(False) # deprecated, see above
        # plot data
        ax.plot(np.squeeze(self.data), '*-')
        # refresh canvas
        self.canvas.draw()
        self.canvas.update()
        self.canvas.flush_events()


class Table(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.title = "Data"
        # self.left = 10
        # self.top = 20
        # self.width = 300
        # self.height = 200
        self.initUI()

    def initUI(self):
        # self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)

        newtable = self.createTable()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tableWidget)
        # self.setLayout(self.layout)
        self.setGeometry(3, 15, 400, 300)

        
        self.show()
 
    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)
        # for i, j in self.df:
        #     self.tableWidget.setItem(item,)
        self.tableWidget.setItem(0,0, QTableWidgetItem("Cell (1,1)"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Cell (1,2)"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Cell (2,1)"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("Cell (2,2)"))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Cell (3,1)"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("Cell (3,2)"))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Cell (4,1)"))
        self.tableWidget.setItem(3,1, QTableWidgetItem("Cell (4,2)"))
        self.tableWidget.move(0,0)
 
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    # ex = Table()
    mainWin.show()
    sys.exit(app.exec_())
