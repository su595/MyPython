
# Arbeitsauftrag:
# Erstellen Sie eine Klasse Student
# Diese Soll sinnvolle Werte beinhalten wie:
#     Name, Vorname, Alter, Fach, Note1, Note2
#     Eine Methode die den Mittelwert der Noten bestimmt
#     Studenten sollen mit Ihren Daten und dem Mittelwert einfach durch print(myStudent1) ausgegeben werden können

# Zeigen Sie das sie eine Verwaltungsklasse Implementieren können, die durch Eingabe(Input) Studenten erzeugt und auf Wunsch alle erstellten Ausgibt!


class Student():

    def __init__(self, Name, Vorname, Note1, Note2, Alter=0, Fach=""):

        # Übergebene Werte zu "Objekt-Variablen" zuweisen
        self.Name = Name
        self.Vorname = Vorname
        self.Alter = Alter
        self.Fach = Fach
        self.Note1 = Note1
        self.Note2 = Note2
    
    def mittelwertErrechnen(self):

        # Mittelwert aus den zwei Noten errechnen
        self.Mittelwert = (self.Note1 + self.Note2) / 2

        return self.Mittelwert
    
    def __str__(self):
        
        Ausgabe = "____________________________ \n"
        Ausgabe += "Name: " + self.Name + "\n"
        Ausgabe += "Vorname: " + self.Vorname + "\n"
        Ausgabe += "Alter: " + str(self.Alter) + "\n"
        Ausgabe += "Fach: " + self.Fach + "\n"
        Ausgabe += "Note1: " + str(self.Note1) + "\n"
        Ausgabe += "Note2: " + str(self.Note2) + "\n"
        Ausgabe += "Mittelwert: " + str(self.mittelwertErrechnen()) + "\n"

        return Ausgabe


class StudentVerwaltung():


    def __init__(self):
        
        # Eine Liste für alle von diesem StudentVerwaltung-Objekt erstellte Students
        self.studentList = []

        Schleife = True
        while Schleife:
            if len(input("Neuer Student? (leerlassen wenn nein) ")):
                self.newStudent()
            
            if len(input("Alle Students darstellen? (leerlassen wenn nein) ")):
                self.displayStudents()
            
            if len(input("Willste weiter machen? (leerlassen wenn ja)")):
                Schleife = False

    def newStudent(self):
        
        # Alle Werte für einen Student werden mit input() abgefragt und in einer lokalen Variable zwischengespeichert
        Name = str(input("Name "))
        Vorname = str(input("Vorname "))
        Alter = int(input("Alter "))
        Fach = str(input("Fach "))
        Note1 = int(input("Note1 "))
        Note2 = int(input("Note2 "))

        # Mit diesen Werten einen neuen Student machen und in die studentListe reinmachen
        self.studentObject = Student(Name, Vorname, Note1, Note2, Alter, Fach)
        self.studentList.append(self.studentObject)
    
    def displayStudents(self):

        for i in self.studentList:
            # hier werden alle Student-Objekte in der studentList geprinted (mit deren __str__ methode)
            print(i)


# Diese Students werden von der Studentverwaltung nicht angezeigt, weil sie seperat erstellt wurden und nicht in der studentList stehen
daniel = Student("Pcimann", "Daniel", 69, "EinFach", 13, 3)
john = Student("Rosenpflanze", "John", 2, "AnderesFach", -420, 9)

Verwaltung = StudentVerwaltung()


