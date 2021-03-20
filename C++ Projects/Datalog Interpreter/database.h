#ifndef DATABASE_H
#define DATABASE_H
#include <map>
#include "relation.h"

class Database
{
public:
	Database() {}
	~Database() {}
	std::map<std::string, Relation> relations;

	std::string toString()
	{
		std::string output;
		for (std::map<std::string, Relation>::iterator it = relations.begin(); it != relations.end(); ++it)
		{
			output += it->second.toString() + "\n";
		}
		return output;
	}
};
#endif
