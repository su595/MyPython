from random import randint
from direct.showbase.ShowBase import ShowBase
# LPoint3 und LVector3 sind "eigene Variablentypen" für Punkte und Vektoren
from panda3d.core import WindowProperties, TransparencyAttrib, LPoint3, LVector3
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
import mysql.connector
import bcrypt

# So ähnlich wie #define in C
ASTEROIDER_SCALE = 1 # Default 1
SPRITE_POS = 70 # 
WINDOW_SIZE = 800, 600 #Größe des Fensters




class Asteroider(ShowBase):
    

    def setProperties(self):
        # Alle möglichen Voreinstellungen machen...
        properties = WindowProperties()
        properties.setSize(WINDOW_SIZE)
        properties.setTitle("Titel des Fensters")
        self.win.requestProperties(properties)

        self.disableMouse()
        self.setBackgroundColor((0, 0, 0, 1))

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

        self.button.clicked.connect(on_button_clicked)


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

    def loadObject(self, texture=None, pos=LPoint3(0, 0), depth=SPRITE_POS, scale=1, transparency=True):
        # Jedes Objekt benutzt das plane-Model (weil 2D und so)
        obj = self.loader.loadModel("models/plane.egg")
        obj.reparentTo(self.camera)

        # Anfangsposition und Sklalierung setzen
        obj.setPos(pos.getX(), depth, pos.getY())
        obj.setScale(scale)

        # This tells Panda not to worry about the order that things are drawn in
        # (ie. disable Z-testing).  This prevents an effect known as Z-fighting.
        # Keine Ahnung was das genau macht, aber es schadet wohl nicht
        obj.setBin("unsorted", 0)
        obj.setDepthTest(False)
        
        if transparency: # Wenn transparency nicht ausdrücklich unterdrückt wird
            # Damit z.B. transparente PNG Dateien im Spiel auch wirklich transparent sind
            obj.setTransparency(TransparencyAttrib.MAlpha)

        if texture: # Wenn eine Textur übergeben wurde
            # Textur laden
            texture = self.loader.loadTexture("textures/" + texture)
            obj.setTexture(texture, 1)

        return obj

    def spawnAsteroids(self, howmany):
        self.asteroids = []

        for i in range(howmany):
            asteroiderScale = ASTEROIDER_SCALE + randint(-2, 2)

            asteroid = self.loadObject(texture="asteroid%d.png" % (randint(1, 3)), scale=asteroiderScale)
            self.asteroids.append(asteroid)
    
    def __init__(self):
        ShowBase.__init__(self)

        self.setProperties()

        # Hintergrund laden mit großer Scale, damit das Fenster komplett ausgefüllt ist
        self.loadObject(texture="stars.jpg", depth=200, scale=140)

        self.spawnAsteroids(5)
        

game = Asteroider()
game.run()