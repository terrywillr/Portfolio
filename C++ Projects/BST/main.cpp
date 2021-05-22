#include <iostream>
#include <fstream>
#include "BST.h"
using namespace std;

int main(int argc, char* argv[])
{
	ifstream in(argv[1]);
	ofstream out(argv[2]);

	BST<int> int_tree;
	BST<string> string_tree;
	bool isInt = true;
	string line;
	while (getline(in, line))
	{
		if (line.empty()) continue;
		string item1, item2;
		istringstream iss(line);
		iss >> item1;
		if (item1 == "INT")
		{
			out << line;
			isInt = true;
			out << " true" << endl;
		}
		if (item1 == "STRING")
		{
			out << line;
			isInt = false;
			out << " true" << endl;
		}
		if (item1 == "add")
		{
			out << line << " ";
			iss >> item2;
			if (isInt)
			{
				out << boolalpha << int_tree.addNode(stoi(item2)) << endl;
			}
			else
			{
				out << boolalpha << string_tree.addNode(item2) << endl;
			}
			
		}
		if (item1 == "remove")
		{
			out << line << " ";
			iss >> item2;
			if (isInt)
			{
				out << boolalpha << int_tree.removeNode(stoi(item2)) << endl;
			}
			else
			{
				out << boolalpha << string_tree.removeNode(item2) << endl;
			}
		}
		if (item1 == "clear")
		{
			if (isInt)
			{
				out << line << " " << boolalpha << int_tree.clearTree() << endl;
			}
			else
			{
				out << line << " " << boolalpha << string_tree.clearTree() << endl;
			}
		}
		if (item1 == "print")
		{
			out << "print:";
			if (isInt)
			{
				out << int_tree << endl;
			}
			else
			{
				out << string_tree << endl;
			}
		}
		if (item1 == "size")
		{
			if (isInt)
			{
				out << line << " " << int_tree.size() << endl;
			}
			else
			{
				out << line << " " << string_tree.size() << endl;
			}
			
		}
		if (item1 == "find")
		{
			out << line << " ";
			iss >> item2;
			if (isInt)
			{
				if (int_tree.findNode(stoi(item2))) out << "found" << endl;
				else out << "not found" << endl;
			}
			else
			{
				if (string_tree.findNode(item2)) out << "found" << endl;
				else out << "not found" << endl;
			}
		}
		if (item1 == "invert")
		{
			out << line << " ";
			if (isInt)
			{
				if (int_tree.invert_tree()) out << "inverted" << endl;
				else out << "tree empty" << endl;
			}
			else
			{
				if (string_tree.invert_tree()) out << "inverted" << endl;
				else out << "tree empty" << endl;
			}
		}
		
	}
	
	return 0;
}