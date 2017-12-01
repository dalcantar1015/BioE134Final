import unittest
from Grid import Grid
from operations.addContainer import addContainer
from operations.removeContainer import removeContainer
from operations.dispense import dispense





class MyTestCase(unittest.TestCase):

    #Max that it can go up to is 6
    def test_addMaxPCRPlates(self):
        testGrid = Grid()
        addContainerTask = addContainer(["addContainer","pcr_plate_96", "test", "testLOC", "TRUE"])
        for i in range(6):
            testGrid.addContainer(addContainerTask)
        pcrPlateAmount = 0
        for val in testGrid.usedPlates:
            if val:
                pcrPlateAmount += 1

        self.assertEqual(pcrPlateAmount, 6)

    #Check that remove function can generate correct amount of containers
    def test_removePCRPlates(self):
        testGrid = Grid()
        addContainerTask = addContainer(["addContainer", "pcr_plate_96", "test", "testLOC", "TRUE"])
        removeContainerTask = removeContainer(["removeContainer", "test"])
        for i in range(3):
            testGrid.addContainer(addContainerTask)
        pcrPlateAmount = 0
        for val in testGrid.usedPlates:
            if val:
                pcrPlateAmount += 1

        self.assertEqual(pcrPlateAmount, 3)

        testGrid.removeContainer(removeContainerTask)
        pcrPlateAmount = 0
        for val in testGrid.usedPlates:
            if val:
                pcrPlateAmount += 1

        self.assertEqual(pcrPlateAmount, 2)

    #Test to make sure code that calculates well locations is actually working
    def test_findCorrectDispenseLocation(self):
        testGrid = Grid()
        addContainerTask = addContainer(["addContainer", "pcr_plate_96", "test", "testLOC", "TRUE"])
        dispenseTask1 = dispense(["dispense", "water", "test/A3", "20"])
        dispenseTask2 = dispense(["dispense", "water", "test/H12", "20"])
        dispenseTask3 = dispense(["dispense", "water", "test/B9", "20"])

        testGrid.addContainer(addContainerTask)
        dest1 = dispenseTask1.dest.split("/")
        dest2 = dispenseTask2.dest.split("/")
        dest3 = dispenseTask3.dest.split("/")

        destPlate = dest1[0]
        dest1Well = dest1[1]

        dest2Well = dest2[1]

        dest3Well = dest3[1]

        destPlateIndex = testGrid.pcrPlateLabels.index(destPlate)
        destPlateCoordinates = testGrid.pcrPlateXY[destPlateIndex]

        dest1WellX = destPlateCoordinates[0] + testGrid.pcrFirstWellLoc[0] + ((int(dest1Well[1:]) - 1) * testGrid.wellDistance)
        dest1WellY = destPlateCoordinates[1] + testGrid.pcrFirstWellLoc[1] + (dispenseTask1.letterConv[dest1Well[0]] * testGrid.wellDistance)

        dest2WellX = destPlateCoordinates[0] + testGrid.pcrFirstWellLoc[0] + ((int(dest2Well[1:]) - 1) * testGrid.wellDistance)
        dest2WellY = destPlateCoordinates[1] + testGrid.pcrFirstWellLoc[1] + (dispenseTask2.letterConv[dest2Well[0]] * testGrid.wellDistance)

        dest3WellX = destPlateCoordinates[0] + testGrid.pcrFirstWellLoc[0] + ((int(dest3Well[1:]) - 1) * testGrid.wellDistance)
        dest3WellY = destPlateCoordinates[1] + testGrid.pcrFirstWellLoc[1] + (dispenseTask3.letterConv[dest3Well[0]] * testGrid.wellDistance)

        self.assertEqual(dest1WellX, 173)
        self.assertEqual(dest1WellY, 251)
        self.assertEqual(dest2WellX, 479)
        self.assertEqual(dest2WellY, 489)
        self.assertEqual(dest3WellX, 377)
        self.assertEqual(dest3WellY, 285)

if __name__ == '__main__':
    unittest.main()
