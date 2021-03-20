#ifndef SCHEME_H
#define SCHEME_H
#include <string>
#include <vector>
#include "parameter.h"
class Scheme
{
public:
	Scheme(std::string n) : name(n) {}
	Scheme() {}
	~Scheme() {}
	void addParameter(std::string param)
	{
		parameterList.push_back(param);
	}
	void addParameter(std::vector<std::string> params)
	{
		parameterList.insert(parameterList.end(), params.begin(), params.end());
	}

	void setName(std::string n)
	{
		name = n;
	}
	std::string toString()
	{
		std::string output;
		output = name + "(";
		for (std::size_t i = 0; i < parameterList.size() - 1; i++)
		{
			output += parameterList[i] + ",";
		}
		output += parameterList[parameterList.size() - 1]+ ")";
		return output;
	}
	std::string name;
	std::vector<std::string> parameterList;
};
#endif
