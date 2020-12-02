#ifndef NODE_H
#define NODE_H
#include <sstream>
#include <string>
using namespace std;
template<typename T>
struct Node
{
	T data;
	Node<T>* left;
	Node<T>* right;
	Node(const T& d) : data(d)
	{
		left = NULL;
		right = NULL;
	}
	virtual ~Node() = default;
	virtual string toString() const
	{
		ostringstream oss;
		oss << data;
		return oss.str();
	}
	friend ostream& operator<<(ostream& out, const Node<T>& node)
	{
		return out << node.toString();
	}
};
#endif
