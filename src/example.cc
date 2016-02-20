#include "example.h"

Display::Display() throw(SDLError,TTFError)
{
	// init quicktime
	// ...

	// init SDL
	if(SDL_Init(SDL_INIT_VIDEO) < 0)
		throw SDLError("couldn't init SDL: ");

	// int SDL_ttf
	if(TTF_Init() == -1)
		throw TTFError("couldn't init TTF");

	_font = TTF_OpenFont("font.ttf", 6);
	if(!_font)
		throw TTFError("couldn't load font 'font.ttf'");

	SDL_EventState(SDL_MOUSEBUTTONDOWN, SDL_ENABLE);
	SDL_EventState(SDL_MOUSEBUTTONUP, SDL_ENABLE);
}

Display::~Display()
{
	TTF_CloseFont(_font);
	TTF_Quit();
	SDL_Quit();
}

void Display::create(const int w, const int h, const bool fs) throw(SDLError)
{
	Uint32 video_flags = SDL_HWSURFACE | SDL_HWACCEL | SDL_DOUBLEBUF;

	if(fs)
		video_flags = SDL_FULLSCREEN|SDL_SWSURFACE;

	_display = SDL_SetVideoMode(w, h, 0, video_flags);
	if(_display== 0)
		throw SDLError("couldn't init display");

	// hide mouse
	SDL_ShowCursor(SDL_DISABLE);
}

void Display::setColor(const float fr, const float fg, const float fb)
{
	const Uint8 r = (int)(fr * 255);
	const Uint8 g = (int)(fg * 255);
	const Uint8 b = (int)(fb * 255);
	_color = SDL_MapRGB(_display->format, r, g, b);
}

void Display::fillRect(const int x, const int y, const int w, const int h)
{
	SDL_Rect rect;
	rect.x = x;
	rect.y = y;
	rect.w = w;
	rect.h = h;
	SDL_FillRect(_display, &rect, _color);
}

void Display::update() throw(SDLError)
{
	//SDL_UpdateRect(_display, 0, 0, _display->w, _display->h);
	SDL_Flip(_display);
	//	throw SDLError("couldn't flip display surface");
}


void Display::drawText(const int x, const int y, string text) throw(TTFError,SDLError)
{
	SDL_Color color= {255,255,255};
	SDL_Surface *text_surface =TTF_RenderText_Solid(_font, text.c_str(), color);

	if(!text_surface)
		throw TTFError("Failed to render text to surface");

	SDL_Rect drect;
	drect.x = x;
	drect.y = y;
	drect.w = text_surface->w;
	drect.h = text_surface->h;

	SDL_Rect srect;
	srect.x = 0;
	srect.y = 0;
	srect.w = text_surface->w;
	srect.h = text_surface->h;

	if(SDL_BlitSurface(text_surface,&srect,_display,&drect) < 0)
		throw SDLError("failed to blit text to display surface");

	SDL_FreeSurface(text_surface);
}

int Display::getTextWidth(string text) throw (TTFError)
{
	int w, h;
	if(TTF_SizeText(_font, text.c_str(), &w, &h))
		throw TTFError("Couldn't get font width");
	return w;
}

#include <iostream>
using namespace std;

void Display::blit(SDL_Surface *src, const double opacity) throw(RuntimeError,SDLError)
{
	if(src == 0)
		throw RuntimeError("Surface argument is null");

	if(SDL_SetAlpha(src, SDL_SRCALPHA, (int)(opacity*255)) < 0)
		throw SDLError("Couldn't set surface alpha");


	if(SDL_BlitSurface(src, 0, _display, 0) < 0)
		throw SDLError("Coudln't blit surface");
}

void Display::blit(SDL_Surface *src, const int x, const int y, const double opacity) throw(RuntimeError,SDLError)
{
	if(src == 0)
		throw RuntimeError("Surface argument is null");

	if(SDL_SetAlpha(src, SDL_SRCALPHA, (int)(opacity*255)) < 0)
		throw SDLError("Couldn't set surface alpha");

	SDL_Rect drect;
	drect.x = x;
	drect.y = y;
	drect.w = src->w;
	drect.h = src->h;

	if(SDL_BlitSurface(src, 0, _display, &drect) < 0)
		throw SDLError("Coudln't blit surface");
}

void Display::blit(SDL_Surface *src, const int x, const int y, const int w, const int h, const int dx, const int dy, const double opacity) throw(RuntimeError,SDLError)
{
	if(src == 0)
		throw RuntimeError("Surface argument is null");

	if(SDL_SetAlpha(src, SDL_SRCALPHA, (int)(opacity*255)) < 0)
		throw SDLError("Couldn't set surface alpha");

	SDL_Rect rect;
	rect.x = x;
	rect.y = y;
	rect.w = w;
	rect.h = h;

	SDL_Rect drect;
	drect.x = dx;
	drect.y = dy;
	drect.w = w;
	drect.h = h;

	if(SDL_BlitSurface(src, &rect, _display, &drect) < 0)
		throw SDLError("Coudln't blit surface");
}

bool Display::pollEvents(Event* e)
{
	SDL_Event event;

	if(SDL_PollEvent(&event) == 0)
		return false;

	//int x, y;

	switch(event.type)
	{
		case SDL_KEYDOWN:
			e->keyPress = true;
			e->key = event.key.keysym.sym;
			break;

		case SDL_QUIT:
			e->quit = true;
			break;

/*			case SDL_KEYUP:
			e->keyRelease = false;
			e->key = event.key.keysym.sym;
			break;

		case SDL_MOUSEMOTION:
			e->mouseMove = true;
			e->x = event.motion.x;
			e->y = event.motion.y;
			break;

		case SDL_MOUSEBUTTONUP:
		case SDL_MOUSEBUTTONDOWN:
			e.mouseClick = true;
			e.button = event.button.button;
			SDL_GetMouseState(&x, &y);
			e.x = x;
			e.y = y;
			break;
*/
	}
	return true;
}
