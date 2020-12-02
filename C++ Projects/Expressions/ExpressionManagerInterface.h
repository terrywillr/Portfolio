//**** YOU MAY NOT MODIFY THIS DOCUMENT ****/
#ifndef EXPRESSION_INTERFACE_H
#define EXPRESSION_INTERFACE_H
#include <string>
using std::string;


class ExpressionManagerInterface
{
public:
    ExpressionManagerInterface(void) {}
    virtual ~ExpressionManagerInterface(void) {}

    /** Return the integer value of the infix expression */
    virtual int value(void) = 0;

    /** Return the infix items from the expression
        Throw an error if not a valid infix expression as follows:
        First check to see if the expression is balanced ("Unbalanced"),
        then throw the appropriate error immediately when an error is found
        (ie., "Missing Operand", "Illegal Operator", "Missing Operator") */
    virtual std::string infix(void) = 0;

    /** Return a postfix representation of the infix expression */
    virtual std::string postfix(void) = 0;

    /** (BONUS) Return a prefix representation of the infix expression */
    virtual std::string prefix(void) = 0;

    /** Return the infix vector'd expression items */
    virtual std::string toString(void) const = 0;
};
#endif	// EXPRESSION_INTERFACE_H
