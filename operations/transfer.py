from PyQt5.QtGui import *
from PyQt5.QtCore import *

class transfer():

    def __init__(self, tabs):
        self.src = tabs[1]
        self.dest = tabs[2]
        self.volume = float(tabs[3])
        if self.volume < 20:
            self.tip = "P20"
        elif self.volume < 200:
            self.tip = "P200"
        else:
            self.tip = "P1000"

        self.letterConv = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4,"F":5, "G": 6, "H": 7}

    def print(self):
        print(self.src, self.dest, self.volume, self.tip)

    def draw(self, qp, grid):
        # Draw out the instruction text
        qp.setPen(Qt.white)
        qp.setFont(QFont('Arial', 20))
        qp.drawText(550, 50, "Transfer " + str(self.volume) + "uL-" + self.tip + " tip")

        qp.setPen(Qt.magenta)
        qp.drawText(900, 50, self.src)

        qp.setPen(Qt.white)
        qp.drawText(1150, 50, " -> " )

        qp.setPen(Qt.cyan)
        qp.drawText(1200, 50,self.dest)

        # Determine correct source container, if pcr plate also determine correct well and highlight
        qp.setPen(Qt.magenta)
        if self.src in grid.smallContainerLabels:
            index = grid.smallContainerLabels.index(self.src)
            coordinates = grid.smallContainerXY[index]
            qp.drawText(coordinates[0], coordinates[1], self.src)
        else:
            src = self.src.split("/")
            srcPlate = src[0]
            srcWell = src[1]
            srcPlateIndex = grid.pcrPlateLabels.index(srcPlate)
            srcPlateCoordinates = grid.pcrPlateXY[srcPlateIndex]
            qp.drawRect(srcPlateCoordinates[0], srcPlateCoordinates[1], grid.pcrPlateWidth, grid.pcrPlateHeight)

            srcWellX = srcPlateCoordinates[0] + grid.pcrFirstWellLoc[0] + ((int(srcWell[1:]) - 1) * grid.wellDistance)
            srcWellY = srcPlateCoordinates[1] + grid.pcrFirstWellLoc[1] + (self.letterConv[srcWell[0]] * grid.wellDistance)
            qp.drawEllipse(QPoint(srcWellX, srcWellY), grid.wellRadius, grid.wellRadius)

        #Determine correct destination container, if pcr plate also determine correct well and highlight
        qp.setPen(Qt.cyan)
        if self.dest in grid.smallContainerLabels:
            index = grid.smallContainerLabels.index(self.dest)
            coordinates = grid.smallContainerXY[index]
            qp.drawText(coordinates[0], coordinates[1], self.dest)
        else:
            dest = self.dest.split("/")
            destPlate = dest[0]
            destWell = dest[1]
            destPlateIndex = grid.pcrPlateLabels.index(destPlate)
            destPlateCoordinates = grid.pcrPlateXY[destPlateIndex]
            qp.drawRect(destPlateCoordinates[0], destPlateCoordinates[1], grid.pcrPlateWidth, grid.pcrPlateHeight)

            destWellX = destPlateCoordinates[0] + grid.pcrFirstWellLoc[0] + ((int(destWell[1:]) - 1) * grid.wellDistance)
            destWellY = destPlateCoordinates[1] + grid.pcrFirstWellLoc[1] + (
            self.letterConv[destWell[0]] * grid.wellDistance)
            qp.drawEllipse(QPoint(destWellX, destWellY), grid.wellRadius, grid.wellRadius)
