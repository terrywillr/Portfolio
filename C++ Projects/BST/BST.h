#ifndef BST_H
#define BST_H
#include "BSTInterface.h"
#include "Node.h"
#include <iostream>

using namespace std;

template <typename T>
class BST : public BSTInterface<T>
{
public:
	BST() { this->root_ = NULL; }
	~BST() { clearTree(); }
	
	bool addNode(const T& data)
	{
		return insert(root_, data);
	}
	bool insert(Node<T>*& node, T data);
	
	bool removeNode(const T& data)
	{
		return remove(root_, data);
	}
	bool remove(Node<T>*& node, T data);
		
	bool clearTree()
	{
		while (root_ != NULL)
		{
			removeNode(root_->data);
		}
		size_ = 0;
		return true;
	}
	string toString() const;
	bool outLevel(Node<T>* root, int level, stringstream& out) const;
	
	bool findNode(T data)
	{
		return find(root_, data);
	}
	bool find(Node<T>* root, T data)
	{
		if (root == NULL) return false;
		if (root->data == data) return true;
		if (root->data < data) return find(root->right, data);
		if (root->data > data) return find(root->left, data);
		return false;
	}

	size_t size()
	{
		return size_;
	}

	friend ostream& operator<< (ostream& out, const BST<T>& tree)
	{
		return out << tree.toString();
	}
private:
	Node<T>* root_;
	size_t size_ = 0;
};


#endif //BST_H

template<typename T>
bool BST<T>::remove(Node<T>*& node, T data)
{
	if (node == NULL) return false;
	if (data < node->data) return remove(node->left, data);
	if (data > node->data) return remove(node->right, data);

	Node<T>* oldNode = node;
	if (node->left == NULL) node = node->right;
	else if (node->right == NULL) node = node->left;
	else
	{
		Node<T>* predecessor = node->left;
		while (predecessor->right != NULL) predecessor = predecessor->right;
		swap(node->data, predecessor->data);
		remove(node->left, data);
		return true;
	}
	delete oldNode;
	size_--;
	return true;
}

template<typename T>
bool BST<T>::insert(Node<T>*& node, T data)
{
	if (node == NULL)
	{
		size_++;
		node = new Node<T>(data);
		return true;
	}
	if (data < node->data) return insert(node->left, data);
	if (data > node->data) return insert(node->right, data);
	return false;
}
template<typename T>
string BST<T>::toString() const
{
	stringstream out;
	if (root_ == NULL) out << " empty";
	else
	{
		int level = 0;
		do
		{
			out << endl << " " << ++level << ":";
		} while (outLevel(root_, level, out));
	}
	return out.str();
}

template<typename T>
bool BST<T>::outLevel(Node<T>* root, int level, stringstream& out) const
{
	if (root == NULL) return false;
	if (level == 1)
	{
		out << " " << root->data;
		return (root->left != NULL) || (root->right != NULL);
	}
	if ((level == 2) && !root->left && root->right) out << " _";
	bool left = outLevel(root->left, level - 1, out);
	bool right = outLevel(root->right, level - 1, out);
	if ((level == 2) && root->left && !root->right) out << " _";
	return left || right;
}