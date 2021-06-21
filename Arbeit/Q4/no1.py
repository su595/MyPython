

class Fahrzeug():

    def __init__(self, nr, leerg, zGesGew) -> None:
        self.fahrzeugnummer = str(nr)
        self.leergewicht = float(leerg)
        self.zulaessigesGesamtGewicht = int(zGesGew)

    def __str__(self) -> str:
        out = self.fahrzeugnummer + "\n"
        out += str(self.leergewicht) + "\n"
        out += str(self.zulaessigesGesamtGewicht) + "\n"

        return out


class PKW(Fahrzeug):

    def __init__(self, nr, leerg, zGesGew, leistung, hoechstgeschwindigkeit) -> None:
        super().__init__(nr, leerg, zGesGew)

        self.leistungKW = float(leistung)
        self.hoechstgeschwindigkeit = int(hoechstgeschwindigkeit)

    def __str__(self) -> str:
        out = super().__str__()
        out += str(self.leistungKW) + "\n"
        out += str(self.hoechstgeschwindigkeit) + "\n"

        return out


class Fahrrad(Fahrzeug):

    def __init__(self, nr, leerg, zGesGew, rahmenhoehe, bezeichnung) -> None:
        super().__init__(nr, leerg, zGesGew)

        self.rahmenhoehe = int(rahmenhoehe)
        self.bezeichnung = str(bezeichnung)

    def __str__(self) -> str:
        out = super().__str__()
        out += str(self.rahmenhoehe) + "\n"
        out += str(self.bezeichnung) + "\n"

        return out


# TEST:
# Fahrr = Fahrrad(1, 6.8, 80, 60, "tolles ding")
# print(Fahrr)

# aut = PKW(44, 1300.56, 420, 100, 54)
# print(aut)

class Fahrzeugvermietung():

    def __init__(self) -> None:
        self.myFahrzeug = Fahrzeug(1,2,3)
        self.myFahrrad = Fahrrad(3,35,333,40,"sktj")
        self.myPkw = PKW(24,56,22,74,112)

        self.printAllVehicles()
    
    def printAllVehicles(self):
        print(self.myFahrzeug)
        print(self.myFahrrad)
        print(self.myPkw)

Fahrzeugvermietung()