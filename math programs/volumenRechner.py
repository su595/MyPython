import math
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QCheckBox


class Quader():

    def __init__(self, länge, breite, höhe):
        self.A = int(länge)
        self.B = int(breite)
        self.C = int(höhe)

    def __str__(self):
        outputStr = "----------------------- \n"
        outputStr += "Seite A: " + str(self.A) + "\n"
        outputStr += "Seite B: " + str(self.B) + "\n"
        outputStr += "Seite C: " + str(self.C) + "\n"
        outputStr += "Volumen: " + str(self.getVolume())

        return outputStr

    def getVolume(self):
        volume = self.A * self.B * self.C

        return volume


class Zylinder():

    def __init__(self, breite, höhe):
        self.r = int(breite)
        self.h = int(höhe)
    
    def __str__(self):
        outputStr = "----------------------- \n"
        outputStr += "Radius: " + str(self.r) + "\n"
        outputStr += "Höhe: " + str(self.h) + "\n"
        outputStr += "Volumen: " + str(self.getVolume())

        return outputStr

    def getVolume(self):
        # V = r^2 * pi * h
        volume = (self.r * self.r * math.pi) * self.h

        return volume


class Pyramide():
    def __init__(self, breite, höhe):
        self.A = int(breite)
        self.h = int(höhe)
    
    def __str__(self):
        outputStr = "----------------------- \n"
        outputStr += "Seitenlänge: " + str(self.A) + "\n"
        outputStr += "Höhe: " + str(self.h) + "\n"
        outputStr += "Volumen: " + str(self.getVolume())

        return outputStr
    
    def getVolume(self):
        volume = 1/3 * self.A * self.A * self.h

        return volume


class UserInterface():
    
    
    def qtBox(self):

        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()

        # jeweils ein Label und ein Eingabefeld (LineEdit) für Email und Password
        self.layout.addWidget(QLabel("Länge: "))
        self.längeLE = QLineEdit()
        self.layout.addWidget(self.längeLE)

        self.layout.addWidget(QLabel("Breite/Radius: "))
        self.breiteLE = QLineEdit()
        self.layout.addWidget(self.breiteLE)

        self.layout.addWidget(QLabel("Höhe: "))
        self.höheLE = QLineEdit()
        self.layout.addWidget(self.höheLE)

        # Drei Checkboxen für die Auswahl zwischen Quader, Zylinder und Pyramide
        self.quaderC = QCheckBox("Quader")
        self.layout.addWidget(self.quaderC)
        self.zylinderC = QCheckBox("Zylinder")
        self.layout.addWidget(self.zylinderC)
        self.pyramideC = QCheckBox("Pyramide")
        self.layout.addWidget(self.pyramideC)

        self.button = QPushButton("Los!")
        self.layout.addWidget(self.button)

        #Drei Label für die Ergebnisse, die in berrechnen() mit setText() gefüllt werden
        self.txt1 = QLabel()
        self.layout.addWidget(self.txt1)
        self.txt2 = QLabel()
        self.layout.addWidget(self.txt2)
        self.txt3 = QLabel()
        self.layout.addWidget(self.txt3)

        self.buttonQuit = QPushButton("Schließen")
        self.layout.addWidget(self.buttonQuit)

        def button_quit():
            self.app.quit()

        def on_button_clicked():
            #Vorherige Werte löschen und mit berrechnen() neue Werte einsetzen
            self.txt1.setText("")
            self.txt2.setText("")
            self.txt3.setText("")
            self.berrechnen()

        self.button.clicked.connect(on_button_clicked)
        self.buttonQuit.clicked.connect(button_quit)

        # Das oben erstellte Layout dem Fenster zuweisen und das Fenster öffnen
        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec()
        
    def berrechnen(self):
        if self.quaderC.isChecked():
            myQuader = Quader(self.längeLE.text(), self.breiteLE.text(), self.höheLE.text())
            self.txt1.setText(str(myQuader.getVolume()))

        if self.zylinderC.isChecked():
            myZylinder = Zylinder(self.breiteLE.text(), self.höheLE.text())
            self.txt2.setText(str(myZylinder.getVolume()))

        if self.pyramideC.isChecked():
            myPyramide = Pyramide(self.breiteLE.text(), self.höheLE.text())
            self.txt3.setText(str(myPyramide.getVolume()))

    def __init__(self):
        pass
        

start = UserInterface()
start.qtBox()
