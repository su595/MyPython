from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, qDrawBorderPixmap
import mysql.connector
import bcrypt
from configparser import ConfigParser
import os.path

# The two classes have the same UML-Diagram in order to be interchangeable without having to change other code

# Here results are written to a database (which doesnt seem to work for me although the code should be correct)
class PlayerDB():

    def qtBox(self): # public

        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()

        # jeweils ein Label und ein Eingabefeld (LineEdit) für Email und Password
        self.layout.addWidget(QLabel("Username: "))
        self.usernameLE = QLineEdit()
        self.layout.addWidget(self.usernameLE)
        self.layout.addWidget(QLabel("Password: "))
        self.pwLE = QLineEdit()
        self.layout.addWidget(self.pwLE)
        # Button für Login oder Registrieren
        self.loginButton = QPushButton("Login")
        self.layout.addWidget(self.loginButton)
        self.regButton = QPushButton("Registrieren")
        self.layout.addWidget(self.regButton)
        self.answerLabel = QLabel("\n")
        self.layout.addWidget(self.answerLabel)
        self.skipButton = QPushButton("Ohne Login starten")
        self.layout.addWidget(self.skipButton)

        def on_button_clicked_login():
            success = self.login(self.usernameLE.text(), self.pwLE.text())

            self.answerLabel.setText(self.loginResponse)
            
            # if the login is successful, exit qt app to the game
            if success:
                self.app.exit()
                
        def on_button_clicked_reg():
            success = self.register(self.usernameLE.text(), self.pwLE.text())

            self.answerLabel.setText(self.loginResponse)

            if success:
                self.app.exit()
        
        def on_button_clicked_skip():
            self.username = "not logged in"
            self.app.exit()

        self.loginButton.clicked.connect(on_button_clicked_login)
        self.regButton.clicked.connect(on_button_clicked_reg)
        self.skipButton.clicked.connect(on_button_clicked_skip)



        # Das oben erstellte Layout dem Fenster zuweisen und das Fenster öffnen
        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec()

    def login(self, username, pw): # private

        # MySQL Verbindung initiieren
        verbindung = mysql.connector.connect(user=self.MY_SQL["user"], password=self.MY_SQL["password"], host=self.MY_SQL["host"], database=self.MY_SQL["db"])

        # Passworthash von dem Username aus der Datenbank abfragen
        mycursor = verbindung.cursor()
        sqlBefehl = "SELECT pw FROM astlogin WHERE username = %s"
        mycursor.execute(sqlBefehl, (username, ))

        pwHashed = mycursor.fetchall()

        # Wenn das Ergebnis leer ist
        if not mycursor.rowcount:
            self.loginResponse = "Username nicht vergeben"

            verbindung.close()
            return False

        # Das kann man sicher auch ohne for machen, aber ich lasse es so weils funktioniert
        for x in pwHashed:
            # es gibt nur ein Ergebnis in einer Zeile, weil das beim SQL Befehl so festgelegt wurde
            pwHashed = x[0]

        # Alles utf-8 encoden weil Bcrypt sehr wählerisch ist
        pw = pw.encode("utf-8")
        pwHashed = pwHashed.encode("utf-8")

        # Übergebenes Passwort und Hash aus der Datenbank vergleichen und true oder false zurückgeben
        if bcrypt.checkpw(pw, pwHashed):

            # Hier noch eine loginResponse für die Qt Box und self.username festlegen
            self.loginResponse = "Erfolgreich"
            self.username = username

            verbindung.close()
            return True
        
        self.loginResponse = "Falsches Passwort"

        verbindung.close()
        return False
    
    def register(self, username, pw): # private

        # MySQL Verbindung initiieren
        verbindung = mysql.connector.connect(user=self.MY_SQL["user"], password=self.MY_SQL["password"], host=self.MY_SQL["host"], database=self.MY_SQL["db"])


        # Schauen ob der Benutzername schon vergeben ist (ob das Ergebnis der Abfrage größer als 0 ist) und wenn ja false returnen
        mycursor = verbindung.cursor()
        sqlBefehl = "SELECT * FROM astlogin WHERE username = %s"
        mycursor.execute(sqlBefehl, (username, ))
        mycursor.fetchall()

        if mycursor.rowcount:
            self.loginResponse = "Username schon vergeben"
            
            verbindung.close()
            return False
        
        pw = pw.encode("utf-8")

        # Wenn der Benutzername nicht vergeben ist, dann den Passworthash generieren und zusammen mit dem Benutzernamen in die Datenbank einfügen
        pwHashed = bcrypt.hashpw(pw, bcrypt.gensalt())

        sqlBefehl = "INSERT INTO astlogin (username, pw, level, points) VALUES ('"+ username +"', '"+ str(pwHashed, "utf-8") +"', '0', '0')"
        print(sqlBefehl)
        
        # Falls beim sql Befehl irgendein Fehler passiert false zurückgeben
        try:
            mycursor.execute(sqlBefehl)
            
            self.loginResponse = "Erfolgreich registriert!"
            self.username = username

            verbindung.close()
            return True
        except Exception as e:
            self.loginResponse = str(e)

            verbindung.close()
            return False

    def savePlayerdataToDatabase(self) -> None: # private
        try:
            verbindung = mysql.connector.connect(user=self.MY_SQL["user"], password=self.MY_SQL["password"], host=self.MY_SQL["host"], database=self.MY_SQL["db"])
            mycursor = verbindung.cursor()

            sqlBefehl = "INSERT INTO astlogin (level, points) VALUES ('%s', '%s') WHERE username = %s"
            mycursor.execute(sqlBefehl, (self.level, self.score, self.username ))
            
            
            verbindung.close()
        except Exeption as e:
            print(e)
      
    def updatePlayerdataFromDatabase(self) -> None: # public
        try:
            verbindung = mysql.connector.connect(user=self.MY_SQL["user"], password=self.MY_SQL["password"], host=self.MY_SQL["host"], database=self.MY_SQL["db"])
            mycursor = verbindung.cursor()

            sqlBefehl = "SELECT level, points FROM astlogin WHERE username = %s"
            mycursor.execute(sqlBefehl, (self.username, ))
            result = mycursor.fetchall()
            print(result)
            self.level = int(result[0][0])
            self.score = int(result[0][1])
            
            verbindung.close()
        except Exception as e:
            print(e)

    def savePlayerHighscoreToDatabase(self) -> None: # public
        # only update the playerdata if it was higher than when last saved
        oldScore = self.score
        oldLevel = self.level
        self.updatePlayerdataFromDatabase()

        if(self.score > oldScore or self.level > oldLevel):
            self.savePlayerdataToDatabase()
            self.highscore = self.score
            self.highlevel = self.level

    def __str__(self) -> str:
        out = "Spieler: " + str(self.username) + "\n"
        out += "Highscore: " + str(self.highscore) + " Punkte bei Level "  + str(self.highlevel) + "\n"
        out += "Level: " + str(self.level) + "\n"
        out += "Punkte: " + str(self.score) + "\n"

        return out

    def __init__(self, MY_SQL) -> None:
        # mySql Config übernehmen
        self.MY_SQL = MY_SQL

        self.qtBox()
        self.updatePlayerdataFromDatabase()
        self.score = 0
        self.level = 0

        # Variablen mit highscore, die nur bei init und neuem highscore überschrieben werden
        self.highscore = self.score
        self.highlevel = self.level


# Here results are written to a local .ini file
# eigentlich savePlayerdataToFile und updatePlayerDataFromFile usw.
class PlayerFile():
    
    def qtBox(self) -> None: # public

        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()

        # nur ein label für den namen
        self.layout.addWidget(QLabel("Username: "))
        self.usernameLE = QLineEdit()
        self.layout.addWidget(self.usernameLE)
        
        # Nur ein Button für Weiter
        self.skipButton = QPushButton("Weiter!")
        self.layout.addWidget(self.skipButton)

        
        def on_button_clicked_skip():

            if(self.usernameLE.text() is None):
                self.username = "anon"
                
            self.username = self.usernameLE.text()
            self.app.exit()

        self.skipButton.clicked.connect(on_button_clicked_skip)

        # Das oben erstellte Layout dem Fenster zuweisen und das Fenster öffnen
        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec()

    def savePlayerdataToDatabase(self) -> None: # public
        try:
            verbindung = mysql.connector.connect(user=self.MY_SQL["user"], password=self.MY_SQL["password"], host=self.MY_SQL["host"], database=self.MY_SQL["db"])
            mycursor = verbindung.cursor()

            sqlBefehl = "INSERT INTO astlogin (level, points) VALUES ('%s', '%s') WHERE username = %s"
            mycursor.execute(sqlBefehl, (self.level, self.score, self.username ))
            
            
            verbindung.close()
        except Exeption as e:
            print(e)
      
    def updatePlayerdataFromDatabase(self) -> None: # private
        try:
            verbindung = mysql.connector.connect(user=self.MY_SQL["user"], password=self.MY_SQL["password"], host=self.MY_SQL["host"], database=self.MY_SQL["db"])
            mycursor = verbindung.cursor()

            sqlBefehl = "SELECT level, points FROM astlogin WHERE username = %s"
            mycursor.execute(sqlBefehl, (self.username, ))
            result = mycursor.fetchall()
            print(result)
            self.level = int(result[0][0])
            self.score = int(result[0][1])
            
            verbindung.close()
        except Exception as e:
            print(e)

    def savePlayerHighscoreToDatabase(self) -> None: # public
        # only update the playerdata if it was higher than when last saved
        oldScore = self.score
        oldLevel = self.level
        self.updatePlayerdataFromDatabase()

        if(self.score > oldScore or self.level > oldLevel):
            self.savePlayerdataToDatabase()
            self.highscore = self.score
            self.highlevel = self.level

    def __str__(self) -> str:
        out = "Spieler: " + str(self.username) + "\n"
        out += "Highscore: " + str(self.highscore) + " Punkte bei Level "  + str(self.highlevel) + "\n"
        out += "Level: " + str(self.level) + "\n"
        out += "Punkte: " + str(self.score) + "\n"

        return out

    def __init__(self, MY_SQL=None) -> None:
        
        self.myParser = ConfigParser()
        self.filename = "Spiel/scores.ini"

        if(os.path.isfile(self.filename)):
            self.myParser.read_file(self.filename)
        
        else: # if the file doesn't exist
            newfile = open(self.filename, 'w')
            self.myParser.add_section("main")
            self.myParser.write(newfile)
            newfile.close()

            self.myParser.read(self.filename)

        self.qtBox()
        self.updatePlayerdataFromDatabase()

        # Variablen mit highscore, die nur bei init und neuem highscore überschrieben werden
        self.highscore = self.score
        self.highlevel = self.level

