#ifndef LEXER_H
#define LEXER_H
#include <vector>
#include <iostream>
#include <fstream>
#include "token.h"
#include <string>
#include <cctype>
class Lexer {
private:
	std::vector<Token*> tokens;
	std::ifstream inputFile;
	int line = 1;
	char curr;
	char next;
	std::string value = "";
	int start = 0;
public:
	Lexer() { }
	~Lexer() { }
	void read(std::string filename);
	void readToken();
	void readID();
	void readString();
	void readComment();
	void makeToken(tokenType type, int lineNum);
	std::vector<Token*> getTokens();
	void print() const;

};
#endif
