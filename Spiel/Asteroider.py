from random import choice, randint, random
from direct.showbase.ShowBase import ShowBase
# LPoint3 und LVector3 sind Objekte für Punkte und Vektoren
from panda3d.core import WindowProperties, TransparencyAttrib, LPoint3, LVector3, ClockObject, TextNode
from direct.task.Task import Task
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, qDrawBorderPixmap
import mysql.connector
import bcrypt
import sys
from math import cos, pi, sin

# So ähnlich wie #define in C++
DEFAULT_DEPTH = 65
WINDOW_SIZE = 800, 600 #Größe des Fensters
SCREEN_X = 20 # 20/15 = 800/600
SCREEN_Y = 15
NUMBER_OF_ASTEROIDS = 10 # Wieviele Asteroids im Spiel sind (vlt. bei größerem Window mehr Asteroids)
ASTEROID_INIT_VELOCITY = 2 # Geschwindigkeit der Asteroids
ASTEROIDER_SCALE = 3 # Größe der Asteroids
ASTEROIDER_SCALE_VARIANCE = 1 # Um wieviel die ASTEROIDER_SCALE zufällig verändert wird
SHIP_SCALE = 2 # Größe des Schiffes
TURN_RATE = 360 # ein Faktor wie schnell sich das Schiff drehen kann
ACCELERATION = 10 # ein Faktor wie schnell sich das Schiff beschleunigen kann
MAX_VEL = 10 # die maximale Geschwindigkeit
MAX_VEL_SQ = MAX_VEL**2 # quadrat davon
DEG_TO_RAD = pi / 180 # Faktor um Degrees zu Radiant umzuwandeln

class Asteroider(ShowBase):
    

    def setProperties(self):

        # set properties of the window
        properties = WindowProperties()
        properties.setSize(WINDOW_SIZE)
        properties.setTitle("Titel des Fensters")
        self.win.requestProperties(properties)

        self.disableMouse()
        self.setBackgroundColor((0, 0, 0, 1))

        # counter for fps used in gameloop and text node to display fps
        self.fpsCounter = 0
        self.textFPS = TextNode("FPS")
        textNodePath = aspect2d.attachNewNode(self.textFPS)
        textNodePath.setScale(0.06)
        textNodePath.setPos(LPoint3(0.9, 0, 0.9))
        
    def showFPS(self, time):
        self.fpsCounter += time
        # Alle halbe Sekunde
        if self.fpsCounter >= 0.5:
            self.textFPS.setText("FPS: " + str(int(60/time)))
            self.fpsCounter = 0

    def setKey(self, key, val):
        self.keys[key] = val

    def setVelocity(self, obj, vector):
        obj.setPythonTag("velocity", vector)
    
    def getVelocity(self, obj):
        return obj.getPythonTag("velocity")

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

        # MySQL Verbindung initiieren
        verbindung = mysql.connector.connect(user='root', password='root', host='localhost', database='testdb')

        # Passworthash von dem Username aus der Datenbank abfragen
        mycursor = verbindung.cursor()
        sqlBefehl = "SELECT pw FROM testtabelle WHERE username = %s"
        mycursor.execute(sqlBefehl, (username, ))

        pwHashed = mycursor.fetchall()

        # Wenn das Ergebnis leer ist
        if not mycursor.rowcount:
            print("Username nicht vergeben")
            return False

        # Das kann man sicher auch ohne for machen, aber ich lasse es so weils funktioniert
        for x in pwHashed:
            # es gibt nur ein Ergebnis in einer Zeile, weil das beim SQL Befehl so festgelegt wurde
            pwHashed = x[0]

        # Alles utf-8 encoden weil Bcrypt sehr wählerisch ist
        pw = pw.encode("utf-8")
        pwHashed = pwHashed.encode("utf-8")

        # Übergebenes Passwort und Hash aus der Datenbank vergleichen und entsprechend true oder false liefern
        # Vorher noch die Verbindung schließen
        if bcrypt.checkpw(pw, pwHashed):
            verbindung.close()
            return True
        else:
            verbindung.close
            print("Falsches Passwort")
            return False
    
    def register(self, username, pw):

        # MySQL Verbindung initiieren
        verbindung = mysql.connector.connect(user='root', password='root', host='localhost', database='testdb')

        # Schauen ob der Benutzername schon vergeben ist (ob das Ergebnis der Abfrage größer als 0 ist) und wenn ja false returnen
        mycursor = verbindung.cursor()
        sqlBefehl = "SELECT * FROM testtabelle WHERE username = %s"
        mycursor.execute(sqlBefehl, (username, ))
        mycursor.fetchall()

        if mycursor.rowcount:
            print("Username schon vergeben")
            return False
        
        # Wenn der Benutzername nicht vergeben ist, dann den Passworthash generieren und zusammen mit dem Benutzernamen in die Datenbank einfügen
        pwHashed = bcrypt.hashpw(pw, bcrypt.gensalt())
        sqlBefehl = "INSERT INTO 'testtabelle' ('username', 'pw') VALUES ('%(username)s', '%(pwHashed)s');"
        if mycursor.execute(sqlBefehl, (username, pwHashed, )):
            print("Erfolgreich registriert!")
            return True
        else:
            print("Fehler")
            return False

    def loadObject(self, texture, pos=LPoint3(0,0), depth=DEFAULT_DEPTH, scale=1, transparency=True):
        # Jedes Objekt benutzt das plane-Model (weil 2D und so)
        obj = self.loader.loadModel("models/plane.egg")
        obj.reparentTo(self.camera)

        # Anfangsposition und Sklalierung setzen
        obj.setPos(pos.getX(), depth, pos.getZ())
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
            texture = self.loader.loadTexture(texture)
            obj.setTexture(texture, 1)

        # Das Objekt returnen um es z.B. in eine Liste einzufügen
        return obj

    def registerInputs(self):
        self.keys = {"turnLeft": 0, "turnRight": 0, "accel": 0, "fire": 0}

        self.accept("escape", sys.exit)

        self.accept("arrow_left",       self.setKey, ["turnLeft", 1])
        self.accept("arrow_left-up",    self.setKey, ["turnLeft", 0])
        self.accept("arrow_right",      self.setKey, ["turnRight", 1])
        self.accept("arrow_right-up",   self.setKey, ["turnRight", 0])
        self.accept("arrow_up",         self.setKey, ["accel", 1])
        self.accept("arrow_up-up",      self.setKey, ["accel", 0])
        self.accept("space",            self.setKey, ["fire", 1])

    def setAsteroidInitialPosAndSpeed(self, obj):
        
        # range generiert ein Tuple an Zahlen zwischen den gegebenen Endpunkten mit choice wird davon einer zufällig ausgewählt
        # und dieser wird mit setX() dem Asteroid zugewiesen
        obj.setX(choice(tuple(range(-SCREEN_X, -5)) + tuple(range(5, SCREEN_X))))
        obj.setZ(choice(tuple(range(-SCREEN_Y, -5)) + tuple(range(5, SCREEN_Y))))
        


        # random angle in radians
        orientation = random() * 2 * pi

        vector = LVector3(sin(orientation), 0, cos(orientation)) * ASTEROID_INIT_VELOCITY

        self.setVelocity(obj, vector)

    def spawnAsteroids(self, howmany):
        # spawn random asteroids (with 3 textures and different sizes)
        # only call this at init, otherwise the asteroids spawned before will not be funtion (bc theyre no longer in the list)

        self.asteroids = []

        for i in range(howmany):
            asteroiderScale = ASTEROIDER_SCALE + randint(-ASTEROIDER_SCALE_VARIANCE, ASTEROIDER_SCALE_VARIANCE)

            asteroid = self.loadObject(texture="textures/asteroid%d.png" % (randint(1, 3)), scale=asteroiderScale)

            self.asteroids.append(asteroid)

            for i in self.asteroids:
                self.setAsteroidInitialPosAndSpeed(i)
    
    def updatePos(self, obj, deltaT):

        velocity = self.getVelocity(obj)

        newPosition = obj.getPos() + (velocity * deltaT)
        
        # check if position is outside of screen
        radius = 1 * obj.getScale().getX()
        if newPosition.getX() - radius > SCREEN_X:
            newPosition.setX(-SCREEN_X)
        elif newPosition.getX() + radius < -SCREEN_X:
            newPosition.setX(SCREEN_X)

        if newPosition.getZ() - radius > SCREEN_Y:
            newPosition.setZ(-SCREEN_Y)
        elif newPosition.getZ() + radius < -SCREEN_Y:
            newPosition.setZ(SCREEN_Y)
        
        obj.setPos(newPosition)

    def updateShip(self, dt):

        # Die Rotation unseres Schiffes
        direction = self.ship.getR()

        if self.keys["turnRight"]:
            direction += TURN_RATE * dt
            self.ship.setR(direction % 360)
        # kein elif!
        if self.keys["turnLeft"]:
            direction -= TURN_RATE * dt
            self.ship.setR(direction % 360)
        
        if self.keys["accel"]:
            direction_rad = DEG_TO_RAD * direction
            newVel = LVector3(sin(direction_rad), 0, cos(direction_rad)) * ACCELERATION * dt

            newVel += self.getVelocity(self.ship)
            if newVel.lengthSquared() > MAX_VEL_SQ:
                newVel.normalize()
                newVel *= MAX_VEL
            
            self.setVelocity(self.ship, newVel)

        self.updatePos(self.ship, dt)

    def gameLoop(self, task):

        # get the time since the last loop (since globalClock was last updated)
        globalClock = ClockObject.getGlobalClock()
        deltaT = globalClock.getDt()
        self.showFPS(deltaT)


        # Update position of the asteroids
        for i in self.asteroids:
            self.updatePos(i, deltaT)
        
        # Update the ship
        self.updateShip(deltaT)

        # Ein return Task.cont heißt, der taskMgr lässt den taskLoop continuen/weiterlaufen
        return Task.cont
  
    def __init__(self):

        # Showbase und das Fenster einstellen
        ShowBase.__init__(self)
        self.setProperties()

        # Hintergrund laden mit großer Scale, damit das Fenster komplett ausgefüllt ist
        self.loadObject("textures/stars.jpg", depth=200, scale=140)

        # Schiff spawnen und Geschwindigkeit setzen
        self.ship = self.loadObject("textures/ship.png", scale=SHIP_SCALE)
        self.setVelocity(self.ship, LVector3.zero())

        # Asteroids spawnen
        self.spawnAsteroids(NUMBER_OF_ASTEROIDS)

        # Die Eingaben "accepten"
        self.registerInputs()


        # GameLoop starten
        self.gameTask = self.taskMgr.add(self.gameLoop, "gameLoop")
        

game = Asteroider()
# Eine Methode von ShowBase
game.run()
