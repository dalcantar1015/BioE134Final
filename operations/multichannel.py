from PyQt5.QtGui import *
from PyQt5.QtCore import *

#Method only works between pcr plate transfers
class multichannel():

    def __init__(self, tabs):
        self.srcStart = tabs[1]
        self.srcEnd = tabs[2]
        self.destStart = tabs[3]
        self.destEnd = tabs[4]
        self.volume = float(tabs[5])
        if self.volume < 20:
            self.tip = "P20"
        elif self.volume < 200:
            self.tip = "P200"
        else:
            self.tip = "P1000"
        self.letterConv = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}

    def print(self):
        print(self.srcStart, self.srcEnd, self.destStart, self.destEnd, self.volume, self.tip)

    def draw(self, qp, grid):
        # Draw out the instruction text
        qp.setPen(Qt.white)
        qp.setFont(QFont('Arial', 20))
        qp.drawText(550, 50, "Multichannel transfer " + str(self.volume) + "uL-" + self.tip + " tips")

        qp.setPen(Qt.magenta)
        qp.drawText(1150, 50, self.srcStart + "-" + self.srcEnd.split("/")[1])

        qp.setPen(Qt.white)
        qp.drawText(1450, 50, " -> ")

        qp.setPen(Qt.cyan)
        qp.drawText(1500, 50, self.destStart + "-" + self.destEnd.split("/")[1])

        qp.setPen(Qt.magenta)
        srcStart = self.srcStart.split("/")
        srcEnd = self.srcEnd.split("/")

        # Determine and highlight source plate
        srcPlate = srcStart[0]
        srcPlateIndex = grid.pcrPlateLabels.index(srcPlate)
        srcPlateCoordinates = grid.pcrPlateXY[srcPlateIndex]
        qp.drawRect(srcPlateCoordinates[0], srcPlateCoordinates[1], grid.pcrPlateWidth, grid.pcrPlateHeight)

        # Draw out the correct multichannel circles on source plate
        srcWellStart = srcStart[1]
        srcWellEnd = srcEnd[1]
        srcWellX = srcPlateCoordinates[0] + grid.pcrFirstWellLoc[0] + ((int(srcWellStart[1:]) - 1) * grid.wellDistance)
        srcWellY = srcPlateCoordinates[1] + grid.pcrFirstWellLoc[1] + (self.letterConv[srcWellStart[0]] * grid.wellDistance)


        for i in range(abs(int(srcWellStart[1:]) - int(srcWellEnd[1:])) + 1):
            for j in range(abs(self.letterConv[srcWellStart[0]] - self.letterConv[srcWellEnd[0]]) + 1):
                qp.drawEllipse(QPoint(srcWellX + i * grid.wellDistance, srcWellY + j * grid.wellDistance), grid.wellRadius, grid.wellRadius)


        #Determine and highlight destination plate
        qp.setPen(Qt.cyan)
        destStart = self.destStart.split("/")
        destEnd = self.destEnd.split("/")

        destPlate = destStart[0]
        destPlateIndex = grid.pcrPlateLabels.index(destPlate)
        destPlateCoordinates = grid.pcrPlateXY[destPlateIndex]
        qp.drawRect(destPlateCoordinates[0], destPlateCoordinates[1], grid.pcrPlateWidth, grid.pcrPlateHeight)

        #Draw out the correct multichannel circles on destination plate
        destWellStart = destStart[1]
        destWellEnd = destEnd[1]
        destWellX = destPlateCoordinates[0] + grid.pcrFirstWellLoc[0] + ((int(destWellStart[1:]) - 1) * grid.wellDistance)
        destWellY = destPlateCoordinates[1] + grid.pcrFirstWellLoc[1] + (self.letterConv[destWellStart[0]] * grid.wellDistance)

        for i in range(abs(int(destWellStart[1:]) - int(destWellEnd[1:])) + 1):
            for j in range(abs(self.letterConv[destWellStart[0]] - self.letterConv[destWellEnd[0]]) + 1):
                qp.drawEllipse(QPoint(destWellX + i * grid.wellDistance, destWellY + j * grid.wellDistance),grid.wellRadius, grid.wellRadius)