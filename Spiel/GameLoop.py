import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, ClockObject
from direct.task.Task import Task



class GameLoop(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(800, 600)
        properties.setTitle("Titel des Fensters")
        self.win.requestProperties(properties)
        self.accept("escape", sys.exit)

        self.zähler = 0
        self.myTask = self.taskMgr.add(self.taskLoop, "taskLoop")
    
    def taskLoop(self, task):
        globalClock = ClockObject.getGlobalClock()
        self.dt = globalClock.getDt()
        self.showFPS(self.dt)

        # Ein return Task.cont heißt, der taskMgr lässt den taskLoop continuen/weiterlaufen
        return Task.cont
    
    def showFPS(self, time):
        self.zähler += time
        # Alle halbe Sekunde
        if self.zähler >= 0.5:
            self.fpstext = "FPS: " + str(int(60/time))
            self.zähler = 0
            print(self.fpstext)

myGameLoop = GameLoop()
myGameLoop.run()