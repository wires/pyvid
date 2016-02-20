import time
import math
import types

class KeyboardInterf:

    keymap = [113, 97, 122, 119, 115, 120, 101, 100, 99, 114, 102, 118, 116, 103, 98, 121, 104, 110]
    
    def __init__(self, system, gui):
        self.system = system
        self.gui = gui
        self.escapeTime = 0.0
        
    def processKey(self, code):
        # keys 1-9
        if(code >= 49) and(code <= 57):
            i = code - 49
            self.gui.setmanView.setSelectedCard(i)
            self.system.midimapper.offset = i
            return
            
        # clip toggle keys
        if(code in self.keymap):
            i = self.keymap.index(code)
            # emulate a midi note press/release
            val = self.system.midiparser.Notes[i]
            self.system.midiparser.Notes[i] = 1.0 - math.ceil(val)
            self.system.midimapper.apply(self.system.midiparser, self.system)
            return
                        
        for (name, function) in KeyboardInterf.__dict__.items():
            # skip all functions not starting with "key"
            if(name[:3] != "key"):
                continue

            # skip all non-functions
            if(not isinstance(function, types.FunctionType)):
                continue


                
            fcode = int(name[3:])
            if(fcode != code):
                continue
            
            function.__call__(self)
            return
        
        print "unknown key, code %s" % code
        
                    
    
    # left -> topview prev
    def key276(self):
        self.gui.topView.down()
    
    # right -> topview next
    def key275(self):
        self.gui.topView.up()
        
    # quickly press escape twice within .5 seconds to exit
    def key027(self):    
        if (time.time() - self.escapeTime < 0.5):
            import sys
            sys.exit(0)
        self.escapeTime = time.time()
    
    # up key
    def key274(self):
        # move list up (only c=1, c=2 are lists)
        c = self.gui.topView.selectedCard
        if(c > 1):
            self.gui.topView.cards[c][2].up()
    
    # down key
    def key273(self):
        # move list down (only c=1, c=2 are lists)
        c = self.gui.topView.selectedCard
        if(c > 1):
            self.gui.topView.cards[c][2].down()
            
    # enter key
    def key013(self):
        # select active
        c = self.gui.topView.selectedCard
        if(c > 1):
            list = self.gui.topView.cards[c][2];
            list.active = list.selected
            if(c == 2):
                # open selected midi port
                self.system.midiparser.midiin.closePort()
                if(list.active > 0):
                    self.system.midiparser.midiin.openPort(list.active - 1)
            if(c == 3):
                if(list.active == 0):
                    self.system.midimapper.offsetScale = 0
                    self.system.setman.reorder(0)
                if(list.active == 1):
                    self.system.midimapper.offsetScale = 16
                    self.system.setman.reorder(16)
                if(list.active == 2):
                    self.system.midimapper.offsetScale = 18
                    self.system.setman.reorder(18)
                # force gui refresh
                self.gui.setmanView.setSetManager(self.system.setman)
                
    
    # spatie LOAD SET
    def key032(self):
        i = self.gui.setmanView.selectedCard
        self.gui.setmanView.activeCard = i
        self.system.setman.active = i

    

        
    def key048(self):
        self.gui.setmanView.setSelectedCard(9)
        self.system.midimapper.offset = 9

    # panic 'P'
    def key112(self):
        self.system.panic()
    
    # hold 'O'
    def key111(self):
        # toggle hold
        status = not self.gui.hold.active
        self.gui.hold.active = status
        self.system.hold = status
    
    # full levels 'L'
    def key108(self):
        status = not self.gui.fullLevels.active
        self.gui.fullLevels.active = status
        self.system.fullLevels = status
        if(status):
            self.gui.halfLevels.active = False
            self.system.halfLevels = False

    # full levels 'L'
    def key105(self):
        status = not self.gui.halfLevels.active
        self.gui.halfLevels.active = status
        self.system.halfLevels = status
        if(status):
            self.gui.fullLevels.active = False
            self.system.fullLevels = False

    # blanking 'K'
    def key107(self):
        status = not self.gui.blanking.active
        self.gui.blanking.active = status
        self.system.blanking = status

    # mute 'M'
    def key109(self):
        status = not self.gui.mute.active
        self.gui.mute.active = status
        self.system.mute = status
                