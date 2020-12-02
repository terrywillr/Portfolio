#include <iostream>
#include <fstream>
#include <string>

#ifdef _MSC_VER
#define _CRTDBG_MAP_ALLOC
#include <crtdbg.h>
#define VS_MEM_CHECK _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#else
#define VS_MEM_CHECK;
#endif

using namespace std;
#include "LinkedList.h"
int main(int argc, char* argv[]) {
    VS_MEM_CHECK

    ifstream in(argv[1]);
    ofstream out(argv[2]);

    string line;
    LinkedList<string>* linkedList = new LinkedList<string>();

    while (getline(in, line))
    {
        string item1, item2, item3;
        if (line.size() == 0) continue;
        istringstream iss(line);
        iss >> item1;
        out << item1;
        if (item1 == "Insert")
        {
            while (iss >> item2)
            {
                out << " " << item2;
                linkedList->push_front(item2);
            }
            out << endl;
        }

        if (item1 == "Empty")
        {
            if (linkedList->empty())
            {
                out << " true" << endl;
            }
            else
            {
                out << " false" << endl;
            }
        }

        if (item1 == "PrintList")
        {
            if (linkedList->empty())
            {
                out << " Empty!" << endl;
            }
            else {
                out << " " << linkedList->toString() << endl;
            }
        }

        if (item1 == "Size")
        {
            out << " " << linkedList->size() << endl;
        }
        if (item1 == "Clear")
        {
            linkedList->clear();
            out << " OK" << endl;
        }

        if (item1 == "Remove")
        {
            iss >> item2;
            linkedList->remove(item2);
            out << " " << item2 << endl;
        }
        try {
            {
                if (item1 == "InsertAfter")
                {
                    iss >> item2 >> item3;

                    LinkedList<string>::Iterator iter = linkedList->begin();
                    while (iter != linkedList->end())
                    {
                        if (iter.getNode()->data != item3)
                        {
                            ++iter;
                        }
                        else
                        {
                            break;
                        }
                    }
                    if (iter != linkedList->end())
                    {
                        linkedList->insert_after(iter, item2);
                        out << " " << item2 << " " << item3 << " OK" << endl;
                    }
                    else
                    {
                        out << " " << item2 << " " << item3 << " Not Found" << endl;
                    }

                }
                if (item1 == "InsertBefore")
                {
                    iss >> item2 >> item3;

                    LinkedList<string>::Iterator iter = linkedList->begin();

                    while (iter != linkedList->end())
                    {
                        if (iter.getNode()->next == linkedList->end().getNode())
                        {
                            throw " " + item2 + " " + item3 + " Not Found";
                        }
                        if (linkedList->begin().getNode()->data == item3)
                        {
                            linkedList->insert_before(iter, item2);
                            break;
                        }
                        if (iter.getNode()->next->data != item3)
                        {
                            ++iter;
                        }
                        else
                        {
                            linkedList->insert_before(iter, item2);
                            break;
                        }
                    }
                    out << " " << item2 << " " << item3 << " OK" << endl;
                }
                if (item1 == "Erase")
                {
                    iss >> item2;
                    out << " " << item2;
                    LinkedList<string>::Iterator iter = linkedList->begin();
                    while (iter != linkedList->end())
                    {
                        if (iter.getNode()->data != item2)
                        {
                            ++iter;
                        }
                        else
                        {
                            break;
                        }
                    }
                    if (iter != linkedList->end())
                    {
                        linkedList->erase(iter);
                        out << " OK" << endl;
                    }
                    else
                    {
                        out << " Not Found" << endl;
                    }

                }
                if (item1 == "Find")
                {
                    iss >> item2;
                    LinkedList<string>::Iterator iter = linkedList->find(linkedList->begin(), linkedList->end(), item2);
                    if (iter == nullptr)
                    {
                        out << " " << item2 << " Not Found" << endl;
                    }
                    else
                    {
                        out << " " << item2 << " OK" << endl;
                    }
                }
                if (item1 == "Replace")
                {
                    iss >> item2 >> item3;
                    out << " " << item2 << " " << item3;
                    linkedList->replace(linkedList->begin(), linkedList->end(), item2, item3);
                    out << " OK" << endl;
                }
            }
        } catch (string& e) {out << e << endl;}
        try
        {
            string empty = "Empty!";

            if (item1 == "Reverse")
            {
                if (linkedList->empty())
                {
                    throw empty;
                }
                else
                {
                    linkedList->reverse();
                    out << " OK" << endl;
                }
            }

            if (item1 == "First")
            {
                if (linkedList->empty())
                {
                    throw empty;
                }
                else
                {
                    out << " " << linkedList->front() << endl;
                }
            }

            if (item1 == "Delete")
            {
                if (linkedList->empty())
                {
                    throw empty;
                }
                else
                {
                    linkedList->pop_front();
                    out << " OK" << endl;
                }
            }
            if (item1 == "Iterate")
            {
                LinkedList<string>::Iterator iter = linkedList->begin();
                if (linkedList->empty())
                {
                    throw empty;
                }
                else
                {
                    while (iter != linkedList->end())
                    {
                        out << endl << "[" << *iter << "]";
                        ++iter;
                    }
                    out << endl;
                }
            }
        } catch (string& e) {out << " " << e << endl;}
    }
    in.close();
    out.close();
    linkedList->clear();
    delete linkedList;
    return 0;
}
