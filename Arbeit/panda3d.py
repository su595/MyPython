from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties


class MyLittlePanda(ShowBase):


    def loadObject(self, dateipfadModel, dateipfadTextur, scale):

        # Modell laden, zur camera verschieben und scale setzten
        self.scene = self.loader.loadModel(dateipfadModel) 
        self.scene.reparentTo(self.camera)
        self.scene.setScale(scale)
        # Position hab ich hier erstmal festgelegt, macht nicht viel aus
        self.scene.setPos(0, 2, 0)

        # Textur laden
        self.texture = self.loader.loadTexture(dateipfadTextur)
        self.scene.setTexture(self.texture, 1)

    def __init__(self):
        ShowBase.__init__(self)

        # Hier werden die Window Properties definiert
        properties = WindowProperties()
        properties.setTitle("LKArbeitvonYannick2021")
        properties.setSize(800, 600)
        self.win.requestProperties(properties)

        self.disableMouse()
        self.setBackgroundColor((0, 0, 0, 1))

        self.loadObject("plane.egg", "hintergrund.jpg", 1)


myPanda = MyLittlePanda()
myPanda.run()

# Aus irgendeinem Grund spinnt der ShowBase import bei mir deswegen funktioniert garnichts :/
# Aber im Prinzip sollte das hier richtig sein