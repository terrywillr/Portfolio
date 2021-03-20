#ifndef DATALOGPROGRAM_H
#define DATALORPROGRAM_H
#include <vector>
#include "scheme.h"
#include "rule.h"
class datalogProgram
{
public:
	datalogProgram() {}
	~datalogProgram() {}
	void addScheme(Scheme s);
	void addFact(Scheme f);
	void addRule(Rule s);
	void addQuery(Predicate p);
	void makeDomain();
	std::string toString();

	std::vector<Scheme> schemesList;
	std::vector<Scheme> factsList;
	std::vector<std::string> domain;
	std::vector<Rule> rulesList;
	std::vector<Predicate> queryList;
	std::string intToString(int);
};
#endif