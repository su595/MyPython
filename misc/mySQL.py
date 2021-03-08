import mysql.connector
import bcrypt

verbindung = mysql.connector.connect(user='root', password='root', host='localhost', database='testdb')

mycursor = verbindung.cursor()
mycursor.execute("Select * FROM testtabelle")
ausgabe = mycursor.fetchall()


ausgabeRes = "Liste aller Ergebnisse: \n"
for x in ausgabe:
    ausgabeRes += str(x) + "\n"

print(ausgabeRes)

verbindung.close()