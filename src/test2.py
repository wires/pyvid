import random
import time
import path

import macosx

from example import *
from model import *
from gui import *
from keymap import *

QTMovie.init()

gc = Display()
gc.create(1024,768,False)

t = time.time()
frames = 0
        
while(1):
	    # draw FPS counter
        frames += 1
        fps = frames/(time.time() - t)
        gc.setColor(0.0,0.0,0.0)
        gc.fillRect(0, 0, 100, 10)
        gc.drawText(0, 0, "fps: %s" % str(int(fps)))
        
        
        # flip screen
        gc.update()

        # reset counter every 2.5 seconds
        if(frames > 1000):
            frames = 0
            t = time.time()