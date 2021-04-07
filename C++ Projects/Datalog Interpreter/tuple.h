#ifndef TUPLE_H
#define TUPLE_H
#include <string>
#include "scheme.h"
class Tuple : public std::vector<std::string>
{
public:
	Tuple(Scheme s)
	{
		//push_back(s.name);
		for (size_t i = 0; i < s.parameterList.size(); i++)
		{
			push_back(s.parameterList[i]);
		}
	}
	Tuple() {}
	~Tuple() {}

	std::string toString() const
	{
		std::string output;
		for (std::vector<std::string>::const_iterator it = this->begin(); it != this->end(); ++it)
		{
			output += *it + "  ";
		}
		return output;
	}
};
#endif
