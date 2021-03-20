#include "token.h"
#include <sstream>

std::string Token::lines()
{
	std::stringstream convert;
	convert << line;
	std::string lineNum = convert.str();
	return lineNum;
}
std::string Token::toString()
{
	std::string output;
	output = "(" + enumToString(item) + ",\"" + name + "\"," + lines() + ")";
	return output;
}

std::string Token::enumToString(tokenType token) {
	std::string outString;
	switch (token) {
	case COMMA:
		outString = "COMMA";
		break;
	case PERIOD:
		outString = "PERIOD";
		break;
	case Q_MARK:
		outString = "Q_MARK";
		break;
	case LEFT_PAREN:
		outString = "LEFT_PAREN";
		break;
	case RIGHT_PAREN:
		outString = "RIGHT_PAREN";
		break;
	case COLON:
		outString = "COLON";
		break;
	case COLON_DASH:
		outString = "COLON_DASH";
		break;
	case MULTIPLY:
		outString = "MULTIPLY";
		break;
	case ADD:
		outString = "ADD";
		break;
	case SCHEMES:
		outString = "SCHEMES";
		break;
	case FACTS:
		outString = "FACTS";
		break;
	case RULES:
		outString = "RULES";
		break;
	case QUERIES:
		outString = "QUERIES";
		break;
	case ID:
		outString = "ID";
		break;
	case STRING:
		outString = "STRING";
		break;
	case COMMENT:
		outString = "COMMENT";
		break;
	case WHITESPACE:
		outString = "WHITESPACE";
		break;
	case UNDEFINED:
		outString = "UNDEFINED";
		break;
	case END:
		outString = "EOF";
		break;
	}
	return outString;
}

tokenType Token::getType()
{
	return item;
}
std::string Token::getName()
{
	return name;
}