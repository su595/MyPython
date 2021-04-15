import mysql.connector


class LittleDBHelper():


    def neuerEintrag(self, inhalt):

        # Hier wird eine Query ausgeführt, die den übergebenen Wert inhalt in die Tabelle einfügt
        query = "INSERT INTO `testtabelle` (`Name`) VALUES (%s);"
        self.mycursor.execute(query, (inhalt, ))


    def datenAnzeigen(self):

        # Hier wird alles aus der Tabelle abgefragt und mit einem for Loop aufgelistet und ausgedruckt
        self.mycursor.execute("Select * FROM testtabelle")
        ausgabe = self.mycursor.fetchall()

        ausgabeRes = ""
        for x in ausgabe:
            ausgabeRes += str(x) + "\n"
        
        print(ausgabeRes)


    def __init__(self):

        # Verbindung aufbauen und cursor definieren
        self.verbindung = mysql.connector.connect(user='root', password='root', host='localhost', database='testdb')
        self.mycursor = self.verbindung.cursor()

        neuerName = str(input("Neuer Name eintragen (sonst leerlassen): "))
        
        if not len(neuerName) == 0:
            self.neuerEintrag(neuerName)
        
        self.datenAnzeigen()

        # Am Ende Verbindung wieder schließen
        self.verbindung.close()


myHelper = LittleDBHelper()
