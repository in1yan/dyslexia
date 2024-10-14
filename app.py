from PyQt5.QtWidgets import QMainWindow,  QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QGridLayout, QMenu
from games.sequence import Sequence
from games.recognition import charRecognition
from games.pairselection import pairSelection
from PyQt5 import uic
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui",self)
        #self.setWindowTitle("Dashboard - dyslexia")
        #self.setGeometry(100, 100, 400, 300)

        ##button
        self.seq_button = self.findChild(QPushButton, "sequence")
        self.seq_button.clicked.connect(self.open_sequence)
        self.rec_button = self.findChild(QPushButton, "recognition")
        self.rec_button.clicked.connect(self.open_recognition)
        self.pair_button = self.findChild(QPushButton, "pairselection")
        self.pair_button.clicked.connect(self.open_pairselection)
        #Menu bar 
        # self.closemenue = self.menubar.findChild(QMenu,"menuclose")
        # self.closemenue.triggered.connect(self.close_app)
        #self.button = QPushButton("Sequence Game", self)
        #self.button.setGeometry(150, 120, 100, 40)
        #self.button.clicked.connect(self.open_sequence)
    def open_sequence(self):
        self.seq = Sequence()
        self.seq.show()
    def open_recognition(self):
        self.rec = charRecognition()
        self.rec.show()
    def open_pairselection(self):
        self.pair = pairSelection()
        self.pair.show()
    def close_app(self):
        sys.exit()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

