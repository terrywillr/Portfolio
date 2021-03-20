#ifndef PREDICATE_H
#define PREDICATE_H
#include <string>
#include <vector>
#include "parameter.h"
class Predicate
{
public:
	Predicate(std::string n) : name(n) {}
	Predicate() {}
	void addParameter(Parameter param)
	{
		parameterList.push_back(param);
	}
	void addParameter(std::vector<Parameter> params)
	{
		parameterList.insert(parameterList.end(), params.begin(), params.end());
	}

	std::string toString()
	{
		std::string output;
		output = name + "(";
		for (std::size_t i = 0; i < parameterList.size() - 1; i++)
		{
			output += parameterList[i].value + ",";
		}
		output += parameterList[parameterList.size() - 1].value + ")";
		return output;
	}

	std::string name;
	std::vector<Parameter> parameterList;

};
#endif
