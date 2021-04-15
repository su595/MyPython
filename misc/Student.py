
# self.Name = str(input("Name "))
# self.Vorname = str(input("Vorname "))
# self.Alter = int(input("Alter "))
# self.Fach = str(input("Fach "))
# self.Note1 = int(input("Note1 "))
# self.Note2 = int(input("Note2 "))
# self.Note3 = int(input("Note3 "))


class Student():

    def __init__(self, Name="", Vorname="", Alter=0, Fach="", Note1=0, Note2=0):

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

        # While Schleife nur zum Test!
        while True:
            if len(input("Neuer Student? (leerlassen wenn nein) ")):
                self.newStudent()
            
            if len(input("Alle Students darstellen? (leerlassen wenn nein) ")):
                self.displayStudents()

    def newStudent(self):
        
        # Alle Werte für einen Student werden mit input() abgefragt
        self.Name = str(input("Name "))
        self.Vorname = str(input("Vorname "))
        self.Alter = int(input("Alter "))
        self.Fach = str(input("Fach "))
        self.Note1 = int(input("Note1 "))
        self.Note2 = int(input("Note2 "))

        # Mit diesen Werten einen neuen Student machen und in die studentListe reinmachen
        self.studentObject = Student(Name=self.Name, Vorname=self.Vorname, Alter=self.Alter, Fach=self.Fach, Note1=self.Note1, Note2=self.Note2)
        self.studentList.append(self.studentObject)
    
    def displayStudents(self):

        for i in self.studentList:
            # hier werden alle Student-Objekte in der studentList geprinted (mit deren __str__ methode)
            print(i)


# Diese Students werden von der Studentverwaltung nicht angezeigt, weil sie seperat erstellt wurden und nicht in der studentList stehen
daniel = Student("Pcimann", "Daniel", 69, "EinFach", 13, 3)
john = Student("Rosenpflanze", "John", 2, "AnderesFach", 14, 9)


Verwaltung = StudentVerwaltung()
# Wegen der while schleife in der StudentVerwaltung.__init__ kann hiernach nichts mehr ausgeführt werden



