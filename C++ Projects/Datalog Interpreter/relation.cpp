#include "relation.h"
#include "token.h"
#include "parameter.h"

void Relation::setScheme(Scheme s)
{
	myScheme = s;
}

bool Relation::addTuple(Tuple t)
{
	return tupleList.insert(t).second;
}

std::string Relation::toString()
{
	std::string output;
	output = myScheme.toString() + "\n";

	for (std::set<Tuple>::iterator it = tupleList.begin(); it != tupleList.end(); ++it)
	{
		output += (*it).toString() + "\n";
	}
	output += "\n";

	return output;
}


Relation Relation::select(int pos, std::string val)
{
	Relation temp;
	temp.setScheme(myScheme);
	
	for (std::set<Tuple>::iterator it = tupleList.begin(); it != tupleList.end(); ++it)
	{
		if ((*it)[pos] == val)
		{
			//std::cout << "Position and value:" << (*it)[pos] << val << std::endl;
			temp.addTuple(*it);
		}
	}
	return temp;
}

Relation Relation::select(int pos1, int pos2)
{
	Relation temp;
	temp.setScheme(myScheme);

	for (std::set<Tuple>::iterator it = tupleList.begin(); it != tupleList.end(); ++it)
	{
		if ((*it)[pos1] == (*it)[pos2])
		{
			//std::cout << "Position and value:::" << (*it)[pos1] << (*it)[pos2] << std::endl;
			temp.addTuple(*it);
		}
	}
	return temp;
}

Relation Relation::project(std::vector<int> pos)
{
	Relation newRelation;
	newRelation.setScheme(myScheme);
	if (!pos.empty())
	{
		for (std::set<Tuple>::iterator it = tupleList.begin(); it != tupleList.end(); ++it)
		{
			Tuple temp;
			for (size_t i = 0; i < pos.size(); i++)
			{
				temp.push_back((*it)[pos[i]]);
			}
			newRelation.addTuple(temp);
		}
	}
	return newRelation;
}

int Relation::getSize()
{
	return tupleList.size();
}

void Relation::addTuples(Relation tups)
{
	for (std::set<Tuple>::iterator it = tups.tupleList.begin(); it != tups.tupleList.end(); ++it)
	{
		addTuple(*it);
	}
}



