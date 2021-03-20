#include "interpreter.h"
#include <iostream>
#include "token.h"

void Interpreter::start(std::string inputFile)
{
	myParser.parse(inputFile);
	schemesList = myParser.schemesList;
	factsList = myParser.factsList;
	domain = myParser.domain;
	rulesList = myParser.rulesList;
	queryList = myParser.queryList;


	for (size_t i = 0; i < schemesList.size(); i++)
	{
		Relation newRelation;
		newRelation.setScheme(schemesList[i]);
		db.relations.insert(std::pair<std::string, Relation>(schemesList[i].name, newRelation));
	}

	for (size_t i = 0; i < factsList.size(); i++)
	{
		Tuple newTuple(factsList[i]);
		db.relations[factsList[i].name].addTuple(newTuple);
	}

	for (size_t i = 0; i < queryList.size(); i++)
	{
		Relation selects = db.relations[queryList[i].name];
		Relation projects;
		std::vector<int> projectsPos;
		std::vector<std::string> renameVals;


		for (size_t j = 0; j < queryList[i].parameterList.size(); j++)
		{
			Parameter temp = queryList[i].parameterList[j];
			if (temp.type == STRING) selects = selects.select(j + 1, temp.value);
			for (size_t k = j+1; k < queryList[i].parameterList.size(); k++)
			{
				if (queryList[i].parameterList[j].value == queryList[i].parameterList[k].value)
				{
					selects = selects.select(j, k);
					break;
				}
			}
		}

		for (size_t k = 0; k < queryList[i].parameterList.size(); k++)
		{
			Parameter temp = queryList[i].parameterList[k];
			if (temp.type == ID)
			{
				bool exists = false;
				for (size_t x = 0; x < projectsPos.size(); x++)
				{
					if (temp.value == renameVals[x]) exists = true;
				}
				if (!exists)
				{
					projectsPos.push_back(k);
					renameVals.push_back(temp.value);
				}
			}
		}

		projects = selects.project(projectsPos);


		Scheme tempScheme(queryList[i].name);
		tempScheme.addParameter(renameVals);
		projects.setScheme(tempScheme);

		std::cout << queryList[i].toString() << "? ";
		if ((selects.tupleList).empty())
		{
			std::cout << "No" << std::endl;
		}
		else if ((projects.tupleList).empty())
		{
			std::cout << "Yes(1)" << std::endl;
		}
		else
		{
			std::cout << "Yes(" << projects.tupleList.size() << ")" << std::endl;
			for (std::set<Tuple>::iterator it = projects.tupleList.begin(); it != projects.tupleList.end(); ++it)
			{
				std::cout << "  ";
				int count = 0;
				for (size_t x = 0; x < projects.myScheme.parameterList.size(); x++)
				{
					if (count != 0)
					{
						std::cout << ", ";
					}
					std::cout << projects.myScheme.parameterList[x] << "=" << (*it)[count];
					count++;
				}
				std::cout << std::endl;
			}
		}
	}
}
