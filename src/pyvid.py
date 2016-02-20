import random
import time
import path

import macosx

from example import *
from model import *
from gui import *
from keymap import *

# init quicktime
QTMovie.init()

class GUI(Container):
    # init SDL
    def __init__(self, system, gc):
        Container.__init__(self, gc, 0, 0)
        self.height = gc.height()
        self.width = gc.width()
        self.t = time.time()
        self.frames = 0
        self.system = system
        
        # main view
        self.masterview = MasterView(self.gc, 0, 0)
        self.masterview.setSystem(self.system)
        self.children.append(self.masterview)

        self.topView = CardLayout(self.gc, 390, 0)
        self.topView.width = self.width - 390
        self.topView.height = 280
        
        # add sequencer widget
        p = Label(self.gc, 390,12)
        p.setText('seq')
        self.topView.addCard("Sequencer", p)

        # add midi view widget
        # TODO: make view relative to self.x self.y
        midiView = MIDIView(self.gc, 0, 0)
        midiView.setMidi(self.system.midiparser)
        self.topView.addCard("Midi View", midiView)

        # add midi device widget
        l = List(self.gc, 390, 12)
        l.setItems(system.midiPorts)
        self.topView.addCard("Midi setup", l)

        # add midi offset widget
        l = List(self.gc, 390, 12)
        l.setItems(["None", "Banksize 16", "Banksize 18"])
        self.topView.addCard("Midi Banking", l)
        
	    # add import message :-)
        l2 = List(self.gc, 390, 12)
        l2.setItems(["liv","is","lief"])
        self.topView.addCard("niets", l2)
        
        self.children.append(self.topView)
        
        # properties view
        container = ButtonContainer(self.gc, 390,280)
        self.panic = Label(self.gc, 0, 0)
        self.panic.setText("Panic 'p'")
        container.addButton(self.panic)
        
        self.hold = Label(self.gc, 0, 0)
        self.hold.setText("Hold 'o'")
        container.addButton(self.hold)
        
        self.fullLevels = Label(self.gc, 0, 0)
        self.fullLevels.setText("Full Levels 'L'")
        container.addButton(self.fullLevels)
        
        self.halfLevels = Label(self.gc, 0, 0)
        self.halfLevels.setText("Half Levels 'I'")
        container.addButton(self.halfLevels)

        self.blanking = Label(self.gc, 0, 0)
        self.blanking.setText("Blanking 'k'")
        self.blanking.active = True
        container.addButton(self.blanking)
                
        self.mute = Label(self.gc, 0, 0)
        self.mute.setText("Mute 'm'")
        container.addButton(self.mute)
        
        self.children.append(container)
    
        # set view
        self.setmanView  = SetManagerView(self.gc, 5, 290)
        self.setmanView.setSetManager(self.system.setman)
        self.children.append(self.setmanView)   
        
    def draw(self):
        # draw children
        Container.draw(self)
        
        # draw FPS counter
        self.frames += 1
        dt = time.time() - self.t
        fps = self.frames / dt
        self.gc.setColor(0.0,0.0,0.0)
        self.gc.fillRect(self.width - 40, 0, 40, 10)
        self.gc.drawText(self.width - 40, 0, "fps: %s" % str(int(fps)))
        
        # reset counter every 2.5 seconds
        if(dt > 8):
            self.frames = 0
            self.t = time.time()
        
        # flip screen
        self.gc.update()
        
run = True
width = 1024
height = 768

try:
    # setup SDL
    gc = Display()
    gc.create(width, height, False)
    
    # construct pyvid model
    system = System()

    # construct GUI
    gui = GUI(system, gc)
    
    # construct keyboard interface
    k = KeyboardInterf(system, gui)

    while(run):
        gui.draw()

        system.processMidiEvents()
    
        # process keyboard events (at most 5 inbetween frames)
        eventCounter = 0
        while(eventCounter<5):
            event = Event()
            if(not gc.pollEvents(event)):
                break
            eventCounter += 1;
            if event.quit:
                import sys
                sys.exit(0)
            if event.keyPress:
                k.processKey(int(event.key))
                
except QTError, e:
    print "FATAL, QTError: ", e.message();

except SDLError, e:
    print "FATAL, SDLError: ", e.message();

except TTFError, e:
    print "FATAL, TTFError: ", e.message();

except RuntimeError, e:
    print "FATAL, runtime_error: ", e.message();
