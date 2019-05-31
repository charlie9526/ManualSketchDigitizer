import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
import cv2
from shape_recreator import shape_recreator
from sd1 import detct_shapes
from text_box import text_out
from pdf import cordiante_to_point
from pdf import generate_pdf



class filedialogdemo(QWidget):
    def __init__(self, parent=None):
        super(filedialogdemo, self).__init__(parent)
        self.path = ""
        layout = QVBoxLayout()
        self.btn = QPushButton("choose")
        self.btn.clicked.connect(self.getfile)
        layout.addWidget(self.btn)


        self.btn1 = QPushButton("create PDF")
        self.btn1.clicked.connect(self.get_pdf)
        layout.addWidget(self.btn1)

        self.le = QLabel("Hello, choose a photo first!")
        layout.addWidget(self.le)
        #self.le.resize(100, 100)
        self.le.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle("Sketch digitaizer")
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.setGeometry(self.left, self.top, self.width, self.height)

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpeg )")
        k = fname[0]
        self.name = k.split("/")[-1].split(".")[0]+".pdf"

        
        #self.setGeometry(self.left, self.top, self.width, self.height)
        pixmap = QPixmap(fname[0])
        self.le.setPixmap(pixmap)
        #self.resize(pixmap.width(),pixmap.height())
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.path = fname[0]
    
    def get_pdf(self):

        out_folder = QFileDialog.getExistingDirectory(self, "Choose directory")
        
        if (self.path != ""):
            path_out = out_folder + "/" + self.name
            self.path_out = path_out
            img = cv2.imread(self.path)
            height, width, channels = img.shape
            generate_pdf(height, width,text_out(self.path)[0],shape_recreator(detct_shapes(text_out(self.path)[1])),self.path_out)
            self.le.setText("Processd successfully!")
        else:
            self.le.setText("You should select a photo first!")


def main():
    app = QApplication(sys.argv)
    ex = filedialogdemo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
