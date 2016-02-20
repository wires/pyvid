#ifndef ERROR_H
#define ERROR_H

#include <string>
#include <sstream>
using namespace std;


// SDL
#include <SDL.h>
#include <SDL_ttf.h>

// quicktime
#include <Quicktime.h>

// portmidi
//#include <portmidi.h>


//#include <stdexcept>
class RuntimeError
{
protected:
	string _msg;
public:
	RuntimeError(string msg)
	{
		_msg = msg;
	}

	string message()
	{
		return _msg.c_str();
	}
};

class SDLError : public RuntimeError
{
	public:
		SDLError(string message) : RuntimeError(message + ": " + string(SDL_GetError()))
			{ };
};

class TTFError : public RuntimeError
{
	public:
		TTFError(string message) : RuntimeError(message + ": " + string(TTF_GetError()))
			{ };
};

static string itos(int i)
{
		ostringstream s;
		s << i;
		return s.str();
}

class QTError : public RuntimeError
{
	public:
		QTError(string message) : RuntimeError(message + ": error code (" + itos(GetMoviesError()) + ")")
		{ };
};

/*
class ParseError : public RuntimeError
{
	public:
		ParseError(string message, string file, int line) : RuntimeError("parse error in " + file + ":" + itos(line) + ": " + message)
		{ };
};

class PortMIDIError : public RuntimeError
{
	public:
		PortMIDIError(string message, PmError err) :
			RuntimeError(message + ": " + string(Pm_GetErrorText(err)))
		{ };
};*/

#endif
