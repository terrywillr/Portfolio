#ifndef SCHEME_H
#define SCHEME_H
#include <string>
#include <vector>
#include "parameter.h"
#include "predicate.h"
class Scheme
{
public:
	Scheme(std::string n) : name(n) {}
	Scheme() {}
	~Scheme() {}
	void setName(std::string n)
	{
		name = n;
	}
	void addParameter(std::string param)
	{
		parameterList.push_back(param);
	}
	void addParameter(std::vector<std::string> params)
	{
		parameterList.insert(parameterList.end(), params.begin(), params.end());
	}

	void editParameter(int pos, std::string val)
	{
		parameterList[pos] = val;
	}

	Predicate toPred()
	{
		Predicate temp(name);
		for (size_t j = 0; j < parameterList.size(); j++)
		{
			Parameter tempParam;
			tempParam.value = parameterList[j];
			tempParam.type = ID;
			temp.addParameter(tempParam);
		}
		return temp;
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
