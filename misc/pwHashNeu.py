import mysql.connector
import bcrypt


verbindung = mysql.connector.connect(user='root', password='root', host='localhost', database='testdb')

# Platzhalter für QT Box
username = input("Neuer Username: ")
password = input("Neues Passwort: ")

mycursor = verbindung.cursor()

# Hier wird eine Variable mit dem %s in der SQL-Query "vermerkt", damit beim Ausführen des Befehls dort die Variable username eingefügt werden kann
sqlBefehl = "SELECT pw FROM testtabelle WHERE username = %s"
mycursor.execute(sqlBefehl, (username, ))


pwHashed = mycursor.fetchall()

if not mycursor.rowcount: # Wenn das Ergebnis leer ist
    print("Kein User mit diesem Username")

for x in pwHashed:
    # funktioniert aufjedenfall wenn es nur ein Ergebnis bei der Query gibt (was hier der Fall ist)
    pwHashed = x[0]



password = password.encode("utf-8")
pwHashed = pwHashed.encode("utf-8")

if bcrypt.checkpw(password, pwHashed):
    print("Login Erfolgreich")
else:
    print("Falsches Passwort")



verbindung.close()
