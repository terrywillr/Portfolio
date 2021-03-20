#include "parser.h"
#include "rule.h"
#include "parameter.h"
#include <algorithm>
#include <iostream>

void Parser::parse()
{
	match(SCHEMES);
	match(COLON);
	parseScheme();
	parseSchemeList();

	match(FACTS);
	match(COLON);
	parseFactList();
	program.makeDomain();

	match(RULES);
	match(COLON);
	parseRuleList();

	match(QUERIES);
	match(COLON);
	parseQuery();
	parseQueryList();

	
}

void Parser::parse(std::string input)
{
	lexer.read(input);
	tokenList = lexer.getTokens();
	token = tokenList[0];
	tokenList.erase(tokenList.begin());

	match(SCHEMES);
	match(COLON);
	parseScheme();
	parseSchemeList();

	match(FACTS);
	match(COLON);
	parseFactList();
	program.makeDomain();

	match(RULES);
	match(COLON);
	parseRuleList();

	match(QUERIES);
	match(COLON);
	parseQuery();
	parseQueryList();

	schemesList = program.schemesList;
	factsList = program.factsList;
	domain = program.domain;
	rulesList = program.rulesList;
	queryList = program.queryList;


}

void Parser::match(tokenType t)
{
	
	if (token->getType() == t)
	{
		token = tokenList[0];
		tokenList.erase(tokenList.begin());
	}
	else
	{
		error();
	}
}

void Parser::error()
{
	std::cout << "Failure!" << std::endl << token->toString() << std::endl;
	exit(EXIT_SUCCESS);
}

void Parser::parseScheme()
{
	Scheme newScheme(token->getName());
	match(ID);
	match(LEFT_PAREN);
	newScheme.addParameter(token->getName());
	match(ID);
	newScheme.addParameter(idList());
	match(RIGHT_PAREN);

	program.addScheme(newScheme);
}

void Parser::parseSchemeList()
{
	if (token->getType() != FACTS)
	{
		parseScheme();
		parseSchemeList();
	}
}

void Parser::parseFact()
{
	Scheme newFact(token->getName());
	match(ID);
	match(LEFT_PAREN);
	newFact.addParameter(token->getName());
	match(STRING);
	newFact.addParameter(stringList());
	match(RIGHT_PAREN);
	match(PERIOD);

	program.addFact(newFact);
}

void Parser::parseFactList()
{
	if (token->getType() != RULES)
	{
		parseFact();
		parseFactList();
	}
}
void Parser::parseRuleList()
{
	if (token->getType() != QUERIES)
	{
		parseRule();
		parseRuleList();
	}
}

void Parser::parseRule()
{
	Rule newRule;
	newRule.addHead(headPredicate());
	match(COLON_DASH);
	newRule.addPred(parsePredicate());
	newRule.addPred(parsePredicateList());
	match(PERIOD);

	program.addRule(newRule);

}

Predicate Parser::headPredicate()
{
	Predicate newHead(token->getName());
	Parameter initial;
	std::vector<Parameter> pList;
	std::vector<std::string> temp;
	match(ID);
	match(LEFT_PAREN);
	initial.value = token->getName();
	initial.type = ID;
	newHead.addParameter(initial);
	match(ID);
	temp = idList();
	for (size_t i = 0; i < temp.size(); i++)
	{
		Parameter a;
		a.value = temp[i];
		a.type = ID;
		pList.push_back(a);
	}
	newHead.addParameter(pList);
	match(RIGHT_PAREN);

	return newHead;
}

Predicate Parser::parsePredicate()
{
	Predicate newPred(token->getName());
	match(ID);
	match(LEFT_PAREN);
	newPred.addParameter(parseParameter());
	newPred.addParameter(parseParameterList());
	match(RIGHT_PAREN);

	return newPred;
}

std::vector<Predicate> Parser::parsePredicateList()
{
	std::vector<Predicate> newPredList;
	if (token->getType() != PERIOD && token->getType() != QUERIES)
	{
		match(COMMA);
		newPredList.push_back(parsePredicate());
		std::vector<Predicate> temp = parsePredicateList();
		newPredList.insert(newPredList.end(), temp.begin(), temp.end());
	}
	return newPredList;
}

Parameter Parser::parseParameter()
{
	Parameter newParam;
	if (token->getType() == STRING)
	{
		newParam.value = token->getName();
		newParam.type = STRING;
		match(STRING);
	}
	else if (token->getType() == ID)
	{
		newParam.value = token->getName();
		newParam.type = ID;
		match(ID);
	}
	else
	{
		newParam.value = parseExpression();
		newParam.type = ID;
	}
	return newParam;
}

std::vector<Parameter> Parser::parseParameterList()
{
	std::vector<Parameter> newParamList;
	if (token->getType() != RIGHT_PAREN)
	{
		match(COMMA);
		newParamList.push_back(parseParameter());
		std::vector<Parameter> temp = parseParameterList();
		newParamList.insert(newParamList.end(), temp.begin(), temp.end());
	}
	return newParamList;
}

std::string Parser::parseExpression()
{
	std::string exp = "(";
	match(LEFT_PAREN);
	exp += parseParameter().value + " ";
	exp += parseOperator() + " ";
	exp += parseParameter().value;
	match(RIGHT_PAREN);
	exp += ")";

	return exp;
}

std::string Parser::parseOperator()
{
	if (token->getType() == ADD)
	{
		match(ADD);
		return "+";
	}
	else if (token->getType() == MULTIPLY)
	{
		match(MULTIPLY);
		return "*";
	}
	else
	{
		error();
		return "";
	}
}

void Parser::parseQuery()
{
	program.addQuery(parsePredicate());
	match(Q_MARK);
}

void Parser::parseQueryList()
{
	if (token->getType() != END)
	{
		parseQuery();
		parseQueryList();
	}
}

std::vector<std::string> Parser::idList()
{
	std::vector<std::string> myList;

	if (token->getType() != RIGHT_PAREN)
	{
		match(COMMA);
		myList.push_back(token->getName());
		match(ID);
		std::vector<std::string> temp = idList();
		myList.insert(myList.end(), temp.begin(), temp.end());
	}
	return myList;
}

std::vector<std::string> Parser::stringList()
{
	std::vector<std::string> myList;

	if (token->getType() != RIGHT_PAREN)
	{
		match(COMMA);
		myList.push_back(token->getName());
		match(STRING);
		std::vector<std::string> temp = stringList();
		myList.insert(myList.end(), temp.begin(), temp.end());
	}
	return myList;
}