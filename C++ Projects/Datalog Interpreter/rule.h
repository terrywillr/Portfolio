#ifndef RULE_H
#define RULE_H
#include "predicate.h"
#include <vector>

class Rule
{
public:
	Rule() {}
	~Rule() {}
	void addHead(Predicate pred)
	{
		headPredicate = pred;
	}
	void addPred(Predicate pred)
	{
		predList.push_back(pred);
	}
	void addPred(std::vector<Predicate> preds)
	{
		predList.insert(predList.end(), preds.begin(), preds.end());
	}
	std::string toString()
	{
		std::string output = headPredicate.toString() + " :- ";
		for (size_t i = 0; i < predList.size() - 1; i++)
		{
			output += predList[i].toString() + ",";
		}
		output += predList[predList.size() - 1].toString();

		return output;
	}

	Predicate headPredicate;
	std::vector<Predicate> predList;
};
#endif
