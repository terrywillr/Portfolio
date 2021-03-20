#include "datalogProgram.h"
#include <sstream>
#include <algorithm>

void datalogProgram::addScheme(Scheme s)
{
	schemesList.push_back(s);
}

void datalogProgram::addFact(Scheme f)
{
	factsList.push_back(f);
	domain.insert(domain.end(), f.parameterList.begin(), f.parameterList.end());
}

void datalogProgram::addRule(Rule r)
{
	rulesList.push_back(r);
}

void datalogProgram::addQuery(Predicate p)
{
	queryList.push_back(p);
}

void datalogProgram::makeDomain()
{
	std::sort(domain.begin(), domain.end());
	domain.erase(std::unique(domain.begin(), domain.end()), domain.end());
}

std::string datalogProgram::toString()
{
	std::string output;
	output = "Schemes(" + intToString(schemesList.size()) + "):\n";
	for (size_t i = 0; i < schemesList.size(); i++)
	{
		output += "  " + schemesList[i].toString() + "\n";
	}
	output += "Facts(" + intToString(factsList.size()) + "):\n";
	for (size_t i = 0; i < factsList.size(); i++)
	{
		output += "  " + factsList[i].toString() + ".\n";
	}
	output += "Rules(" + intToString(rulesList.size()) + "):\n";
	for (size_t i = 0; i < rulesList.size(); i++)
	{
		output += "  " + rulesList[i].toString() + ".\n";
	}
	output += "Queries(" + intToString(queryList.size()) + "):\n";
	for (size_t i = 0; i < queryList.size(); i++)
	{
		output += "  " + queryList[i].toString() + "?\n";
	}
	output += "Domain(" + intToString(domain.size()) + "):\n";
	for (size_t i = 0; i < domain.size(); i++)
	{
		output += "  " + domain[i] + "\n";
	}
	return output;
}

std::string datalogProgram::intToString(int x)
{
	std::stringstream out;
	out << x;
	return out.str();
}