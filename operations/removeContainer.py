from PyQt5.QtGui import *
from PyQt5.QtCore import *

class removeContainer():

    def __init__(self, tabs):
        self.containerName = tabs[1]

    def print(self):
        print(self.containerName)

    def draw(self, qp, grid):
        # Draw out the instruction text
        qp.setPen(Qt.red)
        qp.setFont(QFont('Arial', 20))
        qp.drawText(550, 50, "Remove " + self.containerName)

        #Find container in grid object and highlight it red and remove from grid object
        qp.setPen(Qt.red)
        coordinates, issmall = grid.removeContainer(self)
        if not issmall:
            qp.drawRect(coordinates[0], coordinates[1], grid.pcrPlateWidth, grid.pcrPlateHeight)
            qp.drawText(coordinates[0], coordinates[1] - 10, self.containerName)
        else:
            qp.drawText(coordinates[0], coordinates[1], self.containerName)


