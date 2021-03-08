

class Player:

    def __init__(self, name, id, level, points):
        self.name = name
        self.id = id
        self.level = level
        self.points = points
    
    def __str__(self):
        playerStr = "------------------------------ \n"
        playerStr += str(self.name) + "\n"
        playerStr += str(self.id) + "\n"
        playerStr += str(self.level) + "\n"
        playerStr += str(self.points) + "\n"
        playerStr += "------------------------------"

        return playerStr
    
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name

