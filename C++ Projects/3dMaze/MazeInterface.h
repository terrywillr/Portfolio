//**** YOU MAY NOT MODIFY THIS DOCUMENT ****/
#ifndef MAZE_INTERFACE_H
#define MAZE_INTERFACE_H
#include <string>

class MazeInterface
{
public:
	MazeInterface(void) {}
	~MazeInterface(void) {}

	/** Set maze value
	   @parm height
	   @parm width
	   @parm layer
	   @parm value
	*/
	virtual void setValue(int height, int width, int layer, int value) = 0;

	/** Solve maze
	   @return true if solveable, else false
	*/
	virtual bool find_maze_path() = 0;

	/** Output maze (same order as input maze)
	  @return string of 2D layers
	*/
	virtual std::string toString() const = 0;

};
#endif // MAZE_INTERFACE_H