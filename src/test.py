import random
import time
import path

import macosx

from example import *
from model import *
from gui import *
from keymap import *

QTMovie.init()

display = Display()
display.create(1024,768,False)

t = time.time()
frames = 0

while(1):

	frames += 1
	fps = frames / (time.time() - t)
	display.setColor(0.0,0.0,0.0)
	display.fillRect(0, 0, 100, 10)
	display.drawText(0,0, "Fps: %2.2f" % fps)

	display.update()

	if(frames > 1000):
		frames = 0
		t = time.time()
