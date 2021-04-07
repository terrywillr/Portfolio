#ifndef RELATION_H
#define RELATION_H
#include "tuple.h"
#include <iostream>
#include <set>

class Relation
{
public:
	Relation() {}
	~Relation() {}

	void setScheme(Scheme s);
	bool addTuple(Tuple t);
	std::string toString();
	Relation select(int pos, std::string value);
	Relation select(int pos1, int pos2);
	Relation project(std::vector<int> pos);
	void addTuples(Relation tups);
	int getSize();
	std::set<Tuple> tupleList;
	Scheme myScheme;
};

#endif
