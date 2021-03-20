#ifndef TOKEN_H
#define TOKEN_H
#include <string>
enum tokenType {COMMA, PERIOD, Q_MARK, LEFT_PAREN, RIGHT_PAREN, COLON, COLON_DASH, MULTIPLY, ADD,
	SCHEMES, FACTS, RULES, QUERIES, ID, STRING, COMMENT, WHITESPACE, UNDEFINED, END};
class Token {
private:
	std::string name;
	tokenType item;
	int line;

public:
	Token(std::string n, tokenType i, int l) : name(n), item(i), line(l) { }
	~Token() { }

	std::string toString();
	std::string lines();
	std::string enumToString(tokenType token);
	tokenType getType();
	std::string getName();


};
#endif
