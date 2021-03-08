import mysql.connector
import bcrypt


verbindung = mysql.connector.connect(user='root', password='root', host='localhost', database='testdb')

username = input("Neuer Username: ")
password = input("Neues Passwort: ")

mycursor = verbindung.cursor()
sqlBefehl = "SELECT * FROM testtabelle WHERE username = '" + username + "';"
mycursor.execute(sqlBefehl)
# ?? mycursor.fetchall()

if not mycursor.rowcount: # Wenn das Ergebnis leer ist
    print("Username noch nicht vergeben")
    




password = password.encode("utf-8")
pwHashed = pwHashed.encode("utf-8")

if bcrypt.checkpw(password, pwHashed):
    print("Login Erfolgreich")
else:
    print("Falsches Passwort")



verbindung.close()