#ifndef PARSER_H
#define PARSER_H
#include "lexer.h"
#include "scheme.h"
#include "datalogProgram.h"
class Parser
{
public:
	Parser(std::string inputFile)
	{
		lexer.read(inputFile);
		tokenList = lexer.getTokens();
		token = tokenList[0];
		tokenList.erase(tokenList.begin());
	}
	Parser() {}
	~Parser() {}
	Token* token;
	void parse();
	void parse(std::string input);
	Token getToken();
	void match(tokenType t);
	void error();
	void toString();
	void parseScheme();
	void parseSchemeList();
	void parseFactList();
	void parseFact();
	void parseRuleList();
	void parseRule();
	Predicate headPredicate();
	Predicate parsePredicate();
	std::vector<Predicate> parsePredicateList();
	Parameter parseParameter();
	std::vector<Parameter> parseParameterList();
	std::string parseExpression();
	std::string parseOperator();
	void parseQuery();
	void parseQueryList();
	std::vector<std::string> idList();
	std::vector<std::string> stringList();

	std::vector<Scheme> schemesList;
	std::vector<Scheme> factsList;
	std::vector<std::string> domain;
	std::vector<Rule> rulesList;
	std::vector<Predicate> queryList;

private:
	std::vector<Token*> tokenList;
	datalogProgram program;
	Lexer lexer;
};
#endif
