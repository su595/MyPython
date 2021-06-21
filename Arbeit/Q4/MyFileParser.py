from configparser import ConfigParser
import mysql.connector

USER = "root"
PASSWORD = "root"
HOST = "localhost"
DATABASE = "ParserDB"

class MyFileParser():

    def __init__(self, pfad="Q3python/Q4 Arbeit/user.ini") -> None:

        self.pfad = pfad
        
        # Achtung:  bei falschem Pfad kommt kein Error, sondern einfach falsche Werte!
        self.myCursor = ConfigParser()
        self.myCursor.read(self.pfad)

        self.myConfigPrint()

        self.alterUserFile("Email", "neuHerbert@uwu.com")

        self.myConfigPrint()

        if(self.writeCursorToDatabase()):
            self.readValuesFromDatabase()

    def alterUserFile(self, option, data):
        # cursor anpassen
        self.myCursor.set("user", option, data)

        file = open(self.pfad, "w")

        # neuen cursor in die file schreiben
        self.myCursor.write(file)

        # file danach schließen nicht vergessen
        file.close()

    def myConfigPrint(self):
    
        # cursor updaten
        self.myCursor.read(self.pfad)

        # den kompletten Cursor printen
        for i in self.myCursor:
            print(self.myCursor[i])
            for i2 in self.myCursor[i]:
                print(i2 + ": " + self.myCursor[i][i2])
        
        print("\n")

    def writeCursorToDatabase(self) -> bool:

        # ich glaube normalerweise ist eine checksum was anderes aber irgendwie passt der Name hier ;)
        checksum = 0

        # funktioniert nur wenn myCursor nur einen Abschnitt hat, müsste geändert werden!!!
        for i in self.myCursor:
            for i2 in self.myCursor[i]:

                if(i2 == "name"):
                    name = self.myCursor[i][i2]
                    checksum += 1

                if(i2 == "lastname"):
                    lastname = self.myCursor[i][i2]
                    checksum += 1

                if(i2 == "email"):
                    email = self.myCursor[i][i2]
                    checksum += 1
            
                if(i2 == "password"):
                    pw = self.myCursor[i][i2]
                    checksum += 1

        # wenn nicht alles gefunden wurde
        if(checksum != 4):
            print(".ini ist unvollständig")
            return False

        
        try:
            verbindung = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
            dbCursor = verbindung.cursor()

            sqlBefehl = "INSERT INTO main (name, lastname, email, pw) VALUES (%s, %s, %s, %s) "

            dbCursor.execute(sqlBefehl, (name, lastname, email, pw))

            verbindung.close()

            return True

        except Exception as e:
            print(e)
            return False

    def readValuesFromDatabase(self):

        try:
            verbindung = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
            dbCursor = verbindung.cursor()

            sqlBefehl = "SELECT * FROM main"

            dbCursor.execute(sqlBefehl)
            result = dbCursor.fetchall()

            for x in result:
                out = "ID: " + result[x][0] + "\n"
                out += "name: " + result[x][1] + "\n"
                out += "lastname: " + result[x][2] + "\n"
                out += "email: " + result[x][3] + "\n"
                out += "password: " + result[x][4] + "\n"
                print(out)

            verbindung.close()

        except Exception as e:
            print(e)


MyFileParser()
