#include <iostream>
#include <string>
#include <stack>
#include <algorithm>
#include <fstream>
#include <sstream>


#include "ExpressionManager.h"
using namespace std;
int main(int argc, char* argv[]) {
    ifstream in(argv[1]);
    ofstream out(argv[2]);
    string line, command, exp;
    ExpressionManager expression = ExpressionManager(" ");


    while (getline(in, line))
    {
        try
        {
            if (line.size() == 0) continue;
            istringstream iss(line);
            iss >> command;
            if (command == "Expression:") {
                line = line.substr();
                if (line.find_last_of(" ") == line.size() - 1)
                {
                    exp = line.erase(0, command.size() + 1);
                    exp = exp.erase(exp.size() - 1);
                }
                else
                {
                    exp = line.erase(0, command.size() + 1);
                }
                expression.setExpression(exp);
                out << endl << command << " " << expression << endl;


            }
            if (command == "Infix:")
            {
                out << command << " " << expression.infix() << endl;
            }
            if (command == "Prefix:")
            {
                out << command << " " << expression.prefix() << endl;
            }
            if (command == "Postfix:")
            {
                out << command << " " << expression.postfix() << endl;
            }
            if (command == "Value:")
            {
                out << command << " " << expression.value() << endl;
            }

            continue;
        } catch(exception& e) {out << e.what() << endl;}

    }
    return 0;
}
