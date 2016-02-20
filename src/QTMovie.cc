#include "QTMovie.h"
#include "Error.h"

void QTMovie::init()
{
#ifdef _WIN32
	// initialize quicktime media layer
	if ( InitializeQTML( 0L ) )
		throw RuntimeError( "Quicktime 3.0 not available" );
#endif

	// alocate space for quicktime's internal data
	if ( EnterMovies() )
		throw QTError( "Quicktime 3.0 not available" );
};

void QTMovie::quit()
{
	// clean up
	ExitMovies();
#ifdef _WIN32
	TerminateQTML();
#endif
};

QTMovie::QTMovie(string filename) : _filename(filename), _gworld(0), _movie(0), _playing(false)
{
	short refnum;
	short resid;

	FSSpec fsspec;
#ifdef _WIN32
	NativePathNameToFSSpec( (char*)filename.c_str(), &fsspec, 0L);
#else
	FSRef fsref;
	FSPathMakeRef((const UInt8*)filename.c_str(), &fsref, NULL);
	FSGetCatalogInfo(&fsref, kFSCatInfoNone, NULL, NULL, &fsspec, NULL);
#endif

	// open file (read only)
	if(OpenMovieFile(&fsspec, &refnum, fsRdPerm))
		throw QTError("Can't open file '" + filename + "'");

	// create movie
	// newMovieActive
	if(NewMovieFromFile(&_movie, refnum, &resid, NULL, 0, NULL))
	{
		if(_movie)
			DisposeMovie(_movie);
		throw QTError("Couldn't read from file " + filename);
	}
	MoviesTask(_movie, 0);

	// close file
	if(refnum)
		CloseMovieFile(refnum);

	// reposition movie box
	Rect rect;
	GetMovieBox(_movie, &rect); 

	// store movie dimensions
	_width = rect.right - rect.left;
	_height = rect.bottom - rect.top;

	// wrap buffer in GWorld
	rect.left = rect.top = 0;
	rect.right = _width;
	rect.bottom = _height;

	// allocate buffer
	_surface = QTMovie::createSurface(_width, _height);

	SDL_LockSurface(_surface);
	if(QTNewGWorldFromPtr(&_gworld, k24RGBPixelFormat, &rect, NULL, NULL, 0,
				(char*)_surface->pixels, _surface->pitch) != noErr)
		throw QTError("Couldn't wrap SDLSurface in GWorld");

	SetMovieGWorld(_movie, _gworld, GetGWorldDevice(_gworld));
	if(GetMoviesError() != noErr)
		throw QTError("Failed so assign GWorld to Movie");
	MoviesTask(_movie, 0);

	SetMovieActive(_movie, true);
	if(GetMoviesError() != noErr)
		throw QTError("Failed to set movie active");
	MoviesTask(_movie, 0);

	SDL_UnlockSurface(_surface);

	// get movie duration (in seconds = (double)_duration / (double)_scale);
	_duration = GetMovieDuration(_movie);
	_scale = GetMovieTimeScale(_movie);
}

double QTMovie::duration() const
{
	// movie duration in seconds is _duration / _scale
	// as _scale is (duration_units/second)
	return (double)_duration / (double)_scale;
}

void QTMovie::start()
{
	_playing = true;
	StartMovie(_movie);
	MoviesTask(_movie, 0);
}

void QTMovie::stop()
{
	_playing = false;
	StopMovie(_movie);
	MoviesTask(_movie, 0);
}

#include <iostream>
using namespace std;

void QTMovie::decode()
{
	// wrap time around
//	TimeValue v = ((int)(t * (double)_scale)) % _duration;
	//cout << v << endl;

	SDL_LockSurface(_surface);

	// loop if needed
	TimeValue v = GetMovieTime(_movie, 0);
	if(v == _duration)
	{
		GoToBeginningOfMovie(_movie);
		MoviesTask(_movie, 0);
	}

	// set movie time
//	SetMovieTimeValue(_movie, v);
//	MoviesTask(_movie, 0);

	UpdateMovie(_movie);
	if(GetMoviesError() != noErr)
		throw QTError("update movie failed");

	MoviesTask(_movie, 0);
	if(GetMoviesError() != noErr)
		throw QTError("moviestask failed");

	SDL_UnlockSurface(_surface);
};

QTMovie::~QTMovie()
{
	if(_movie)
		DisposeMovie(_movie);

	QTMovie::deleteSurface(_surface);
	//free(_buffer);
}

void QTMovie::deleteSurface(SDL_Surface* surface)
{
	SDL_FreeSurface(surface);
}

SDL_Surface* QTMovie::createSurface(int w, int h)
{
    // Create a 32-bit surface with the bytes of each pixel in R,G,B,A order,
    // as expected by OpenGL for textures. SDL interprets each pixel as a
    // 32-bit number, so our masks must depend on the endianness (byte order)
    // of the machine

#if SDL_BYTEORDER == SDL_BIG_ENDIAN
	const Uint32 r = 0xff0000;
	const Uint32 g = 0x00ff00;
	const Uint32 b = 0x0000ff;
	const Uint32 a = 0x000000;
#else
	const Uint32 r = 0x0000ff;
	const Uint32 g = 0x00ff00;
	const Uint32 b = 0xff0000;
	const Uint32 a = 0x000000;
#endif

	const int flags = SDL_SRCALPHA; //| SDL_HWSURFACE;

	SDL_Surface *surface = SDL_CreateRGBSurface(flags,
			w, h, 24, r, g, b, a);

	if(! surface)
		throw SDLError("failed to create " + itos(w) + "x" + itos(h) +
				"x24 surface");

	return surface;
}

SDL_Surface* QTMovie::lock()
{
	return _surface;
}

void QTMovie::unlock(SDL_Surface *surface)
{
}
