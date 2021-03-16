import bcrypt


class HashBrothers():

    def HashCodePrüfen(self):
        
        # Variablen für Bcrypt richtig encoden
        self.HashCode = self.HashCode.encode("utf-8")
        self.password = self.password.encode("utf-8")

        # Passwort checken
        if bcrypt.checkpw(self.password, self.HashCode):
            return True
        else:
            return False
    
    def __init__(self):
        
        self.password = input("Zu prüfendes Passwort: ")
        # Der vorgegebene Hash Code
        self.HashCode = "$2b$12$acCJTPaaIx56B9eG0nv9HOHp8zaC7PDlingzE68LyzUPSSfzv3sW6"

        if self.HashCodePrüfen():
            print("Passt")
        else:
            print("Passt nicht!")

myHaschisch = HashBrothers()

