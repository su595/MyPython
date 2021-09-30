from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

class Asteroider(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(800, 600)
        properties.setTitle("Fenster Titel")
        self.win.requestProperties(properties)

        self.disableMouse()
        self.setBackgroundColor((0, 0, 0, 1))

        self.scene = self.loader.loadModel("models/planeNeu.egg") 
        # Reparent the model to render.
        self.scene.reparentTo(self.camera)
        # Apply scale and position transforms on the model.
        self.scene.setScale(10)
        self.scene.setPos(0, 55, 0)
        # Textur laden
        self.texture = self.loader.loadTexture("textures/stars.jpg")
        self.scene.setTexture(self.texture, 1)


class Player:
    def __init__(self, name, lastname, email, id, level, points):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.id = id
        self.level = level
        self.points = points
    
    def printPlayer(self):
        playerStr = "------------------------------ \n"
        playerStr += str(self.name) + "\n"
        playerStr += str(self.lastname) + "\n"
        playerStr += str(self.email) + "\n"
        playerStr += str(self.id) + "\n"
        playerStr += str(self.level) + "\n"
        playerStr += str(self.points) + "\n"
        playerStr += "------------------------------"

        return playerStr


        
spieler1 = Player("Yannick", "Hein", "email von mir", 1, 69, 100)
print(spieler1.printPlayer())

game = Asteroider()
game.run()