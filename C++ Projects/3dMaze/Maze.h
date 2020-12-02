#ifndef MAZE_H
#define MAZE_H
#include "MazeInterface.h"
using namespace std;
#define L	maze_, r, c - 1, l
#define R	maze_, r, c + 1, l
#define U	maze_, r - 1, c, l
#define D	maze_, r + 1, c, l
#define O	maze_, r, c, l - 1
#define I	maze_, r, c, l + 1


class Maze : public MazeInterface
{
private:
	enum CellValue_t{ OPEN, BLOCKED, VISITED, EXIT, LEFT, RIGHT ,UP, DOWN, OUT, IN, PATH };
	int height;
	int width;
	int layers;
	int*** maze_;
public:
	Maze(int h, int w, int l) : height(h), width(w), layers(l)
	{
		maze_ = new int** [height];
		for (int i = 0; i < height; ++i)
		{
			maze_[i] = new int* [width];
			for (int j = 0; j < width; ++j)
			{
				maze_[i][j] = new int[layers];
			}
		}
	}

	~Maze()
	{
		for (int i = 0; i < height; ++i)
		{
			for (int j = 0; j < width; ++j)
			{
				delete[] maze_[i][j];
			}
			delete[] maze_[i];
		}
		delete[] maze_;
	}

	void setValue(int h, int w, int l, int value)
	{
		maze_[h][w][l] = value;
	}

	bool find_maze_path()
	{
		int r = 0;
		int c = 0;
		int l = 0;
		return find_maze_path(maze_, r, c, l);
	}
	bool find_maze_path(int*** maze_, int r, int c, int l)
	{
		if (r < 0 || r >= height || c < 0 || c >= width || l < 0 || l >= layers) { return false; }
		else if (maze_[r][c][l] != OPEN) { return false; }
		else if (r == height - 1 && c == width - 1 && l == layers - 1) 
		{ 
			maze_[r][c][l] = EXIT;
			return true; 
		}
		else
		{
			maze_[r][c][l] = VISITED;
			if (find_maze_path(L))
			{
				maze_[r][c][l] = LEFT;
				return true;
			}
			else if (find_maze_path(R))
			{
				maze_[r][c][l] = RIGHT;
				return true;
			}
			else if (find_maze_path(U))
			{
				maze_[r][c][l] = UP;
				return true;
			}
			else if (find_maze_path(D))
			{
				maze_[r][c][l] = DOWN;
				return true;
			}
			else if (find_maze_path(O))
			{
				maze_[r][c][l] = OUT;
				return true;
			}
			else if (find_maze_path(I))
			{
				maze_[r][c][l] = IN;
				return true;
			}
			else
			{
				return false;
			}
		}
	}
	

	string toString() const
	{
		string output;
		for (int i = 0; i < layers; ++i)
		{
			output += "Layer " + to_string(i + 1) + "\n";
			for (int k = 0; k < height; ++k)
			{
				for (int j = 0; j < width; ++j)
				{
					if (maze_[k][j][i] == OPEN) output += " _";
					if (maze_[k][j][i] == VISITED) output += " *";
					if (maze_[k][j][i] == BLOCKED) output += " X";
					if (maze_[k][j][i] == LEFT) output += " L";
					if (maze_[k][j][i] == RIGHT) output += " R";
					if (maze_[k][j][i] == UP) output += " U";
					if (maze_[k][j][i] == DOWN) output += " D";
					if (maze_[k][j][i] == IN) output += " I";
					if (maze_[k][j][i] == OUT) output += " O";
					if (maze_[k][j][i] == EXIT) output+= " E";
				}
				output += "\n";
			}
		}
		
		
		return output;
	}

	friend ostream& operator<< (ostream& os, Maze& maze)
	{
		os << maze.toString();
		return os;
	}
};
#endif
