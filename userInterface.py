import os
import shutil
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class filedialogdemo(QWidget):
   def __init__(self, parent = None):
      super(filedialogdemo, self).__init__(parent)
		
      layout = QVBoxLayout()
      self.btn = QPushButton("Upload .STL file")
      self.file = None
      self.btn.clicked.connect(self.getfile)
      layout.addWidget(self.btn)

      self.btn1 = QPushButton("Generate .eMesh file")
      self.btn1.clicked.connect(self.convertfile)
      layout.addWidget(self.btn1)
		
      self.setLayout(layout)
      self.setWindowTitle(".STL to .eMesh File Converter")

   # Upload STL File	
   def getfile(self):
      fname, _ = QFileDialog.getOpenFileName(self, 'Open file', 
         'c:\\',"Image files (*.stl)")
      self.file = fname
      

   # Convert uploaded STL file to OpenFOAM compatible file
   def convertfile(self):
      shutil.copy(self.file, "./user/constant/triSurface")

      with open("./simulation/system/surfaceFeaturesDict", "r", encoding="utf-8") as fr:
         line = fr.readlines()
      
      line[15] = "surfaces (\"" + str(os.path.basename(self.file)) + "\");\n"

      with open("./user/system/surfaceFeaturesDict", "w", encoding="utf-8") as fw:
         fw.writelines(line)

      os.chdir("./user")
      os.system("surfaceFeatures")
   
   def closeEvent(self, event):
      os.chdir("../")
      shutil.rmtree("./user")
      
				
def main():
   shutil.copytree("./simulation", "./user")
   app = QApplication(sys.argv)
   ex = filedialogdemo()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()