import serial
import serial.tools.list_ports
import time
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5 import QtGui
from PIL import Image
import sys


class LEDArrayCommunication():


    def __init__(self):
        pass
        #self.UI()

    def buttonFunction(self, filepath):

        imageList = self.imageToList(filepath, (10,10))

        self.listToString(imageList, (10,10))     

    def listToString(self, list, size):
        # maybe sample half as often in the vertical direction

        imageString = ""

        for i1 in range(int(size[0]/2)):
            for i2 in range(size[1]):

                thisPixel = list[i1*size[0]*2 + i2]
                imageString += self.valueToChar(thisPixel)
            
            imageString += "\n"
        
        print(imageString)
        print(i1)
        print(i2)
            


    def valueToChar(self, value):
        # " .:-=+*#%@"
        if(value < 26):
            return "@"
        if(value < 52):
            return "%"
        if(value < 77):
            return "#"
        if(value < 103):
            return "*"
        if(value < 128):
            return "+"
        if(value < 154):
            return "="
        if(value < 179):
            return "-"
        if(value < 205):
            return ":"
        if(value < 230):
            return "."
        if(value < 256):
            return " "
        
        return "bigger than 255"

    def UI(self):
        
        # some required init
        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()

        # set window title and window icon (arduino icon)
        self.window.setWindowTitle("test")
        self.window.setWindowIcon(QtGui.QIcon("./misc/pics/icon.png"))

        # add different widgets to the layout (labels, a lineEdit and buttons)
        self.layout.addWidget(QLabel(".jpg filepath pls"))
        
        self.QTfilepath = QLineEdit()
        self.layout.addWidget(self.QTfilepath)

        self.buttonGo = QPushButton("Go")
        self.layout.addWidget(self.buttonGo)

        self.layout.addWidget(QLabel("\n "))
        self.feedback = QLabel("\n")
        self.layout.addWidget(self.feedback)
        self.layout.addWidget(QLabel("\n "))

        self.buttonQuit = QPushButton("Quit.")
        self.layout.addWidget(self.buttonQuit)

        def buttonGo():
            # get the filepath from the lineEdit
            enteredFilepath = str(self.QTfilepath.text())

            # put the last 4 chars of the filepath into a new string
            fileExtension = enteredFilepath[len(enteredFilepath) - 4]
            fileExtension += enteredFilepath[len(enteredFilepath) - 3]
            fileExtension += enteredFilepath[len(enteredFilepath) - 2]
            fileExtension += enteredFilepath[len(enteredFilepath) - 1]

            # check if the last 4 chars are the correct file extension and then display a message and call doEverything()
            if(fileExtension == ".jpg"):
                self.feedback.setText("Successful")
                self.buttonFunction(enteredFilepath)
                

            # if the file extension is wrong or missing display this message
            else:
                self.feedback.setText("Are you sure your filepath leads to a .jpg image??")

        def buttonQuit():
            # Terminate the whole program (so that the serial port is freed)
            # Any ongoing action (like a serial write) will of course fail
            sys.exit()
        
        # connect the two buttons to the function to be run when the button is pressed
        self.buttonGo.clicked.connect(buttonGo)
        self.buttonQuit.clicked.connect(buttonQuit)


        # set the defined layout and show the window
        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec()

    def imageToList(self, filepath, size):

        newImage = Image.open(filepath)
        newImage = newImage.resize(size)
        newImage = newImage.convert(mode="L")
        newImage.show()
        imageList = newImage.getdata()

        return imageList


test = LEDArrayCommunication()

list = test.imageToList("./misc/pics/sky.jpg", (100,100))
test.listToString(list, (100,100))

# for debug:
# i("./misc/pics/sky.jpg")

# available pictures
# ./misc/pics/red.jpg
# ./misc/pics/green.jpg
# ./misc/pics/blue.jpg
# ./misc/pics/sky.jpg
# ./misc/pics/asteroid3.jpg
