from PyQt5.QtGui import *
from PyQt5.QtCore import *

class addContainer():

    def __init__(self, tabs):
        self.container = tabs[1]
        self.name = tabs[2]
        self.location = tabs[3]
        if tabs[4] == "TRUE":
            self.isnew = True
        else:
            self.isnew = False

    def print(self):
        print(self.container, self.name, self.location, self.isnew)

    def draw(self, qp, grid):
        #Draw out the instruction text
        qp.setPen(Qt.green)
        qp.setFont(QFont('Arial', 20))
        qp.drawText(550, 50, "Add " + self.container + " [" + self.name + "] " +  " -> " + self.location)

        #Add container into grid object
        coordinates = grid.addContainer(self)

        #Draw green pcr plate or other container label
        if self.container == "pcr_plate_96":
            qp.drawRect(coordinates[0], coordinates[1], grid.pcrPlateWidth, grid.pcrPlateHeight)
            qp.drawText(coordinates[0], coordinates[1] - 10, self.name)
        else:
            qp.drawText(coordinates[0], coordinates[1], self.name)