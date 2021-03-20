#include <iostream>
#include "interpreter.h"

int main(int argc, char* argv[])
{
	Interpreter interpreter;
	interpreter.start(argv[1]);

	return 0;
}