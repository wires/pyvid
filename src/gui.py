import random

class Panel:
    def __init__(self, gc, x, y):
        self.gc = gc
        self.x = x
        self.y = y
    
class Container(Panel):
    def __init__(self, gc, x, y):
        self.children = []
        self.gc = gc
        self.x = x
        self.y = y

    def draw(self):
        for child in self.children:
            child.draw()

class MIDIView(Panel):
    def setMidi(self, midi):
        self.midi = midi
        
    def draw(self):
        self.gc.setColor(0.0,0.0,0.0)
        self.gc.fillRect(400, 10, 300, 200)

        self.gc.drawText(400, 10, "CCs:")
        for j in range(8):
            line = ''
            for i in range(16):
                v = self.midi.CCs[i+(j*16)]
                if(v != 0):
                    line = ('%0.2f ' % v)
                else:
                    line = " .   "
                self.gc.drawText(400 + i * 20,20 + j * 8, line)

        self.gc.drawText(400, 100, "Notes:")
        for j in range(8):
            line = ''
            for i in range(16):
                v = self.midi.Notes[i+(j*16)]
                if(v != 0):
                    line = ('%0.2f ' % v)
                else:
                    line = " .   "
                self.gc.drawText(400 + i * 20,110 + j * 8, line)
                
        
class MasterView(Panel):
    def setSystem(self, system):
        self.system = system
        
    def draw(self):
        if(self.system.blanking) or (self.system.mute):
            self.gc.setColor(0.0,0.0,0.0)
            self.gc.fillRect(0,0,384,288)
            if(self.system.mute):
                return
        i = 0
        for set in self.system.setman.sets:
            for movie in set.movies:
                i+=1
                if(movie.opacity > 0.0):
                    if(not movie.mov.playing()):
                        movie.mov.start()
                    movie.mov.decode()
                    surface = movie.mov.lock()
                    self.gc.blit(surface, movie.opacity)

class MovieThumbnailView(Panel):
    # thumbnail dimensions
    tw = 160
    th = 120
    
    def setMovie(self, movie):
        self.movie = movie

        # thumbnail crop coordinates
        self.w = self.movie.mov.width()
        self.h = self.movie.mov.height()
        self.tx = int((self.w - self.tw) * random.random())
        self.ty = int((self.h - self.th) * random.random())
        
        # decode thumbnail
        self.thumbnail = self.movie.mov.lock()
        
    def draw(self):
        if(self.movie.opacity > 0.0):
            self.gc.setColor(1.0,0.0,0.0)
        else:
            self.gc.setColor(0.0,0.0,0.0)
        self.gc.fillRect(self.x-2, self.y-2, self.tw+4, self.th+4)
        self.gc.blit(self.thumbnail,self.tx,self.ty,self.tw,self.th, self.x, self.y, 1.0)
        self.gc.drawText(self.x, self.y + 2 + self.th, self.movie.path.name)
        if(self.w != 384) or (self.h != 288):
            self.gc.drawText(self.x, self.y + 10 + self.th, "%1.2f    (%sx%s)" % (self.movie.opacity, self.w, self.h))
        else:
            self.gc.drawText(self.x, self.y + 10 + self.th, "%1.2f" % (self.movie.opacity))

class SetView(Container):
    def setSet(self, set):
        self.set = set
    
        # movie thumbnail widgets
        x = self.x
        y = self.y
        height = self.gc.height()
        for movie in set.movies:
            view = MovieThumbnailView(self.gc, x, y)
            view.setMovie(movie)
            self.children.append(view)
            
            y += view.th + 20
            if(y + view.th + 30 > height):
                x += view.tw + 10
                y = self.y


class Label(Panel):
    active = False
    selected = False
    width = -1
    text = ''
    
    def setText(self, text):
        self.text = text
        self.width = self.gc.getTextWidth(self.text)
    
    def draw(self):
        if(self.width == -1):
            return
        if (self.selected):
            self.gc.setColor(0.5,0.5,0.5)
        elif(self.active):
            self.gc.setColor(0.3,0.5,0.3)
        else:
            self.gc.setColor(0.2,0.2,0.2)
        self.gc.fillRect(self.x, self.y, self.width+4, 10)
        self.gc.drawText(self.x+2, self.y+2, str(self.text))
        
                
class CardLayout(Panel):
    
    def __init__(self, gc, x, y):
        self.labelx = x
        self.x = x
        self.y = y
        self.gc = gc
        self.selectedCard = 0
        self.activeCard = 0
        self.cards = []    
    
        self.width = False
        self.height = False
    
    def up(self):
        if(self.selectedCard < len(self.cards) - 1):
            self.selectedCard += 1
    
    def down(self):
        if(self.selectedCard > 0):
            self.selectedCard -= 1

    def setSelectedCard(self, i):
        # clip to nr of cards in layout
        if(i < len(self.cards)):
            self.selectedCard = i
        else:
            self.selectedCard = len(self.cards) - 1
        
    def addCard(self, name, panel):

        # draw indicator
        label = Label(self.gc, self.labelx, self.y)
        label.setText(name)
        
        # shift label x position
        self.labelx += label.width + 10
        
        # store name, label and panel
        self.cards.append((name, label, panel))
        
    # if width/height != false, fill background
    def draw(self):
        if(self.width) and (self.height):
            self.gc.setColor(0.0,0.0,0.0)
            self.gc.fillRect(self.x,self.y,self.width,self.height)
            
        i = 0
        for (name, label, panel) in self.cards:
            label.selected = (self.selectedCard == i)
            label.active = (self.activeCard == i)
            label.draw()
            # draw if selected panel
            if(label.selected):
                panel.draw()
            
            i += 1

class SetManagerView(CardLayout):
    def setSetManager(self, manager):
        self.manager = manager
        self.cards = []
        self.labelx = self.x
        for set in manager.sets:
            # shift y postion for labels
            view = SetView(self.gc, self.x, self.y + 15)
            view.setSet(set)
            self.addCard(set.name, view)

    def draw(self):
        self.gc.setColor(0.1,0.1,0.1)
        self.gc.fillRect(0, self.y, self.gc.width(), self.gc.height() - self.y - 10)
        CardLayout.draw(self)

class List(Panel):
    itemHeight = 10

    def up(self):
        if(self.selected < len(self.items) - 1):
            self.selected += 1
    
    def down(self):
        if(self.selected > 0):
            self.selected -= 1

    def setItems(self, items):
        self.items = items
        self.selected = 0
        self.active = 0
        self.width = -1
        
        self.height = len(items) * self.itemHeight 
        
        i = 0
        for item in self.items:
            self.width = max(self.width, self.gc.getTextWidth(self.itemString(i, item)))
            i+=1
        
    def itemString(self, i, item):
        return "%2d. %s" % (i, str(item))
        
    def draw(self):
        
        self.gc.setColor(0.3,0.3,0.3)
        self.gc.fillRect(self.x, self.y, self.width+4, self.height+4)

        i = 0
        for item in self.items:
            if(self.active == i):
                self.gc.setColor(0.2,0.9,0.2)
                self.gc.fillRect(self.x, self.y+2 + (i * self.itemHeight), self.width+4, self.itemHeight)
            if (self.selected == i):
                self.gc.setColor(0.5,0.5,0.5)
                self.gc.fillRect(self.x+2, self.y+2 + (i * self.itemHeight), self.width, self.itemHeight)
            self.gc.drawText(self.x+2, self.y+2 + (i * self.itemHeight), self.itemString(i, item))
            i += 1
            
class ButtonContainer(Container):
    def __init__(self, gc, x, y):
        Container.__init__(self, gc, x, y)
        self.labelx = 0
        
    def addButton(self, button):
        button.x += self.x + self.labelx
        button.y += self.y
        self.children.append(button)
        self.labelx += button.width + 10
        