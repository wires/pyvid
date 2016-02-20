%module example
%{
#include "Error.h"
#include "example.h"
#include "QTMovie.h"
#include "RtMidi.h"
%}

// handle basic strings
%include "std_string.i"

// use vectors
%include "std_vector.i"
namespace std {
	%template(msgVector) vector<unsigned char>;
}

// handle exceptions
%include "exception.i"
%exception {
	try {
		$action
	}
	catch(RuntimeError& e) {
		SWIG_exception(SWIG_RuntimeError, e.message().c_str());
	} catch(...) {
		SWIG_exception(SWIG_RuntimeError, "unknown error");
	}
}

%include "Error.h"
%include "example.h"
%include "QTMovie.h"
%include "RtMidi.h"
