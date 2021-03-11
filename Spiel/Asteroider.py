from logging import error
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
import mysql.connector
import bcrypt



class Asteroider(ShowBase):
    

    def qtBox(self):

        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()

        # jeweils ein Label und ein Eingabefeld (LineEdit) für Email und Password
        self.layout.addWidget(QLabel("Email: "))
        self.usernameLE = QLineEdit()
        self.layout.addWidget(self.usernameLE)
        self.layout.addWidget(QLabel("Password: "))
        self.pwLE = QLineEdit()
        self.layout.addWidget(self.pwLE)
        # Box für Login oder Registrieren
        # und ein Login Knopf
        self.button = QPushButton("Los!")
        self.layout.addWidget(self.button)

        def on_button_clicked():
            # Wenn der Button gedrückt wird, wird das sichtbare Fenster geschlossen, der Code läuft normal weiter
            self.app.quit()

        self.button.clicked.connect(on_button_clicked())


        # Das oben erstellte Layout dem Fenster zuweisen und das Fenster öffnen
        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec()

        return list((self.usernameLE.text(), self.pwLE.text()))
    
    def login(self, username, pw):

        verbindung = mysql.connector.connect(user='root', password='root', host='localhost', database='testdb')

        mycursor = verbindung.cursor()
        sqlBefehl = "SELECT pw FROM testtabelle WHERE username = %s"
        mycursor.execute(sqlBefehl, (username, ))

        pwHashed = mycursor.fetchall()

        # Wenn das Ergebnis leer ist
        if not mycursor.rowcount:
            print("Username nicht vergeben")
            return False

        for x in pwHashed:
            # es gibt nur ein Ergebnis in einer Zeile, weil das beim SQL Befehl so festgelegt wurde
            pwHashed = x[0]

        pw = pw.encode("utf-8")
        pwHashed = pwHashed.encode("utf-8")

        if bcrypt.checkpw(pw, pwHashed):
            return True
        else:
            print("Falsches Passwort")
            return False
    
    def register(self, username, pw):
        verbindung = mysql.connector.connect(user='root', password='root', host='localhost', database='testdb')

        mycursor = verbindung.cursor()
        sqlBefehl = "SELECT * FROM testtabelle WHERE username = %s"
        mycursor.execute(sqlBefehl, (username, ))

        mycursor.fetchall()

        if mycursor.rowcount:
            print("Username schon vergeben")
            return False
        
        pwHashed = bcrypt.hashpw(pw, bcrypt.gensalt())
        sqlBefehl = "INSERT INTO 'testtabelle' ('username', 'pw') VALUES ('%(username)s', '%(pwHashed)s');"
        if mycursor.execute(sqlBefehl, (username, pwHashed, )):
            print("erfolgreich")
            return True
        else:
            print("fehler")
            return False

    def loadObject(self, dateipfadModel, dateipfadTextur, scale):
        self.scene = self.loader.loadModel(dateipfadModel) 
        # Reparent the model to render.
        self.scene.reparentTo(self.camera)
        # Apply scale and position transforms on the model.
        self.scene.setScale(scale)
        self.scene.setPos(0, 2, 0)
        # Textur laden
        self.texture = self.loader.loadTexture(dateipfadTextur)
        self.scene.setTexture(self.texture, 1)

    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(800, 600)
        properties.setTitle("Titel des Fensters")
        self.win.requestProperties(properties)

        self.disableMouse()
        self.setBackgroundColor((0, 0, 0, 1))

        self.loadObject("models/planeNeu.egg", "textures/stars.jpg", 1)

        loginDaten = self.qtBox()
        


            
        
        

game = Asteroider()
game.run()