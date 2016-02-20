#include <SDL.h>
#include <SDL_ttf.h>
#include <string>
#include "QTMovie.h"
#include "Error.h"

using std::string;

class Event
{
public:
//	bool mouseClick;
//	bool mouseMove;
	bool keyPress;
//	bool keyRelease;
	bool quit;

//	bool valid;

//	int x;
//	int y;
//	int button;
	int key;

//	Event() : mouseClick(false), mouseMove(false), keyPress(false), keyRelease(false), quit(false), valid(false) {}
	Event() :  keyPress(false), quit(false) {}
};

class Display
{

protected:
	SDL_Surface* _display;
	Uint32 _color;
	TTF_Font* _font;
public:
	// init system
	Display() throw(SDLError,TTFError);
	virtual ~Display();
	
	int height() { if(_display == 0) return 0; return _display->h; }
	int width() { if(_display == 0) return 0; return _display->w; }

	// create and show display
	void create(const int width, const int height, const bool fs) throw(SDLError);

	// primitives
	void setColor(const float r, const float g, const float b);
	void fillRect(const int x, const int y, const int w, const int h);
	void drawText(const int x, const int y, string text) throw (TTFError,SDLError);
	int getTextWidth(string text) throw (TTFError);

	// refresh display
	void update() throw(SDLError);

	SDL_Surface* surface() { return _display; };

	void blit(SDL_Surface* src, const double opacity) throw(SDLError,RuntimeError);
	void blit(SDL_Surface* src, const int x, const int y, const int w, const int h, const int dx, const int dy, const double opacity) throw(SDLError,RuntimeError);
	void blit(SDL_Surface* src, const int x, const int y, const double opacity) throw(SDLError,RuntimeError);

	bool pollEvents(Event *e);
};
