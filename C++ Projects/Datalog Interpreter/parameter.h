#ifndef PARAMETER_H
#define PARAMETER_H
#include <string>
#include "token.h"
class Parameter
{
public:
	Parameter() {}
	~Parameter() {}
	std::string value;
	tokenType type;
};
#endif
