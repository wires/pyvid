#ifndef _QTMOVIE_H
#define _QTMOVIE_H

#include <string>
using std::string;

// SDL
#include <SDL.h>

// quicktime
#include <Quicktime.h>

class QTMovie
{
	int _width;
	int _height;

	SDL_Surface* _surface;
//	void *_buffer;
	GWorldPtr _gworld;
	Movie _movie;
	PixMapHandle _pixmap;

	TimeScale _scale;
	TimeValue _duration;

	bool _playing;

	string _filename;
public:
	QTMovie(string filename) ;
	~QTMovie();

	string filename() const { return _filename; }

	bool playing() const { return _playing; }
	int width() const { return _width; }
	int height() const { return _height; }
	double duration() const;

	void decode();

	void unlock(SDL_Surface *surface);
	SDL_Surface* lock();

	void start();
	void stop();

	static void init();
	static void quit();

	static SDL_Surface* createSurface(int, int);
	static void deleteSurface(SDL_Surface*);
};

#endif
