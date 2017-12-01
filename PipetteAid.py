import sys
from Window import Window
from PyQt5.QtWidgets import QApplication
from os import listdir

#Program to be executed
#Main run application that provides access of semiprotocol files
#In order to add more semiprotocols add them to './Semiprotocols' folder and restart program

files = listdir("./Semiprotocols")

app = QApplication([])
window = Window(files)
sys.exit(app.exec_())