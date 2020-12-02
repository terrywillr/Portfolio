#ifndef LAB05_EXPRESSIONMANAGER_H
#define LAB05_EXPRESSIONMANAGER_H
#include "ExpressionManagerInterface.h"
#include <vector>
#include <stack>
#include <algorithm>
using namespace std;
class ExpressionManager: public ExpressionManagerInterface
{
public:
    ExpressionManager(string exp) : expression_(exp) { }
    ~ExpressionManager() {}
    int value();
    string infix();

    string postfix();

    string prefix();

    string toString() const
    {
        return expression_;
    }
    void setExpression(string exp) { expression_ = exp; }

    friend ostream& operator<< (ostream& os, const ExpressionManager& expression)
    {
        os << expression.toString();
        return os;
    }
    bool isDigit(const string s)
    {
        return !s.empty() && s.find_first_not_of("0123456789") == string::npos;
    }
    int isOperator(string s);
private:
    string expression_;
    vector<string> postFix_;
    vector<string> preFix_;
    vector<string> eval;
    string operators = "([{ +-  */% )]}";


};

#endif //LAB05_EXPRESSIONMANAGER_H
