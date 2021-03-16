import mysql.connector
import bcrypt


verbindung = mysql.connector.connect(user='root', password='root', host='localhost', database='testdb')

username = input("Username: ")
password = input("Passwort: ")

mycursor = verbindung.cursor()

# So geht es auch, die Query ist aber unübersichtlicher
sqlBefehl = "SELECT pw FROM testtabelle WHERE username = '" + username + "';"
mycursor.execute(sqlBefehl)

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