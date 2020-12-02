//**** YOU MAY NOT MODIFY THIS DOCUMENT ****/
#ifndef LINKED_LIST_INTERFACE_H
#define LINKED_LIST_INTERFACE_H
#include <string>

template<typename T>
class LinkedListInterface
{
public:
    LinkedListInterface(void) {}
    virtual ~LinkedListInterface(void) {}

    /** Insert Node(value) at beginning of linked list */
    virtual void push_front(const T& value) = 0;

    /** Remove Node at beginning of linked list */
    virtual void pop_front(void) = 0;

    /** Return reference to value of Node at beginning of linked list */
    virtual T& front(void) = 0;

    /** Return true if linked list size == 0 */
    virtual bool empty(void) const = 0;

    /** Remove all Nodes with value from linked list */
    virtual void remove(const T& value) = 0;

    /** Remove all Nodes from linked list */
    virtual void clear(void) = 0;

    /** Reverse Nodes in linked list */
    virtual void reverse(void) = 0;

    /** Return the number of nodes in the linked list */
    virtual size_t size(void) const = 0;

    /** Return contents of Linked List as a string */
    virtual std::string toString(void) const = 0;
};
#endif	// LINKED_LIST_INTERFACE_H