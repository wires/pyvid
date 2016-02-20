import random
import path
import math

from example import *

class Movie:
    def __init__(self, path):
        self.opacity = 0.0
        self.path = path
        self.mov = QTMovie(path)
        # decode first frame once
        self.mov.decode()
           
class Set:
    def __init__(self, name, movies, files):
        self.movies = movies
        self.name = name
        self.files = files
                                    
class MIDI:
    def __init__(self):
        self.CCs = []
        self.Notes = []
        self.midiin = RtMidiIn()
        self.msgQueue = msgVector()
        
        for i in range(128):
            self.CCs.append(0.0)
            self.Notes.append(0.0)
    
    def process(self):
        # process MIDI event (at most 100 midi messages inbetween frames)
        change = False
        cnt = 0
        while(cnt < 100):
            self.midiin.getMessage(self.msgQueue)
            if(len(self.msgQueue) == 0):
                break
            cnt += 1
            self.parse(self.msgQueue)
            change = True

        return change
        
    def parse(self, z):
        # parse note on/note off
        if (z[0] == 144):
            self.Notes[z[1]] = z[2] / 128.0

        # parse cc
        elif (z[0] == 176):
            self.CCs[z[1]] = z[2] / 128.0
        
        # parse aftertouch
        elif (z[0] == 160):
            self.Notes[z[1]] = z[2] / 128.0
        
        # unknown msg, display to console
        else:
            c = 0
            for i in z:
                c += 1
                print "%s = %s" % (c, i)

class SetManager:
    def __init__(self, dir):
        self.active = 0
        self.files = []
        self.movies = []

        # scan all files
        for dir in path.path(dir).dirs():
            i = 1
            files = []
            for file in dir.walkfiles():
                if(file[-4:] != '.mov'):
                    continue;

                # store files and movie instances
                self.files.append(file)
                mov = Movie(file)
                self.movies.append(mov)
                print "loaded %s" % file
        
        self.reorder(0)
        
    def reorder(self, size):
        banking = True
        if(size == 0):
            banking = False
            size = 18
            
        self.sets = []
        setCount = int(math.ceil(float(len(self.movies)) / float(size)))
        for i in range(setCount):
            movies = self.movies[(i*size):][:size]
            files  = self.files[(i*size):][:size]
            if(banking):
                text = "Bank %d" % i
            else:
                text = "Clips %d-%d" % ((i*size), (i*size) + (len(files)))
            self.sets.append(Set(text, movies, files))

class MidiMap:
    # TODO rewite midi mapper with applyNoteOn() applyNoteOff() applyCC applyAftertouch  ,
    def __init__(self):
        self.offsetScale = 0
        self.offset = 0;

    def applySet(self, midiparser, system, activeSet, noteOffset):
        for i in range(len(activeSet.movies)):
                    note = midiparser.Notes[i + noteOffset]
                    if(system.fullLevels):
                        note = math.ceil(note)
                    if(system.halfLevels):
                        note = math.ceil(note)/2
                    if(note > 0.0):
                        activeSet.movies[i].opacity = note
                        activeSet.movies[i].mov.start()
                    else:
                        # don't stop movies if hold is on
                        if(not system.hold):
                            activeSet.movies[i].opacity = 0.0
                            activeSet.movies[i].mov.stop()
            
                            
                        
    def apply(self, midiparser, system):
        # banking or not
        if(self.offsetScale != 0):
            self.applySet(midiparser, system, system.setman.sets[system.setman.active], 0)
        else:
            for j in range(len(system.setman.sets)):
                self.applySet(midiparser, system, system.setman.sets[j], (18 * j))
                
                
            
class System:
    def __init__(self):
        
        # setup midi parser
        self.midiparser = MIDI()
        
        self.midimapper = MidiMap()
        
        self.blanking = True
        self.hold = False
        self.mute = False
        self.fullLevels = False
        self.halfLevels = False
        
        # scan midi ports
        self.midiPorts = ['None']
        for i in range(self.midiparser.midiin.getPortCount()):
            self.midiPorts.append(self.midiparser.midiin.getPortName(i))
        #self.midiparser.midiin.openPort(1)
            
        self.setman = SetManager('footage')

    def panic(self):
        # panic
        for set in self.setman.sets:
            for movie in set.movies:
                movie.mov.stop()
                movie.opacity = 0.0
        
        for note in self.midiparser.Notes:
            note = 0.0
        
        for cc in self.midiparser.CCs:
            cc = 0.0

        # empty midi queue
        self.midiparser.midiin.closePort()
        
        
    def processMidiEvents(self):
        # process some midi events
        change = self.midiparser.process()
        if(change):
            self.midimapper.apply(self.midiparser, self)
