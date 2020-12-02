# nearest_neighbor.py
"""Volume 2: Nearest Neighbor Search.
<Name>
<Class>
<Date>
"""

import numpy as np
from scipy import linalg as la
from scipy.spatial import KDTree
from scipy import stats
from matplotlib import pyplot as plt


# Problem 1
def exhaustive_search(X, z):
    """Solve the nearest neighbor search problem with an exhaustive search.

    Parameters:
        X ((m,k) ndarray): a training set of m k-dimensional points.
        z ((k, ) ndarray): a k-dimensional target point.

    Returns:
        ((k,) ndarray) the element (row) of X that is nearest to z.
        (float) The Euclidean distance from the nearest neighbor to z.
    """
    index = np.argmin(la.norm((X - z), axis=1))
    return X[index], la.norm(X[index] - z)
    

# Problem 2: Write a KDTNode class.
class KDTNode:
    """Node class for K-D Trees.

    Attributes:
        left (KDTNode): a reference to this node's left child.
        right (KDTNode): a reference to this node's right child.
        value ((k,) ndarray): a coordinate in k-dimensional space.
        pivot (int): the dimension of the value to make comparisons on.
    """
    def __init__(self, x):
        if type(x) != np.ndarray:
            raise TypeError("x must be of type np.ndarray")

        self.value = x
        self.left = None
        self.right = None
        self.pivot = None

# Problems 3 and 4
class KDT:
    """A k-dimensional binary tree for solving the nearest neighbor problem.

    Attributes:
        root (KDTNode): the root node of the tree. Like all other nodes in
            the tree, the root has a NumPy array of shape (k,) as its value.
        k (int): the dimension of the data in the tree.
    """
    def __init__(self):
        """Initialize the root and k attributes."""
        self.root = None
        self.k = None

    def find(self, data):
        """Return the node containing the data. If there is no such node in
        the tree, or if the tree is empty, raise a ValueError.
        """
        def _step(current):
            """Recursively step through the tree until finding the node
            containing the data. If there is no such node, raise a ValueError.
            """
            if current is None:                     # Base case 1: dead end.
                raise ValueError(str(data) + " is not in the tree")
            elif np.allclose(data, current.value):
                return current                      # Base case 2: data found!
            elif data[current.pivot] < current.value[current.pivot]:
                return _step(current.left)          # Recursively search left.
            else:
                return _step(current.right)         # Recursively search right.

        # Start the recursive search at the root of the tree.
        return _step(self.root)

    # Problem 3
    def insert(self, data):
        """Insert a new node containing the specified data.

        Parameters:
            data ((k,) ndarray): a k-dimensional point to insert into the tree.

        Raises:
            ValueError: if data does not have the same dimensions as other
                values in the tree.
            ValueError: if data is already in the tree
        """
        def _insert(data, curNode):
            if curNode.value[curNode.pivot] > data[curNode.pivot]:
                if curNode.left is None:
                    curNode.left = KDTNode(data)
                    curNode.left.pivot = (curNode.pivot + 1) % self.k
                    return curNode.left
                else:
                    _insert(data, curNode.left)
            elif curNode.value[curNode.pivot] < data[curNode.pivot]:               
                if curNode.right is None:
                    curNode.right = KDTNode(data)
                    curNode.right.pivot = (curNode.pivot + 1) % self.k
                    return curNode.right
                else:
                    _insert(data, curNode.right)

            else:
                raise ValueError("Data is already in tree")


        if self.root is None:
            self.root = KDTNode(data)
            self.root.pivot = 0
            self.k = data.shape[0]
            return self.root

        else:
            if data.shape != (self.k,):
                raise ValueError("Data does not contain the correct number of points")
            else:
                return _insert(data, self.root)





    # Problem 4
    def query(self, z):
        """Find the value in the tree that is nearest to z.

        Parameters:
            z ((k,) ndarray): a k-dimensional target point.

        Returns:
            ((k,) ndarray) the value in the tree that is nearest to z.
            (float) The Euclidean distance from the nearest neighbor to z.
        """
        def _query(current, nearest, d_star):
            if current is None:
                return nearest, d_star
            x = current.value
            i = current.pivot
            if la.norm(x - z) < d_star:
                nearest = current
                d_star = la.norm(x - z)
            if z[i] < x[i]:
                nearest, d_star = _query(current.left, nearest, d_star)
                if z[i] + d_star >= x[i]:
                    nearest, d_star = _query(current.right, nearest, d_star)
            else:
                nearest, d_star = _query(current.right, nearest, d_star)
                if z[i] - d_star <= x[i]:
                    nearest, d_star =  _query(current.left, nearest, d_star)
            return nearest, d_star

        node, d_star = _query(self.root, self.root, la.norm(self.root.value - z))
        return node.value, d_star

    def __str__(self):
        """String representation: a hierarchical list of nodes and their axes.

        Example:                           'KDT(k=2)
                    [5,5]                   [5 5]   pivot = 0
                    /   \                   [3 2]   pivot = 1
                [3,2]   [8,4]               [8 4]   pivot = 1
                    \       \               [2 6]   pivot = 0
                    [2,6]   [7,5]           [7 5]   pivot = 0'
        """
        if self.root is None:
            return "Empty KDT"
        nodes, strs = [self.root], []
        while nodes:
            current = nodes.pop(0)
            strs.append("{}\tpivot = {}".format(current.value, current.pivot))
            for child in [current.left, current.right]:
                if child:
                    nodes.append(child)
        return "KDT(k={})\n".format(self.k) + "\n".join(strs)


# Problem 5: Write a KNeighborsClassifier class.
class KNeighborsClassifier:
    """A k-nearest neighbors classifier that uses SciPy's KDTree to solve
    the nearest neighbor problem efficiently.
    """
    def __init__(self, n_neighbors):
        self.k = n_neighbors
        self.data = None
        self.y = None

    def fit(self, X, y):
        tree = KDTree(X)
        self.tree = tree
        self.label = y


    def predict(self, z):
        distances, indices = self.tree.query(z, k=self.k)
        index, count = stats.mode(indices, axis=None)
        return self.label[index]


# Problem 6
def prob6(n_neighbors, filename="mnist_subset.npz"):
    """Extract the data from the given file. Load a KNeighborsClassifier with
    the training data and the corresponding labels. Use the classifier to
    predict labels for the test data. Return the classification accuracy, the
    percentage of predictions that match the test labels.

    Parameters:
        n_neighbors (int): the number of neighbors to use for classification.
        filename (str): the name of the data file. Should be an npz file with
            keys 'X_train', 'y_train', 'X_test', and 'y_test'.

    Returns:
        (float): the classification accuracy.
    """
    data = np.load(filename)
    X_train = data["X_train"].astype(np.float)
    y_train = data["y_train"]
    X_test = data["X_test"].astype(np.float)
    y_test = data["y_test"]

    classifier = KNeighborsClassifier(n_neighbors)
    classifier.fit(X_train, y_train)
    num_correct = 0
    index = 0
    for ele in X_test:
        prediction = classifier.predict(ele)
        if prediction == y_test[index]:
            num_correct += 1
        index += 1


    return num_correct / len(y_test)




"""if __name__ == "__main__":
    print(prob6(4))"""
