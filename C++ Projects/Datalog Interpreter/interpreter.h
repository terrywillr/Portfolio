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
	void processRules();
	Relation selects(Predicate query);
	Relation projectQuery(Predicate query, Relation rel);
	Relation projectJoin(Predicate query, Relation rel);
	void rename(std::string name, std::vector<std::string> param, Relation &renameRel);
	Relation join(Relation a, Relation b);
	bool joinable(Tuple a, Tuple b, std::vector<std::string> aParam, std::vector<std::string> bParam);
};

#endif
