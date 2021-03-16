

class HooniganTuning():
    

    def __init__(self):
        print("Welcome to HooniganTuning! ")

        # Hier werden die Werte der Variablen über das Terminal erfragt
        self.Marke = str(input("\nMarke: "))
        self.Modell = str(input("\nModell: "))
        self.PS = int(input("\nPS (Zahl): "))
        self.Farbe = str(input("\nFarbe: "))

        # Ein String kann man nicht einfach in ein Boolean umwandeln, also teste ich hier, 
        # ob der input leer ist und wenn ja, setzte ich Elektro manuell auf false
        temp = str(input("\nElektro (leerlassen, wenn kein Elektro): "))

        self.Elektro = True
        if len(temp) == 0:
            self.Elektro = False
        

        myAuto = Auto(self.Marke, self.Modell, self.PS, self.Farbe, self.Elektro)

        myAuto.tuning()
        print(myAuto)


class Auto():

    def __init__(self, Marke, Modell, PS, Farbe, Elektro):
        
        self.myMarke = Marke
        self.myModell = Modell
        self.myPS = PS
        self.myFarbe = Farbe
        self.myElektro = Elektro

    
    def __str__(self):

        # Die Eigenschaften vom Auto werden mit str() zu einem String konvertiert, dann etwas "dekoriert"  
        # und zusammen in einen einzigen String outputStr addiert, der zurückgegeben wird
        outputStr = "Marke: " + str(self.myMarke) + "; "
        outputStr += "Modell: " + str(self.myModell) + "; "
        outputStr += "PS: " + str(self.myPS) + "; "
        outputStr += "Farbe: " + str(self.myFarbe) + "; "
        outputStr += "Elektro: " + str(self.myElektro) + "; "

        return outputStr


    def tuning(self):

        # PS um den Faktor 1.15 erhöhen und runden, damit es besser aussieht
        self.myPS = round(self.myPS * 1.15)
    

myTuning = HooniganTuning()
