from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, TextNode

class Asteroider(ShowBase):


    def loadObject(self, dateipfadModel, dateipfadTextur, scale):
        self.scene = self.loader.loadModel(dateipfadModel) 
        # Reparent the model to render.
        self.scene.reparentTo(self.camera)
        # Apply scale and position transforms on the model.
        self.scene.setScale(scale)
        self.scene.setPos(0, 2, 0)
        # Textur laden
        self.texture = self.loader.loadTexture(dateipfadTextur)
        self.scene.setTexture(self.texture, 1)


    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(800, 600)
        properties.setTitle("Titel des Fensters")
        self.win.requestProperties(properties)

        self.disableMouse()
        self.setBackgroundColor((0, 0, 0, 1))

        # bei setText steht der angezeigte String
        text = TextNode("NameDerNode")
        text.setText("irgendStr")
        textNodePath = aspect2d.attachNewNode(text)
        textNodePath.setScale(0.1)
        


            
        
        

game = Asteroider()
game.run()