.PHONY: all test clean 

PYTHON_INC = -I/System/Library/Frameworks/Python.framework/Versions/2.3/include/python2.3
PYTHON_LIB = -framework Python

SDL_INC = `sdl-config --cflags`
SDL_LIB = `sdl-config --libs` /sw/lib/libSDL_ttf.a /usr/X11R6/lib/libfreetype.a

QT_INC = -I/Developer/Headers/FlatCarbon/ -I/System/Library/Frameworks/QuickTime.framework/Versions/A/Headers/
QT_LIB = -framework QuickTime

MIDI_INC = -D__MACOSX_CORE__ -I.
MIDI_LIB = -framework CoreMIDI -framework CoreFoundation -framework CoreAudio

CXXFLAGS = $(PYTHON_INC) $(SDL_INC) $(QT_INC) $(MIDI_INC)
LDFLAGS = $(PYTHON_LIB) $(SDL_LIB) $(QT_LIB) $(MIDI_LIB)

OBJ = example.o example_wrap.o QTMovie.o RtMidi.o

all:
	swig -c++ -python example.i
	$(CXX) $(CXXFLAGS) -c example.cc
	$(CXX) $(CXXFLAGS) -c RtMidi.cpp
	$(CXX) $(CXXFLAGS) -c QTMovie.cc
	$(CXX) $(CXXFLAGS) -c example_wrap.cxx
	$(CXX) -bundle $(LDFLAGS) $(OBJ) -o _example.so

test:
	$(CXX) -o test $(CXXFLAGS) $(LDFLAGS) $(OBJ) main.cc

link:
	python setup.py py2app -A
	ln -s `pwd`/../footage ./dist/pyvid.app/Contents/Resources/

app:
	python setup.py py2app
	mkdir dist/pyvid.app/Contents/Resources/footage/
	cp -av ../footage/examples dist/pyvid.app/Contents/Resources/footage/

clean:
	rm -f _example.so *.o example.py example_wrap* *.pyc test
	rm -rf dist/ build/
