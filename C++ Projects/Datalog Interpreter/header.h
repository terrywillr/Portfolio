#ifndef HEADER_H
#define HEADER_H
#include "predicate.h"
class Header
{
public:
	Header() {}
	~Header() {}

	void addAttribute(std::string a)
	{
		attributes.push_back(a);
	}

	std::vector<std::string> getAttributes() const
	{
		return attributes;
	}
private:
	std::vector<std::string> attributes;
};

#endif