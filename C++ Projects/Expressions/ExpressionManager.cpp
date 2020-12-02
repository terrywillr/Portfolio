#include "ExpressionManager.h"
#include <sstream>

string ExpressionManager::infix()
{
    vector<string> formatString;


    stack<char> balanceCheck;
    string toReturn = expression_;
    bool isBalanced = true;
    size_t index = 0;
    stringstream item(expression_);
    string intermediate;
    while (char ch = expression_[index++])
    {
        if (ch == '(' || ch == '[' || ch == '{') {balanceCheck.push(ch);}
        if (ch == ')')
        {
            if (balanceCheck.empty()) {isBalanced = false; break;}
            char top = balanceCheck.top();
            balanceCheck.pop();
            if (top != '(') { isBalanced = false; break;}
        }
        if (ch == ']')
        {
            if (balanceCheck.empty()) {isBalanced = false; break;}
            char top = balanceCheck.top();
            balanceCheck.pop();
            if (top != '[') { isBalanced = false; break;}
        }
        if (ch == '}')
        {
            if (balanceCheck.empty()) {isBalanced = false; break;}
            char top = balanceCheck.top();
            balanceCheck.pop();
            if (top != '{') { isBalanced = false; break;}
        }

    }
    if (!isBalanced) { return "Unbalanced"; }


    stack<string> correctOperands;
    vector<string> v;
    stringstream items(expression_);
    string inter;
    while (getline(items, inter, ' '))
    {
        if (operators.find(inter) / 4 != 0 && operators.find(inter) / 4 != 3)
        {
            v.push_back(inter);
        }
    }
    if (!isDigit(v.at(0)))
    {
        return "Missing Operand";
    }
    reverse(v.begin(), v.end());

    for (size_t i = 0; i < v.size(); ++i)
    {
        correctOperands.push(v.at(i));
    }
    for (size_t i = 0; i < correctOperands.size(); ++ i)
    {
        if (v.size() <= 1)
        {
            break;
        }
        if (isDigit(correctOperands.top()))
        {
            correctOperands.pop();
            if (isDigit(correctOperands.top()))
            {
                return "Missing Operator";
            }
        }
        else if (operators.find(correctOperands.top()) / 4 == 1 || operators.find(correctOperands.top()) / 4 == 2)
        {
            correctOperands.pop();
            if (!isDigit(correctOperands.top()))
            {
                return "Missing Operand";
            }
        }
        else
        {
            return "Illegal Operator";
        }
    }
    if (!isDigit(v.at(0)))
    {
        return "Missing Operand";
    }
    v.clear();
    return toReturn;
}

string ExpressionManager::postfix()
{
    stack<string> operator_stack;

    stringstream items(expression_);
    string intermediate;
    string outfix_expression;

    while (getline(items, intermediate, ' '))
    {
        postFix_.push_back(intermediate);
    }
    for (size_t i = 0; i < postFix_.size(); ++i)
    {
        if (operators.find(postFix_.at(i)) == string::npos)
        {
            outfix_expression += postFix_.at(i) + " ";
        }
        else if (operators.find(postFix_.at(i)) / 4 == 0)
        {
            operator_stack.push(postFix_.at(i));
        }
        else if (postFix_.at(i) == ")")
        {
            while (!operator_stack.empty() && operator_stack.top() != "(")
            {
                string c = operator_stack.top();
                operator_stack.pop();
                outfix_expression += c + " ";
            }
            if (operator_stack.top() == "(")
            {
                operator_stack.pop();
            }
        }
        else if (postFix_.at(i) == "]")
        {
            while (!operator_stack.empty() && operator_stack.top() != "[")
            {
                string c = operator_stack.top();
                operator_stack.pop();
                outfix_expression += c + " ";
            }
            if (operator_stack.top() == "[")
            {
                operator_stack.pop();
            }
        }
        else if (postFix_.at(i) == "}")
        {
            while (!operator_stack.empty() && operator_stack.top() != "{")
            {
                string c = operator_stack.top();
                operator_stack.pop();
                outfix_expression += c + " ";
            }
            if (operator_stack.top() == "{")
            {
                operator_stack.pop();
            }
        }
        else
        {
            while (!operator_stack.empty() && operators.find(postFix_.at(i)) / 4 <= operators.find(operator_stack.top()) / 4)
            {
                string c = operator_stack.top();
                operator_stack.pop();
                outfix_expression += c + " ";
            }
            operator_stack.push(postFix_.at(i));
        }
    }

    while (!operator_stack.empty())
    {
        string c= operator_stack.top();
        operator_stack.pop();
        outfix_expression += c + " ";
    }
    postFix_.clear();
    return outfix_expression;
}

string ExpressionManager::prefix()
{
    stack<string> operator_stack;

    stringstream items(expression_);
    string intermediate;
    string outfix_expression;

    while (getline(items, intermediate, ' '))
    {
        if (intermediate == "(")
        {
            preFix_.push_back(")");
        }
        else if (intermediate == "[")
        {
            preFix_.push_back("]");
        }
        else if (intermediate == "{")
        {
            preFix_.push_back("}");
        }
        else if (intermediate == ")")
        {
            preFix_.push_back("(");
        }
        else if (intermediate == "]")
        {
            preFix_.push_back("[");
        }
        else if (intermediate == "}")
        {
            preFix_.push_back("{");
        }
        else
        {
            preFix_.push_back(intermediate);
        }
    }
    reverse(preFix_.begin(), preFix_.end());
    for (size_t i = 0; i < preFix_.size(); ++i)
    {
        if (operators.find(preFix_.at(i)) == string::npos)
        {
            outfix_expression += preFix_.at(i) + " ";
        }
        else if (operators.find(preFix_.at(i)) / 4 == 0)
        {
            operator_stack.push(preFix_.at(i));
        }
        else if (preFix_.at(i) == ")")
        {
            while (!operator_stack.empty() && operator_stack.top() != "(")
            {
                string c = operator_stack.top();
                operator_stack.pop();
                outfix_expression += c + " ";
            }
            if (operator_stack.top() == "(")
            {
                operator_stack.pop();
            }
        }
        else if (preFix_.at(i) == "]")
        {
            while (!operator_stack.empty() && operator_stack.top() != "[")
            {
                string c = operator_stack.top();
                operator_stack.pop();
                outfix_expression += c + " ";
            }
            if (operator_stack.top() == "[")
            {
                operator_stack.pop();
            }
        }
        else if (preFix_.at(i) == "}")
        {
            while (!operator_stack.empty() && operator_stack.top() != "{")
            {
                string c = operator_stack.top();
                operator_stack.pop();
                outfix_expression += c + " ";
            }
            if (operator_stack.top() == "{")
            {
                operator_stack.pop();
            }
        }
        else
        {
            while (!operator_stack.empty() && operators.find(preFix_.at(i)) / 4 > operators.find(operator_stack.top()) / 4 && operators.find(operator_stack.top()) / 4 != 0)
            {
                string c = operator_stack.top();
                operator_stack.pop();
                outfix_expression += c + " ";
            }
            operator_stack.push(preFix_.at(i));
        }
    }

    while (!operator_stack.empty())
    {
        string c= operator_stack.top();
        operator_stack.pop();
        outfix_expression += c + " ";
    }
    stringstream reversal(outfix_expression);
    vector<string> toReverse;
    string middle;
    while(getline(reversal, middle, ' '))
    {
        toReverse.push_back(middle + " ");
    }
    reverse(toReverse.begin(), toReverse.end());
    string newString;
    for (size_t i = 0; i < toReverse.size(); ++i)
    {
        newString += toReverse.at(i);
    }
    preFix_.clear();
    return newString;
}


int ExpressionManager::value()
{
    ExpressionManager expression = ExpressionManager(expression_);
    string calc_exp = expression.postfix();
    stack<int> stk;
    stringstream items(calc_exp);
    string intermediate;
    while(getline(items, intermediate, ' '))
    {
        eval.push_back(intermediate);
    }
    for (size_t i = 0; i < eval.size(); ++i)
    {
        if (isDigit(eval.at(i)))
        {
            stk.push(stoi(eval.at(i)));
        }
        else
        {

            int val1 = stk.top();
            stk.pop();
            int val2 = stk.top();
            stk.pop();
            switch (isOperator(eval.at(i)))
            {
                case 1: stk.push(val2 + val1); break;
                case 2: stk.push(val2 - val1); break;
                case 3: stk.push(val2 * val1); break;
                case 4: stk.push(val2 / val1); break;
                case 5: stk.push(val2 % val1); break;
            }
        }
    }
    return stk.top();
}
int ExpressionManager::isOperator(string s)
{
    if (s == "+") {return 1;}
    if (s == "-") {return 2;}
    if (s == "*") {return 3;}
    if (s == "/") {return 4;}
    if (s == "%") {return 5;}
}
