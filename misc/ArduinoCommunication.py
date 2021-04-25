import serial
import serial.tools.list_ports
import time
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5 import QtGui
from PIL import Image
import sys




LED_ARRAY_SIZE = 12,12 # width, height
BAUDRATE = 115200 # make sure this is the same in the arduino script

class LEDArrayCommunication():

    def __init__(self):
        
        self.establishSerialConnection()

        self.UI()

    def doEverything(self, filepath):

        self.resizeAndConvertImage(filepath)

        self.sendList(self.imageList)     

    def sendList(self, listToBeSent):
        
        # create a string with the start 's'
        stringToBeSent = "S"

        # iterate over the list
        for x in range(len(listToBeSent)):
            tempTuple = listToBeSent[x]

            # and iterate over each tuple in the list
            for x2 in range(3):
                # add every value in every tuple to the string seperated by a comma
                stringToBeSent += str(tempTuple[x2])
                stringToBeSent += ","

        # add the end 'E' to the string
        stringToBeSent += "E"

        print(stringToBeSent)
        
        for x in range(len(stringToBeSent)):

            self.arduino.write(bytes(stringToBeSent[x], "ASCII"))
            
            # A sleep time so the Serial buffer of the Arduino doesn't get overwhelmed
            # not neccessary at 9600 baud rate
            # time.sleep(0.001)

    def UI(self):
        
        # some required init
        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()

        # set window title and window icon (arduino icon)
        self.window.setWindowTitle("The hypermodern User Interface for my LED Array")
        self.window.setWindowIcon(QtGui.QIcon("./misc/pics/icon.png"))

        # add different widgets to the layout (labels, a lineEdit and buttons)
        self.layout.addWidget(QLabel("\nMay you be so kind as to enter a filepath to the .jpg image of your choice in the field below. "))
        
        self.QTfilepath = QLineEdit()
        self.layout.addWidget(self.QTfilepath)

        self.buttonGo = QPushButton("Let it be known that the user's desire is to have the rigorously selected image be displayed. \n Oh, ye spirits of the mystical serial communication, please, within your asynchronus powers, act upon this request with great urgency! ")
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
                self.feedback.setText("Thou request shall be fulfilled")
                self.doEverything(enteredFilepath)

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

    def resizeAndConvertImage(self, filepath):

        newImage = Image.open(filepath)
        newImage = newImage.resize((LED_ARRAY_SIZE))
        newImage.show()
        self.imageList = list(newImage.getdata())


    def establishSerialConnection(self):
        
        ports = serial.tools.list_ports.comports(include_links=False)

        for port in ports :
            print('Find port '+ port.device)

        # connect to the found serial port, flush the buffers  
        self.arduino = serial.Serial(port=port.device, baudrate=BAUDRATE, timeout=1)
        
        print('Connect ' + self.arduino.name)

        # wait for the arduino to initialize
        time.sleep(3)





test = LEDArrayCommunication()

# for debug:
# test.doEverything("./misc/pics/sky.jpg")

# available pictures
# ./misc/pics/red.jpg
# ./misc/pics/green.jpg
# ./misc/pics/blue.jpg
# ./misc/pics/sky.jpg
# ./misc/pics/asteroid3.jpg


# PROBLEMs:
# the com port is hardcoded



