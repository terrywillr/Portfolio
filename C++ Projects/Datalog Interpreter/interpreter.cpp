#include "interpreter.h"
#include <iostream>
#include "token.h"
#include <algorithm>
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

	processRules();
	//std::cout << "DATABASE\n" << db.toString() << "END DATABASE\n";

	std::cout << std::endl << "Query Evaluation" << std::endl;

	for (size_t i = 0; i < queryList.size(); i++)
	{
		Relation afterSelects;
		Relation afterProjects;

		afterSelects = selects(queryList[i]);

		afterProjects = projectQuery(queryList[i], afterSelects);
		

		std::cout << queryList[i].toString() << "? ";

		if (afterSelects.tupleList.empty())
		{
			std::cout << "No\n";
		}
		else if (afterProjects.tupleList.empty())
		{
			std::cout << "Yes(1)\n";
		}
		else
		{
			std::cout << "Yes(" << afterProjects.tupleList.size() << ")\n";
			for (std::set<Tuple>::iterator it = afterProjects.tupleList.begin(); it != afterProjects.tupleList.end(); ++it)
			{
				std::cout << "  ";
				int count = 0;
				for (size_t x = 0; x < afterProjects.myScheme.parameterList.size(); x++)
				{
					if (count != 0) std::cout << ", ";
					std::cout << afterProjects.myScheme.parameterList[x] << "=" << (*it)[count];
					count++;
				}
				std::cout << std::endl;
			}
		}
	}

	
}

void Interpreter::processRules()
{ 
	int sizeBefore = 0;
	int sizeAfter = 0;
	int numPasses = 0;
	std::cout << "Rule Evaluation" << std::endl;
	std::string output;
	Database copy = db;
	// TODO : Check if tuple needs to get updated and only then add a new tuple. 
	do
	{
		//std::cout << "Database at beginning:" << db.toString() << "End database\n";
		//std::cout << "Iteration number:" << numPasses << std::endl;
		sizeBefore = db.getSize();
		
		for (size_t i = 0; i < rulesList.size(); ++i)
		{
			std::cout << rulesList[i].toString() << ". " << std::endl;
			Predicate headPred = rulesList[i].headPredicate;
			// std::cout << "Head Predicate: " << headPred.toString() << std::endl;
			std::vector<Predicate> predList = rulesList[i].predList;
			Relation afterPreds;

			afterPreds = selects(predList[0]);
			//std::cout << "After selection:" << afterPreds.toString() << std::endl;
			afterPreds = projectQuery(predList[0], afterPreds);
			//std::cout << "After projection:" << afterPreds.toString() << std::endl;

			for (size_t j = 1; j < predList.size(); j++)
			{
				afterPreds = join(afterPreds, projectQuery(predList[j], selects(predList[j])));
				//std::cout << "Join operation: " << afterPreds.toString() << std::endl;
			}
			// std::cout << "After joins: " << afterPreds.toString() << std::endl;

			afterPreds = projectJoin(headPred, afterPreds);
			//std::cout << "After choosing columns:" << afterPreds.toString() << std::endl;
			// std::cout << "After project Join: " << afterPreds.toString() << std::endl;

			// std::cout << "Checking database for extra values:" << db.relations[headPred.name].toString() << std::endl;
			
			
			//std::cout << "Database before adding tuple:" << db.toString() << "End database\n";
			for (std::set<Tuple>::iterator it = afterPreds.tupleList.begin(); it != afterPreds.tupleList.end(); ++it)
			{
				bool truthVal = db.relations[headPred.name].addTuple(*it);
				
				if (truthVal)
				{
					std::cout << "  ";
					int count = 0;
					for (size_t j = 0; j < afterPreds.myScheme.parameterList.size(); j++)
					{
						if (count != 0)
						{
							std::cout << ", ";
						}
						std::cout << db.relations[headPred.name].myScheme.parameterList[j] << "=" << (*it)[count];
						count++;
					}
					std::cout << "\n";
				}
			}
		}
		sizeAfter = db.getSize();

		numPasses++;
		// std::cout << "Finished pass" << std::endl;
	} while (sizeBefore != sizeAfter);
	
	
	std::cout << output;
	
	std::cout << std::endl << "Schemes populated after " << numPasses << " passes through the Rules." << std::endl;
	//std::cout << "Problematic Relation:" << db.relations["DeaWoo"].toString() << std::endl;
}


Relation Interpreter::selects(Predicate query)
{
	Relation newRelation = db.relations[query.name];
	//std::cout << "Selecting Relation: " << newRelation.toString() << std::endl;

	for (size_t j = 0; j < query.parameterList.size(); j++)
	{
		Parameter temp = query.parameterList[j];

		if (temp.type == STRING)
		{
			newRelation = newRelation.select(j, temp.value);
		}
	}

	for (size_t j = 0; j < query.parameterList.size(); j++)
	{
		for (size_t k = j+1; k < query.parameterList.size(); k++)
		{
			if (query.parameterList[j].value == query.parameterList[k].value)
			{
				newRelation = newRelation.select(j, k);
				break;
			}
		}
	}
	return newRelation;
}

Relation Interpreter::projectQuery(Predicate query, Relation rel)
{
	std::vector<int> projectPos;
	std::vector<std::string> renameVals;
	Relation newRelation;

	for (size_t k = 0; k < query.parameterList.size(); k++)
	{
		Parameter temp = query.parameterList[k];
		if (temp.type == ID)
		{
			bool exists = false;
			for (size_t x = 0; x < projectPos.size(); x++)
			{
				if (temp.value == renameVals[x]) exists = true;
			}

			if (!exists)
			{
				projectPos.push_back(k);
				renameVals.push_back(temp.value);
			}
		}
	}

	newRelation = rel.project(projectPos);

	rename(query.name, renameVals, newRelation);

	return newRelation;
}

Relation Interpreter::projectJoin(Predicate query, Relation rel)
{
	std::vector<int> projectPos;
	std::vector<std::string> renameVals;
	Relation newRelation;

	for (size_t k = 0; k < query.parameterList.size(); k++)
	{
		Parameter temp = query.parameterList[k];
		if (temp.type == ID)
		{
			bool exists = false;
			for (size_t x = 0; x < projectPos.size(); x++)
			{
				if (temp.value == renameVals[x])
				{
					exists = true;
				}
			}
			if (!exists)
			{
				for (size_t l = 0; l < rel.myScheme.parameterList.size(); l++)
				{
					if (temp.value == rel.myScheme.parameterList[l])
					{
						projectPos.push_back(l);
						renameVals.push_back(temp.value);
						break;
					}
				}
			}
		}
	}
	newRelation = rel.project(projectPos);

	rename(query.name, renameVals, newRelation);

	return newRelation;
}

void Interpreter::rename(std::string name, std::vector<std::string> param, Relation& renameRel)
{
	Scheme tempScheme(name);
	tempScheme.addParameter(param);
	renameRel.setScheme(tempScheme);
}

Relation Interpreter::join(Relation a, Relation b)
{
	Relation product;
	Predicate joinProj;
	Scheme productScheme = a.myScheme;

	productScheme.addParameter(b.myScheme.parameterList);
	product.setScheme(productScheme);

	for (std::set<Tuple>::iterator it = a.tupleList.begin(); it != a.tupleList.end(); ++it)
	{
		for (std::set<Tuple>::iterator jt = b.tupleList.begin(); jt != b.tupleList.end(); ++jt)
		{
			if (joinable((*it), (*jt), a.myScheme.parameterList, b.myScheme.parameterList))
			{
				Tuple newTuple = (*it);
				newTuple.insert(newTuple.end(), (*jt).begin(), (*jt).end());
				product.addTuple(newTuple);
			}
		}
	}

	std::vector<std::string>::iterator it = std::unique(productScheme.parameterList.begin(), productScheme.parameterList.end());
	productScheme.parameterList.resize(std::distance(productScheme.parameterList.begin(), it));
	joinProj = productScheme.toPred();

	product= projectJoin(joinProj, product);

	return product;
}

bool Interpreter::joinable(Tuple a, Tuple b, std::vector<std::string> aParam, std::vector<std::string> bParam)
{
	for (size_t i = 0; i < a.size(); i++)
	{
		for (size_t j = 0; j < b.size(); j++)
		{
			if (aParam[i] == bParam[j] && a[i] != b[j])
			{
				return false;
			}
		}
	}
	return true;
}