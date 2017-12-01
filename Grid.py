from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Grid():



    #Main class storing any information for the current state of the image.
    #Saves how many pcr plate containers are in place (up to 6)
    #Saves how many 'other' containers are in place(up to 7)
    #Saves values for sizes of each container and locations of where they belong on a screen
    #Made to properly accomodate a 1920x1080 screen
    def __init__(self):
        self.pcrPlateWidth = 490
        self.pcrPlateHeight = 327
        self.pcrPlateXY = [[50, 208], [590, 208], [1130, 208], [50, 643], [590, 643], [1130, 643]]
        self.pcrFirstWellLoc = [55, 43]
        self.wellDistance = 34
        self.wellRadius = 17

        self.smallContainerXY = [[1690,125],[1690,260],[1690,395],[1690,530],[1690,665],[1690,800],[1690,935]]

        self.usedSmallContainers = [False, False, False, False, False, False, False]
        self.smallContainerLabels = ["", "", "", "", "", "", ""]
        self.usedPlates = [False, False, False, False, False, False]
        self.pcrPlateLabels = ["", "", "", "", "", ""]

    #Adds container to grid
    def addContainer(self, task):
        if task.container == "pcr_plate_96":
            index = 0
            for used in self.usedPlates:
                if not used:
                    break
                else:
                    index += 1
            self.pcrPlateLabels[index] = task.name
            self.usedPlates[index] = True
            return self.pcrPlateXY[index]
        else:
            index = 0
            for used in self.usedSmallContainers:
                if not used:
                    break
                else:
                    index += 1
            self.smallContainerLabels[index] = task.name
            self.usedSmallContainers[index] = True
            return self.smallContainerXY[index]

    #Removes container from grid
    def removeContainer(self, task):
        if task.containerName in self.pcrPlateLabels:
            index = self.pcrPlateLabels.index(task.containerName)
            self.usedPlates[index] = False
            self.pcrPlateLabels[index] = ""
            return self.pcrPlateXY[index], False
        else:
            index = self.smallContainerLabels.index(task.containerName)
            self.usedSmallContainers[index] = False
            self.smallContainerLabels[index] = ""
            return self.smallContainerXY[index], True


    #Used for the rewind capability, allows a new copy of grid state to be saved in order to return to it
    def makeCopy(self):
        copy = Grid()
        copy.usedPlates = self.usedPlates[:]
        copy.pcrPlateLabels = self.pcrPlateLabels[:]
        copy.usedSmallContainers = self.usedSmallContainers[:]
        copy.smallContainerLabels = self.smallContainerLabels[:]
        return copy


    #Draws current containers found on the deck along with separating boundaries.
    def draw(self, qp):
        qp.setPen(Qt.white)
        qp.setFont(QFont('Arial', 20))
        qp.drawLine(0, 100, 1920, 100)
        qp.drawLine(1670, 100, 1670, 1080)

        for i in range(len(self.usedPlates)):
            if self.usedPlates[i]:
                qp.drawRect(self.pcrPlateXY[i][0], self.pcrPlateXY[i][1], self.pcrPlateWidth, self.pcrPlateHeight)
                qp.drawText(self.pcrPlateXY[i][0], self.pcrPlateXY[i][1] - 10, self.pcrPlateLabels[i])

        for i in range(len(self.usedSmallContainers)):
            if self.usedSmallContainers[i]:
                qp.drawText(self.smallContainerXY[i][0], self.smallContainerXY[i][1], self.smallContainerLabels[i])
