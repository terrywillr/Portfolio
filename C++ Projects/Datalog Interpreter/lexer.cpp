#include "lexer.h"

void Lexer::read(std::string fileName) {
	inputFile.open(fileName);
	// Making sure file opens
	if (inputFile)
	{
		while (inputFile.get(curr))
		{
			readToken();
		}
		makeToken(END, line);

	}
	else {
		std::cout << "Could not read file." << std::endl;
	}
}

void Lexer::readToken()
{
	// Dealing with whitespace. If there is a newline, increment line. If EOF, break.
	while (isspace(curr))
	{
		if (curr == '\n') line++;

		inputFile.get(curr);

		if (inputFile.eof()) break;
	}
	switch (curr)
	{
	case ',':
		value = ",";
		makeToken(COMMA, line);
		break;
	case '.':
		value = ".";
		makeToken(PERIOD, line);
		break;
	case '?':
		value = "?";
		makeToken(Q_MARK, line);
		break;
	case '(':
		value = "(";
		makeToken(LEFT_PAREN, line);
		break;
	case ')':
		value = ")";
		makeToken(RIGHT_PAREN, line);
		break;
	case '*':
		value = "*";
		makeToken(MULTIPLY, line);
		break;
	case '+':
		value = "+";
		makeToken(ADD, line);
		break;
	case ':':
		value = ":";
		//If a colon is read, check if next character is a colon-dash
		next = inputFile.peek();
		if (next == '-')
		{
			value = ":-";
			makeToken(COLON_DASH, line);
			inputFile.get(curr);
		}
		else
			makeToken(COLON, line);
		break;
	// If one-line comment, read the comment
	case '\'':
		readString();
		break;
	// If multi-line comment, read whole comment.
	case '#':
		readComment();
		break;
	default:
		// check for undefined tokens, if not undefined, create ID.
		if (isalpha(curr))
			readID();
		else if (!inputFile.eof())
		{
			value += curr;
			makeToken(UNDEFINED, line);
		}
		break;
	}
}

void Lexer::readID() {
	value += curr;
	inputFile.get(curr);
	// read ID string until no longer alphanumeric
	while (isalnum(curr))
	{
		value += curr;
		inputFile.get(curr);
	}
	// if string matches special strings, create a token for it, else create ID token
	if (value == "Schemes")
	{
		makeToken(SCHEMES, line);
	}
	else if (value == "Facts")
	{
		makeToken(FACTS, line);
	}
	else if (value == "Queries")
	{
		makeToken(QUERIES, line);
	}
	else if (value == "Rules")
	{
		makeToken(RULES, line);
	}
	else
	{
		makeToken(ID, line);
	}
	// continue Lexer
	readToken();
}

void Lexer::readString()
{
	bool endofString = false;
	value += curr;
	start = line;
	while (endofString == false)
	{
		// If EOF reached before end quotation, create UNDEFINED token.
		if (inputFile.peek() == -1)
		{
			makeToken(UNDEFINED, start);
			endofString = true;
		}
		else
		{
			inputFile.get(curr);
			switch (curr)
			{
			case '\n':
				line++;
				value += curr;
				break;
			case '\'':
				value += curr;
				if (inputFile.peek() != '\'')
				{
					makeToken(STRING, start);
					endofString = true;
				}
				else
				{
					inputFile.get(curr);
					value += curr;
				}
				break;
			default:
				value += curr;
				break;
			}
		}
	}
}

void Lexer::readComment()
{
	value += curr;
	start = line;
	if (inputFile.peek() != '|')
	{
		inputFile.get(curr);
		while (curr != '\n')
		{
			value += curr;
			inputFile.get(curr);
		}
		if (curr == '\n') line++;
		makeToken(COMMENT, start);
	}
	else
	{
		inputFile.get(curr);
		value += curr;
		inputFile.get(curr);
		next = inputFile.peek();

		while ((curr != '|' || next != '#') && next != -1)
		{
			if (curr == '\n') line++;
			value += curr;
			inputFile.get(curr);
			next = inputFile.peek();
 		}
		if (curr == '|' && next == '#')
		{
			value += curr;
			inputFile.get(curr);
			value += curr;
			makeToken(COMMENT, start);
		}
		else if (inputFile.eof())
		{
			inputFile.get(curr);
			value += curr;
			line++;
			makeToken(UNDEFINED, start);
		}
	}
}
// Create the token and add it to the tokens vector
void Lexer::makeToken(tokenType type, int line)
{
	Token* token = new Token(value, type, line);
	tokens.push_back(token);
	value = "";
}
// Print out all tokens, and token count
void Lexer::print() const 
{
	for (size_t i = 0; i < tokens.size(); i++) 
	{
		std::cout << tokens.at(i)->toString() << std::endl;
	}
	std::cout << "Total Tokens = " << tokens.size() << std::endl;
}

// Deletes comments picked up by Lexer.
std::vector<Token*> Lexer::getTokens()
{
	std::vector<Token*> newTokens;
	for (size_t i = 0; i < tokens.size(); ++i)
	{
		if (tokens[i]->getType() != COMMENT)
		{
			newTokens.push_back(tokens[i]);
		}
	}
	return newTokens;
}