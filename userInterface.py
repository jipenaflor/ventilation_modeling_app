import os
import shutil
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ventilationModelingApp(QWidget):
   def __init__(self, parent = None):
      super(ventilationModelingApp, self).__init__(parent)
      win_layout = QHBoxLayout()

      #Control Panel Layout
      control_layout = QVBoxLayout()

      # STL to eMesh File Converter
      self.converter = QLabel()
      self.converter.setText("STL to eMesh File Converter")
      control_layout.addWidget(self.converter)

      self.btn1 = QPushButton("Upload .STL file")
      self.file = None
      self.btn1.clicked.connect(self.getFile)
      control_layout.addWidget(self.btn1)

      self.btn2 = QPushButton("Generate .eMesh file")
      self.btn2.clicked.connect(self.convertFile)
      control_layout.addWidget(self.btn2)

      # Boundary Block Generator
      self.boundaryBlock = QLabel()
      self.boundaryBlock.setText("Boundary Block Generator")
      control_layout.addWidget(self.boundaryBlock)

      bblck_layout = QFormLayout()

      self.bblck1 = QLineEdit()
      self.bblck2 = QLineEdit()
      self.bblck3 = QLineEdit()

      self.bblck1.setValidator(QDoubleValidator())
      self.bblck2.setValidator(QDoubleValidator())
      self.bblck3.setValidator(QDoubleValidator())

      bblck_layout.addRow("x", self.bblck1)
      bblck_layout.addRow("y", self.bblck2)
      bblck_layout.addRow("z", self.bblck3)

      control_layout.addLayout(bblck_layout)

      self.btn3 = QPushButton("Generate Boundary Block")
      self.btn3.clicked.connect(self.setBlock)
      control_layout.addWidget(self.btn3)

      win_layout.addLayout(control_layout)
      self.setLayout(win_layout)
      self.setWindowTitle("Ventilation Modeling Application")

   # Upload STL File	
   def getFile(self):
      fname, _ = QFileDialog.getOpenFileName(self, 'Open file', 
         'c:\\',"Image files (*.stl)")
      self.file = fname
      

   # Convert uploaded STL file to OpenFOAM compatible file
   def convertFile(self):
      shutil.copy(self.file, "./user/constant/triSurface")

      with open("./simulation/system/surfaceFeaturesDict", "r", encoding="utf-8") as fr:
         line = fr.readlines()
      
      line[15] = "surfaces (\"" + str(os.path.basename(self.file)) + "\");\n"

      with open("./user/system/surfaceFeaturesDict", "w", encoding="utf-8") as fw:
         fw.writelines(line)

      os.chdir("./user")
      os.system("surfaceFeatures")
   
   def setBlock(self):
      print("Under construction...")
   
   def closeEvent(self, event):
      os.chdir("../")
      os.system("rm -r ./user")
      
				
def main():
   shutil.copytree("./simulation", "./user")
   app = QApplication(sys.argv)
   ex = ventilationModelingApp()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()