from Grid import Grid
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from SemiProtocolReader import SemiProtocolReader

class Window(QWidget):

    def __init__(self, files):
        super().__init__()
        self.tasks = None
        self.files = files
        self.initUI()
        self.currentTaskIndex = 0
        self.start = False
        self.redraw = False
        self.grid = Grid()
        self.fileName = None
        self.SPR = SemiProtocolReader()
        self.previousGridStates = []
        self.end = False

    #Function that defines all buttons that will be needed throughout the duration of the program's runtime.
    #Buttons that aren't needed initially are hidden and shown when needed throughout the program
    def initUI(self):
        #Creates a selection box for different semiprotocol files found
        self.selection = QComboBox(self)
        self.selection.setFont(QFont('Arial', 20))
        self.selection.move(700, 300)
        self.selection.addItem("Please Select a Protocol")
        for file in self.files:
            self.selection.addItem(file)
        self.selection.activated[str].connect(self.selectProtocol)

        # Creates button and connects to quit function
        self.qbtn = QPushButton('Quit', self)
        self.qbtn.setFont(QFont('Arial', 20))
        self.qbtn.clicked.connect(QCoreApplication.instance().quit)
        self.qbtn.resize(self.qbtn.sizeHint())
        self.qbtn.move(200, 25)

        # Creates button that connects to start function
        self.startbtn = QPushButton('Start', self)
        self.startbtn.setFont(QFont('Arial', 20))
        self.startbtn.clicked.connect(self.start)
        self.startbtn.resize(self.startbtn.sizeHint())
        self.startbtn.move(600, 300)
        self.startbtn.hide()

        #Creates button that connects to next task function
        self.nextbtn = QPushButton('Next', self)
        self.nextbtn.setFont(QFont('Arial', 20))
        self.nextbtn.clicked.connect(self.next)
        self.nextbtn.resize(self.nextbtn.sizeHint())
        self.nextbtn.move(300, 25)
        self.nextbtn.hide()

        # Creates button that connects to previous task function
        self.prebtn = QPushButton('Previous', self)
        self.prebtn.setFont(QFont('Arial', 20))
        self.prebtn.clicked.connect(self.pre)
        self.prebtn.resize(self.prebtn.sizeHint())
        self.prebtn.move(400, 25)
        self.prebtn.hide()

        # Creates button that connects to restart function
        self.rebtn = QPushButton('Restart', self)
        self.rebtn.setFont(QFont('Arial', 20))
        self.rebtn.clicked.connect(self.restart)
        self.rebtn.resize(self.rebtn.sizeHint())
        self.rebtn.move(850, 400)
        self.rebtn.hide()

        #Sets window properties
        self.setWindowTitle('PipetteAid 2.0')
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.showFullScreen()

    #Function that takes in input from the selection box and allows use of the start button
    def selectProtocol(self, text):
        if text != "Please Select a Protocol":
            self.fileName = text
            self.startbtn.show()
        else:
            self.fileName = None
            self.startbtn.hide()

    #Function that sets up the window with the buttons that will be needed (NEXT and PREVIOUS)
    #Generates list of tasks from selection box input and adds initial grid state
    def start(self):
        self.tasks = self.SPR.run(self.fileName)
        self.previousGridStates.append(self.grid.makeCopy())
        self.nextbtn.show()
        self.prebtn.show()
        self.startbtn.hide()
        self.selection.hide()
        self.start = True
        self.redraw = True
        self.update()

    #Begins the next task function call and appends current grid state to previous states for rewinding ability
    def next(self):
        if not self.end:
            self.currentTaskIndex += 1
            self.previousGridStates.append(self.grid.makeCopy())
        if self.currentTaskIndex < len(self.tasks):
            self.redraw = True
        else:
            self.end = True
            self.rebtn.show()
            self.qbtn.move(750, 400)

        self.update()

    #Rewinds the program by setting the current grid state equal to the most recent previous grid state
    #Causes function to invoke the previous task command
    def pre(self):
        self.end = False
        self.rebtn.hide()
        self.qbtn.move(200, 25)

        if self.currentTaskIndex > 0:
            self.previousGridStates.pop()
            self.currentTaskIndex -= 1
            self.grid = self.previousGridStates[-1].makeCopy()
            self.redraw = True
            self.update()

    #Sets all window parameters to their initial state essentially restarting the program
    def restart(self):
        self.selection.setCurrentIndex(0)
        self.tasks = None
        self.files = self.files
        self.currentTaskIndex = 0
        self.start = False
        self.redraw = False
        self.grid = Grid()
        self.fileName = None
        self.SPR = SemiProtocolReader()
        self.previousGridStates = []
        self.selection.show()
        self.rebtn.hide()
        self.qbtn.move(200, 25)
        self.prebtn.hide()
        self.nextbtn.hide()
        self.end = False
        self.update()


    #Invokes each task and grid draw method in order to be a very general case without need for many if statements
    #If the end of semiprotocol is reached then it sets the window up to give off the restart capability
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.white)
        qp.setFont(QFont('Arial', 20))
        qp.drawText(10, 50, "Pipette Aid 2.0")

        if self.start and self.redraw:
            qp.drawText(10, 150, "Deck")
            self.grid.draw(qp)
            self.tasks[self.currentTaskIndex].draw(qp, self.grid)
            self.redraw = False

        if self.end:
            qp.drawText(600, 300, "You have reached the end of the semiprotocol")
            qp.drawText(300, 350, "You can either QUIT, RESTART, or use the PREVIOUS button to go back through the current semiprotocol")

        qp.end()
