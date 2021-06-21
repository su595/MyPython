from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from direct.task.Task import Task

PATH = "Spiel/sounds/stone.ogg"


class MusikPanda(ShowBase):

    def setProperties(self):
        # set properties of the window
        properties = WindowProperties()
        properties.setSize(800, 600)
        properties.setTitle("Titel des Fensters")
        self.win.requestProperties(properties)

        self.disableMouse()
        # pink yay
        self.setBackgroundColor((255, 0, 128, 1))
        
    def makeMusic(self, path, loop=False):
        self.music = self.loader.loadSfx(path)
        self.music.setLoop(loop)
        self.music.setVolume(1)
        self.music.play()
        print("start")
    
    def musicStop(self):
        self.music.stop()
        print("stop")

    def registerInputs(self):
        self.keys = {"space": 0}
        
        self.accept("space",            self.setKey, ["space", 1])

    def setKey(self, key, val):
        self.keys[key] = val

    def gameLoop(self, task):
        # hier wird bei drücken von space einmal die musik abgespielt
        if(self.keys["space"]):
            self.setKey("space", 0)

            if self.isMusicPlaying:
                self.isMusicPlaying = False
                self.musicStop()

            else:
                self.isMusicPlaying = True
                # zum testen ein fester Pfad
                self.makeMusic(PATH, True)

        # Ein return Task.cont heißt, der taskMgr lässt den taskLoop continuen/weiterlaufen
        return Task.cont
  
    def __init__(self):
        # Showbase und das Fenster konfigurieren
        ShowBase.__init__(self)
        self.setProperties()

        self.registerInputs()

        self.isMusicPlaying = False

        # GameLoop starten
        self.gameTask = self.taskMgr.add(self.gameLoop, "gameLoop")


myMusikPanda = MusikPanda()
myMusikPanda.run()
