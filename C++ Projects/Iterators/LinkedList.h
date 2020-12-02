
#ifndef LINKEDLIST_H
#define LINKEDLIST_H
#include "LinkedListInterface.h"
#include <sstream>
using namespace std;

template<typename T>
class LinkedList : public LinkedListInterface<T>
{
public:
    LinkedList() { this->head = NULL; }
    ~LinkedList() = default;

    struct Node
    {
        T data;
        Node* next;
        Node(const T& d) : data(d), next(NULL) {}
        Node(const T& d, Node* n) : data(d), next(n) {}
    };
    friend ostream& operator<< (ostream& os, LinkedList<T>& linkedList)
    {
        for (Iterator iter = linkedList.begin(); iter != linkedList.end(); ++iter)
        {
            os << "[" << *iter << "]" << endl;
            return os;
        }
    }

    virtual void push_front(const T& value);

    virtual void pop_front(void)
    {
        Node* temp = head;
        head = head->next;
        delete temp;
        --listSize;
    }

    virtual T& front(void)
    {
        Node* ptr = head;
        ptr->data;
        return ptr->data;
    }

    virtual bool empty(void) const
    {
        if (head == NULL)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    virtual void remove(const T& value);

    virtual void clear(void)
    {
        while (head != NULL)
        {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
        listSize = 0;
    }

    virtual void reverse(void);


    virtual size_t size(void) const
    {
        return listSize;
    }

    virtual std::string toString(void) const
    {
        ostringstream os;
        Node* ptr = head;
        while(ptr != NULL)
        {
            os << ptr->data << " ";
            ptr = ptr->next;
        }
        return os.str();
    }
    /****************************************************************************/
    class Iterator
    {
    private:
        Node* node_ptr;
    public:
        Iterator(Node* ptr): node_ptr(ptr) {}
        ~Iterator() = default;
        Node* getNode() { return node_ptr; }
        bool operator!=(const Iterator& rhs) { return this->node_ptr != rhs.node_ptr; }
        bool operator==(const Iterator& rhs) { return this->node_ptr == rhs.node_ptr; }

        T& operator*() { return node_ptr->data; }

        Iterator& operator++()
        {
            if (node_ptr) node_ptr = node_ptr->next;
            return *this;
        }

    };
    /****************************************************************************/
    Iterator begin() { return Iterator(this->head); }
    Iterator end() { return Iterator(NULL); }
    Iterator erase(Iterator position);

    Iterator insert_after(Iterator position, const T& value)
    {
        Node* tmp = new Node(value, position.getNode()->next);
        position.getNode()->next = tmp;
        ++listSize;
        return position;
    }

    Iterator insert_before(Iterator position, const T& value)
    {
        if (position == begin())
        {
            Node* ptr = new Node(value, position.getNode());
            ptr->next = position.getNode();
            head = ptr;
        }
        else
        {
            Node* tmp = new Node(value, position.getNode()->next);
            position.getNode()->next = tmp;
        }
        ++listSize;
        return position;
    }

    Iterator find(Iterator first, Iterator last, const T& value)
    {
        for (Iterator iter = first; iter != last; ++iter)
        {
            if (iter.getNode()->data == value)
            {
                return iter;
            }
        }
        return NULL;
    }

    Iterator replace(Iterator first, Iterator last, const T& oldValue, const T& newValue)
    {
        for (Iterator iter = first; iter != last; ++iter)
        {
            if (iter.getNode()->data == oldValue)
            {
                iter.getNode()->data = newValue;
            }
        }
        return first;
    }
private:
    Node* head;
    size_t listSize = 0;
};
#endif


template<typename T>
void LinkedList<T>::push_front(const T& value)
{
    if (head == NULL)
    {
        head = new Node(value, head);
        head->next = NULL;
    }
    else
    {
        Node* ptr = new Node(value, head);
        ptr->next = head;
        head = ptr;
    }
    ++listSize;
}
template<typename T>
void LinkedList<T>::reverse(void)
{
    Node* current = head;
    Node* prev = NULL;
    Node* next = NULL;
    while (current != NULL)
    {
        next = current->next;
        current->next = prev;
        prev = current;
        current = next;
    }
    head = prev;
}

template<typename T>
void LinkedList<T>::remove(const T& value) {
    Node *temp = head;
    Node *prev = head;
    while (temp != NULL) {
        if (temp->data == value) {
            if (temp == head) {
                head = temp->next;
                delete temp;
                temp = head;
            } else {
                prev->next = temp->next;
                delete temp;
                temp = prev->next;
            }
        } else {
            prev = temp;
            temp = temp->next;
        }
    }
    --listSize;
}
template<typename T>
typename LinkedList<T>::Iterator LinkedList<T>::erase(Iterator position)
{
    Node* ptr = head;
    if(position.getNode() == head)
    {
        ptr = position.getNode()->next;
        delete head;
        head = ptr;
    }
    else
    {
        while ((ptr != NULL) && (ptr->next != NULL))
        {
            if (position.getNode() == ptr->next)
            {
                Node* temp = ptr->next->next;
                delete ptr->next;
                ptr->next = temp;
                break;
            }
            ptr = ptr->next;
        }
    }
    --listSize;
    return LinkedList<T>::Iterator(ptr);
}