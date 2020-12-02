#include <iostream>
#include <fstream>
#include <sstream>
#include "Maze.h"
using namespace std;

int main(int argc, char* argv[])
{
	
	ifstream in(argv[1]);
	ofstream out(argv[2]);

	string line1, height, width, num_layers;
	getline(in, line1);
	stringstream iss(line1);
	iss >> height >> width >> num_layers;
	Maze myMaze(stoi(height), stoi(width), stoi(num_layers));
	string line2;
	string inMaze;
	while (getline(in, line2))
	{
		if (line2.empty()) continue;
		else
		{
			inMaze += " " + line2;
		}
	}
	stringstream setMaze(inMaze);
	for (int i = 0; i < stoi(num_layers); ++i)
	{
		for (int j = 0; j < stoi(height); ++j)
		{
			for (int k = 0; k < stoi(width); ++k)
			{
				string value;
				setMaze >> value;
				myMaze.setValue(j, k, i, stoi(value));
			}
		}
	}
	out << "Solve Maze:\n" << myMaze;
	if (myMaze.find_maze_path())
	{
		out << endl << "Solution:" << endl << myMaze;
	}
	else
	{
		out << endl << "No Solution Exists!";
	}
	in.close();
	out.close();
	return 0;
}