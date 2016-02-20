#include <string>
#include <iostream>
using namespace std;

#include <SDL.h>
#include "QTMovie.h"
#include "Error.h"
#include "example.h"

int main(int argc, char *argv[])
{
	try
	{
		// initialize quicktime
		QTMovie::init();

		// init SDL
		Display display;
		display.create(384,288, false);
		
	/*	// init SDL
		if(SDL_Init(SDL_INIT_VIDEO) < 0)
			throw runtime_error("couldn't init SDL: " + string(SDL_GetError()));

		// options
		Uint32 video_flags = SDL_HWSURFACE | SDL_HWACCEL | SDL_DOUBLEBUF;
		int w = 384;
		int h = 288;
		int desired_bpp = 0;

		// open screen
		SDL_Surface *screen = SDL_SetVideoMode(w, h, desired_bpp, video_flags);
		if(screen == 0)
			throw runtime_error("couldn't set video mode:" + string(SDL_GetError()));
*/
		
		SDL_Surface *screen = display.surface();
		QTMovie movie("footage.mov");

		movie.start();
		bool run = true;
		while(run)
		{
			movie.decode();

			SDL_Surface *const src = movie.lock();
			int i = SDL_SetAlpha(src, SDL_SRCALPHA, 100);
			cerr << i << endl;

//			SDL_UpdateRect(screen, 0, 0, screen->w, screen->h);
			display.blit(src, 1.0);

			display.update();

			/// check incoming SDL events
			SDL_Event event;
			while(SDL_PollEvent(&event))
			{
				switch( event.type )
				{
					// stop if escape/QUIT is pressed twice
					// (quit = close window)
					case SDL_QUIT:
					case SDL_KEYDOWN:
						run = false;
						break;

					default:
						break;
				}
			}
		}
	}

	catch(runtime_error& e)
	{
		cerr << "exception occured" << endl;
		cerr << e.message() << endl;
	}
	catch(...)
	{
		cerr << "unknown exception occured" << endl;
	}

	QTMovie::quit();
	SDL_Quit();
	return 0;
}
