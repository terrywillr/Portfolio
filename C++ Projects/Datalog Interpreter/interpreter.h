#ifndef INTERPRETER_H
#define INTERPRETER_H

#include "parser.h"
#include "database.h"
#include <vector>

class Interpreter
{
public:
	Interpreter() {}
	~Interpreter() {}

	void start(std::string intputFile);

	std::vector<Scheme> schemesList;
	std::vector<Scheme> factsList;
	std::vector<std::string> domain;
	std::vector<Rule> rulesList;
	std::vector<Predicate> queryList;
private:
	std::string input;
	Parser myParser;
	Database db;
};

#endif
