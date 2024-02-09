import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMainWindow, QPushButton, QDesktopWidget, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QPixmap, QImage, QFont

from mss import mss
import numpy as np
from PIL import Image
import cv2

import moduleimagetotext as predictor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ana Ekran Özellikleri
        
        desktop = QDesktopWidget()
        self.desktopWidth = desktop.screenGeometry().width()
        self.desktopHeight = desktop.screenGeometry().height()
        self.screenWidth = int(self.desktopWidth*0.3)
        self.screenHeight = int(self.desktopHeight*0.8)

        self.setFixedSize(QSize(self.screenWidth, self.screenHeight))    
        self.setWindowTitle("Ekran Kaşifi") 
        # Ana değişkenler
    
        self.predicted_text = "..."
        self.monitorX = 0
        self.monitorY = 0
        self.monitorWidth = self.desktopWidth
        self.monitorHeight = self.desktopHeight
        
        # Widgetleri Ekle
        widget = QWidget()
        widget.setLayout(self.compenents())
        self.setCentralWidget(widget)

    def compenents(self):
        column1 = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = self.text_fields()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()
        row5 = QHBoxLayout()
        row5.setAlignment(Qt.AlignLeft)
        
        self.predicted_text_field = self.processed_text()
        row1.addWidget(self.monitor())
        row3.addWidget(self.predicted_text_field)
        row4.addWidget(self.button_process())
        row4.addWidget(self.button_copy_text())
        row5.addWidget(self.desktop_screen_label())
        
        column1.addLayout(row1)
        column1.addLayout(row2)
        column1.addLayout(row3)
        column1.addLayout(row4)
        column1.addLayout(row5)
        return column1

    # Çekilen resim monitoru

    def monitor(self):
        self.lbl = QLabel()
        pixmap = QPixmap()
        self.lbl.setPixmap(pixmap)
        self.lbl.setFixedSize(
            QSize(int(self.screenWidth*0.8), int(self.screenHeight*0.3)))

        return self.lbl

    # total ekran çözünürlüğü
    
    def desktop_screen_label(self):
        lbl = QLabel(f"Total Ekran Çözünürlüğü {self.desktopWidth} {self.desktopHeight}")
        lbl.setFixedSize(QSize(300,34))
        return lbl
    # tahmin edilen yazı kısmı

    def processed_text(self):
        predicted_text_field = QLineEdit(self.predicted_text)
        predicted_text_field.setClearButtonEnabled(True)
        predicted_text_field.setFont(QFont("Cambria", 16))
        predicted_text_field.setFixedSize(
            QSize(int(self.screenWidth), int(self.screenHeight*0.3)))

        return predicted_text_field

    # işlenecek ekranın boyutu
    def text_fields(self):
        labelx = QLabel("X")
        labelx.setFixedSize(QSize(34, 34))
        line_editx = QLineEdit()
        line_editx.setFixedSize(QSize(34, 34))
        line_editx.setText(f"{self.monitorX}")

        labely = QLabel("Y")
        labely.setFixedSize(QSize(34, 34))
        line_edity = QLineEdit()
        line_edity.setFixedSize(QSize(34, 34))
        line_edity.setText(f"{self.monitorY}")
        
        labelwidth = QLabel("Genişlik")
        labelwidth.setFixedSize(QSize(34, 34))
        line_editwidth = QLineEdit()
        line_editwidth.setFixedSize(QSize(34, 34))
        line_editwidth.setText(f"{self.monitorWidth}")
        
        labelheight = QLabel("YÜkseklik")
        labelheight.setFixedSize(QSize(60, 34))
        line_editheight = QLineEdit()
        line_editheight.setFixedSize(QSize(34, 34))
        line_editheight.setText(f"{self.monitorHeight}")
        
        def do_action():
            self.monitorY = int(line_editx.text())
            self.monitorX = int(line_edity.text())
            self.monitorWidth = int(line_editwidth.text())
            self.monitorHeight = int(line_editheight.text())

        button = QPushButton("Uygula")
        button.setFixedSize(QSize(100, 34))
        button.clicked.connect(do_action)
        lay = QHBoxLayout()

        lay.addWidget(labelx)
        lay.addWidget(line_editx)
        lay.addWidget(labely)
        lay.addWidget(line_edity)
        lay.addWidget(labelwidth)
        lay.addWidget(line_editwidth)
        lay.addWidget(labelheight)
        lay.addWidget(line_editheight)
        lay.addWidget(button)
        return lay

    # Resmi çek ve işle

    def button_process(self):
        button = QPushButton("Çek")
        button.clicked.connect(self.take_picture)
        button.setFixedHeight(int(self.screenHeight*0.2))
        return button

    def take_picture(self):
        # resmi çek
        mon = {
            "top": self.monitorX,
            "left": self.monitorY,
            "width": self.monitorWidth,
            "height": self.monitorHeight}
        sct = mss()
        im = sct.grab(mon)
        im = Image.frombytes("RGB", im.size, im.rgb)
        im = np.array(im)

        self.predicted_text = predictor.image_texts(im)
        self.predicted_text_field.setText(self.predicted_text)

        # resmi programda göster
        image_rgb = cv2.cvtColor(cv2.resize(
            im, (int(self.screenWidth*0.8), int(self.screenHeight*0.3))), cv2.COLOR_BGR2RGB)
        qimage = QImage(
            image_rgb, image_rgb.shape[1], image_rgb.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.lbl.setPixmap(pixmap)

        return im

    # yazıyı koypyala
    def button_copy_text(self):
        button = QPushButton("Yazıyı Kopyala")
        button.clicked.connect(self.copy_text)
        button.setFixedHeight(int(self.screenHeight*0.2))
        return button

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.predicted_text)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
