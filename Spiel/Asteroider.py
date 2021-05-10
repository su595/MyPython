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
MEME_TEXTURES = False       # ( ͡° ͜ʖ ͡°)
DEFAULT_DEPTH = 65          # Default Tiefe in der alle Objekte liegen
WINDOW_SIZE = 800, 600      # Größe des Fensters
SCREEN_X = 20               # 20/15 = 800/600
SCREEN_Y = 15
NUMBER_OF_ASTEROIDS = 5    # Wieviele Asteroids am Anfang im Spiel sind (vlt. bei größerem Window mehr Asteroids)
AST_INIT_VELOCITY = 0.5     # Geschwindigkeit der Asteroids
ASTEROIDER_SCALE = 4        # Größe der Asteroids
ASTEROIDER_SCALE_VARIANCE = 2 # Um wieviel die ASTEROIDER_SCALE zufällig verändert wird
AST_SCALE_SMALLER = 0.5     # Um wieviel bei einem Treffer die Asteroids kleiner werden
AST_MIN_SCALE = 4           # Ab wann der Asteroid verschwindet
SHIP_SCALE = 2              # Größe des Schiffes
TURN_RATE = 360             # ein Faktor wie schnell sich das Schiff drehen kann
ACCELERATION = 50           # ein Faktor wie schnell sich das Schiff beschleunigen kann
MAX_VEL = 6                 # die maximale Geschwindigkeit
MAX_VEL_SQ = MAX_VEL**2     # quadrat davon
DEG_TO_RAD = pi / 180       # Faktor um Degrees zu Radiant umzuwandeln
BULLET_LIFE = 2             # Nach wie viel Zeit die Bullets verschwinden
BULLET_REPEAT = 0.4         # Wie schnell man hintereinander schießen kann
BULLET_SPEED = 20           # Wie schnell die Bullets sind
BULLET_SIZE = 1             # Wie groß die Bullets sind


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
        
    def initializeGameObjects(self):

        # Hintergrund laden mit großer Scale, damit das Fenster komplett ausgefüllt ist
        if MEME_TEXTURES:
            self.loadObject("textures/school.jpg", depth=200, scale=140)
        else:
            self.loadObject("textures/stars.jpg", depth=200, scale=140)

        # Schiff spawnen und Geschwindigkeit setzen
        if MEME_TEXTURES:
            self.ship = self.loadObject("textures/tentacle.png", scale=SHIP_SCALE)
        else:
            self.ship = self.loadObject("textures/ship.png", scale=SHIP_SCALE)

        self.setVelocity(self.ship, LVector3.zero())

        # Asteroids spawnen
        self.asteroids = []
        for i in range(NUMBER_OF_ASTEROIDS):
            self.newAsteroid()
        
        # Liste für Bullets deklarieren und Zeit bis zum nächsten Bullet
        self.bulletList = []
        self.nextBullet = 0.0

        # Variablen und textNodes für Level und Score deklarieren
        self.levelNode = TextNode("Level ")
        textNodePath = aspect2d.attachNewNode(self.levelNode)
        textNodePath.setScale(0.06)
        textNodePath.setPos(LPoint3(-1.3, 0, 0.9))
        self.scoreNode = TextNode("Level ")
        textNodePath = aspect2d.attachNewNode(self.scoreNode)
        textNodePath.setScale(0.06)
        textNodePath.setPos(LPoint3(-1.3, 0, 0.8))

        self.level = 1
        self.score = 0


        self.registerInputs()

    def resetGame(self):
        # reset the ship
        self.ship.setR(0)
        self.ship.setX(0)
        self.ship.setZ(0)
        self.ship.show()

        # reset level and score
        self.level = 1
        self.score = 0

        # spawn new asteroids
        for i in range(NUMBER_OF_ASTEROIDS):
            self.newAsteroid()
                
    def showFPS(self, dt):
        self.fpsCounter += dt
        # Alle halbe Sekunde
        if self.fpsCounter >= 0.5:
            self.textFPS.setText("FPS: " + str(int(60/dt)))
            self.fpsCounter = 0

    def setKey(self, key, val):
        self.keys[key] = val

    def setVelocity(self, obj, vector):
        obj.setPythonTag("velocity", vector)
    
    def getVelocity(self, obj):
        return obj.getPythonTag("velocity")

    def randomPos(self):
        tempPoint = LPoint3()

        # range generiert ein Tuple an Zahlen zwischen den gegebenen Endpunkten mit choice wird davon einer zufällig ausgewählt
        # und dieser wird mit setX() dem Asteroid zugewiesen
        tempPoint.setX(choice(tuple(range(-SCREEN_X, -5)) + tuple(range(5, SCREEN_X))))
        tempPoint.setZ(choice(tuple(range(-SCREEN_Y, -5)) + tuple(range(5, SCREEN_Y))))

        return tempPoint

    def randomAngle(self):
        # random angle in radians
        return random() * 2 * pi

    def setExpires(self, obj, expireTime):
        obj.setPythonTag("expires", expireTime)
    
    def getExpires(self, obj):
        return obj.getPythonTag("expires")

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
        self.login = QPushButton("Login")
        self.layout.addWidget(self.login)
        self.answerLabel = QLabel("\n")
        self.layout.addWidget(self.answerLabel)

        def on_button_clicked():
            succ = self.login(self.usernameLE.text(), self.pwLE.text())

            self.answerLabel.setText(self.loginResponse)
            if(succ):
                pass
                


        self.login.clicked.connect(on_button_clicked)


        # Das oben erstellte Layout dem Fenster zuweisen und das Fenster öffnen
        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec()

        return list(())
    
    def login(self, username, pw):
        self.loginResponse = "nichts"

        # MySQL Verbindung initiieren
        verbindung = mysql.connector.connect(user='root', password='root', host='localhost', database='testdb')

        # Passworthash von dem Username aus der Datenbank abfragen
        mycursor = verbindung.cursor()
        sqlBefehl = "SELECT pw FROM testtabelle WHERE username = %s"
        mycursor.execute(sqlBefehl, (username, ))

        pwHashed = mycursor.fetchall()

        # Wenn das Ergebnis leer ist
        if not mycursor.rowcount:
            self.loginResponse = "Username nicht vergeben"
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
            self.loginResponse = "Erfolgreich"
            return True
        
        verbindung.close
        self.loginResponse = "Falsches Passwort"
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

        # Textur laden und dem Objekt zuweisen
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

    def newAsteroid(self, pos="unset", vector="unset", scale="unset", speed=AST_INIT_VELOCITY):

        # make a varied scale if unset
        if(scale == "unset"):
            scale = ASTEROIDER_SCALE + randint(-ASTEROIDER_SCALE_VARIANCE, ASTEROIDER_SCALE_VARIANCE)

        # load the object with the determined scale and texture
        if MEME_TEXTURES:
            asteroid = self.loadObject(texture="textures/ahegao.png", scale=scale)
        else:
            asteroid = self.loadObject(texture="textures/asteroid%s.png" % randint(1,3), scale=scale)

        # append the new Asteroid to the end of the list
        self.asteroids.append(asteroid)

        # if the position or velocity isn't set, make it random/standard
        if (pos == "unset"):
            pos = self.randomPos()
        
        if (vector == "unset"):
            direction = self.randomAngle()
            vector = LVector3(sin(direction), 0, cos(direction)) * speed

        # set the position, direction and vector of the asteroid
        asteroid.setX(pos.getX())
        asteroid.setZ(pos.getZ())
        self.setVelocity(asteroid, vector)

    def checkBulletAsteroidCollision(self):
        
        for bullet in self.bulletList:

            for i in range(len(self.asteroids)-1, -1, -1):
                asteroid = self.asteroids[i]

                # if the bullet and asteroid distance is less than the sum of their radii
                if ((bullet.getPos() - asteroid.getPos()).lengthSquared() < (((bullet.getScale().getX() + asteroid.getScale().getX()) * .6) ** 2)):
                    # make it that the bullet gets removed in the next gameloop and handle the hit
                    self.setExpires(bullet, 0)
                    self.asteroidHit(i)

    def checkShipCollision(self):
        # Now we do the same collision pass for the ship
        shipSize = self.ship.getScale().getX()
        shipPos = self.ship.getPos()

        for asteroid in self.asteroids:

            # Same sphere collision check for the ship vs. the asteroid
            if ((shipPos - asteroid.getPos()).lengthSquared() <
                    (((shipSize + asteroid.getScale().getX()) * .4) ** 2)):
                
                # If there is a hit, clear the screen and schedule a restart
                self.alive = False         # Ship is no longer alive
                # Remove every object in asteroids and bullets from the scene
                for i in self.asteroids + self.bulletList:
                    i.removeNode()
                
                self.asteroids = []
                self.bulletList = []          # Clear the bullet list
                self.ship.hide()           # Hide the ship
                # Reset the velocity
                self.setVelocity(self.ship, LVector3(0, 0, 0))
                self.resetGame()

                break

    def asteroidHit(self, index):

        # if the asteroid is too small remove the asteroid and exit the function
        if(self.asteroids[index].getScale() < AST_MIN_SCALE):
            self.asteroids[index].removeNode()
            del self.asteroids[index]

            self.score += 200
            # if there are no asteroids left
            if len(self.asteroids) == 0:
                self.score += 1000
                self.levelUp()

            return
        
        oldPos = LPoint3(self.asteroids[index].getX(), self.asteroids[index].getZ())
        oldVel = self.getVelocity(self.asteroids[index])
        oldScale = self.asteroids[index].getScale().getX()

        # delete the old asteroid after its properties have been stored
        self.asteroids[index].removeNode()
        del self.asteroids[index]

        self.score += 100

        # make one Asteroid with the same velocity and one with negative velocity
        for i in (-1, 1):
            self.newAsteroid(pos=oldPos, vector=oldVel * i, scale=oldScale * AST_SCALE_SMALLER)

    def fire(self, task):
        currentTime = task.time

        # Schauen ob genug Zeit vergangen ist, sonst direkt returnen
        if(currentTime < self.nextBullet):
            return
        
        # Schuss abfeuern
        direction = DEG_TO_RAD * self.ship.getR()
        pos = self.ship.getPos()
        if MEME_TEXTURES:
            bullet = self.loadObject("textures/youKnow.png", pos=pos, scale=BULLET_SIZE)
        else:
            bullet = self.loadObject("textures/bullet.png", pos=pos, scale=0.2)
        relativeVel = self.getVelocity(self.ship) + (LVector3(sin(direction), 0, cos(direction)) * BULLET_SPEED)
        self.setVelocity(bullet, relativeVel)
        self.setExpires(bullet, currentTime + BULLET_LIFE)

        self.bulletList.append(bullet)

        self.setKey("fire", 0)

    def updateBullets(self, task, dt):
        newBullets = []

        # Für jedes Bullet die Position updaten, schauen, ob es expired ist, und dann entweder removen oder in der neuen Liste behalten
        for i in self.bulletList:
            self.updatePos(i, dt)

            if self.getExpires(i) > task.time:
                newBullets.append(i)
            else:
                i.removeNode()
        
        self.bulletList = newBullets

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

    def updateShip(self, task, dt):

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


        if self.keys["fire"]:
            self.fire(task)

        self.updatePos(self.ship, dt)

    def levelUp(self):

        self.level += 1

        # spawn more asteroids with a higher velocity
        for i in range(NUMBER_OF_ASTEROIDS + self.level * 2):
            self.newAsteroid(speed=AST_INIT_VELOCITY + self.level * 0.2)

    def gameLoop(self, task):

        # get the time since the last loop (since globalClock was last updated)
        globalClock = ClockObject.getGlobalClock()
        deltaT = globalClock.getDt()
        self.showFPS(deltaT)


        # Update position of the asteroids
        for asteroid in self.asteroids:
            self.updatePos(asteroid, deltaT)
        
        # Update the ship
        self.updateShip(task, deltaT)

        # Update Bullets
        self.updateBullets(task, deltaT)

        # check if bullets hit the asteroids and if ship hit asteroids
        self.checkBulletAsteroidCollision()
        self.checkShipCollision()

        # update the textNodes
        self.scoreNode.setText("Score: " + str(self.score))
        self.levelNode.setText("Level: " + str(self.level))


        # Ein return Task.cont heißt, der taskMgr lässt den taskLoop continuen/weiterlaufen
        return Task.cont
  
    def __init__(self):

        # Showbase und das Fenster konfigurieren
        ShowBase.__init__(self)
        self.setProperties()

        # Alle Objekte im Spiel initialisieren
        self.initializeGameObjects()

        # GameLoop starten
        self.gameTask = self.taskMgr.add(self.gameLoop, "gameLoop")


game = Asteroider()
# Eine Methode von ShowBase
game.run()
