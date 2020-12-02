# numpy_intro.py
"""Python Essentials: Intro to NumPy.
<Name>William Terry
<Class>Math 321 Section 004
<Date> 9/10/20
"""
import numpy as np

def prob1():
    """Define the matrices A and B as arrays. Return the matrix product AB."""
    A = np.array([[3, -1, 4], [1, 5, -9]])
    B = np.array([[2, 6, -5, 3],[5, -8, 9, 7],[9, -3, -2, -3]])

    return np.dot(A, B)


def prob2():
    """Define the matrix A as an array. Return the matrix -A^3 + 9A^2 - 15A."""
    A = np.array([[3, 1, 4], [1, 5, 9], [-5, 3, 1]])
    return -1 *(np.dot(np.dot(A, A), A)) + 9 * (np.dot(A, A)) - 15 * A


def prob3():
    """Define the matrices A and B as arrays. Calculate the matrix product ABA,
    change its data type to np.int64, and return it.
    """
    A = np.triu(np.ones((7, 7), dtype=np.int))
    B = np.tril(-1 * np.ones((7, 7), dtype=np.int)) + np.triu(5 * np.ones((7, 7), dtype=np.int)) -  5 * np.diag(np.ones((7), dtype = np.int))
    return np.dot(np.dot(A, B), A).astype(np.int64)


def prob4(A):
    """Make a copy of 'A' and set all negative entries of the copy to 0.
    Return the copy.

    Example:
        >>> A = np.array([-3,-1,3])
        >>> prob4(A)
        array([0, 0, 3])
    """
    mask = A < 0   #Creates array of boolean statements that are true for values less than 0
    A[mask] = 0    #Any negative values are thus set to 0
    return A


def prob5():
    """Define the matrices A, B, and C as arrays. Return the block matrix
                                | 0 A^T I |
                                | A  0  0 |,
                                | B  0  C |
    where I is the 3x3 identity matrix and each 0 is a matrix of all zeros
    of the appropriate size.
    """
    A = (np.arange(6).reshape(3, 2)).T
    B = np.tril(3 * np.ones((3, 3)))
    C = np.eye(3) * np.diag((-2 * np.ones(3)))
    I = np.eye(3)
    """R1, R2, R3 create each row of the block matrix."""
    R1 = np.hstack((np.zeros((3, 3)), A.T, I))
    R2 = np.hstack((A, np.zeros((2,2)), np.zeros((2,3))))
    R3 = np.hstack((B, np.zeros((3,2)), C))
    return np.vstack((R1, R2, R3)).astype(np.int64)   #stacks each row into the whole block matrix

def prob6(A):
    """Divide each row of 'A' by the row sum and return the resulting array.

    Example:
        >>> A = np.array([[1,1,0],[0,1,0],[1,1,1]])
        >>> prob6(A)
        array([[ 0.5       ,  0.5       ,  0.        ],
               [ 0.        ,  1.        ,  0.        ],
               [ 0.33333333,  0.33333333,  0.33333333]])
    """
    arraysum = A.sum(axis=1)
    return A / arraysum.reshape((len(A), 1))


def prob7():
    """Given the array stored in grid.npy, return the greatest product of four
    adjacent numbers in the same direction (up, down, left, right, or
    diagonally) in the grid.
    """
    grid = np.load("grid.npy")
    horizontal = np.max(grid[:,:-3] * grid[:,1:-2] * grid[:,2:-1] * grid[:,3:])
    vertical = np.max(grid[:-3,:] * grid[1:-2,:] * grid[2:-1,:] * grid[3:,:])
    diagonal_left = np.max(grid[:-3,:-3] * grid[1:-2,1:-2] * grid[2:-1,2:-1] * grid[3:,3:])
    diagonal_right = np.max(grid[3:,:-3] * grid[2:-1,1:-2] * grid[1:-2,2:-1] * grid[:-3,3:])
    return max(horizontal, vertical, diagonal_left, diagonal_right)

"""if __name__ == "__main__":
    print(prob1())
    print(prob2())
    print(prob3())
    print(prob4(np.array([-12,  10, -11, -42, -13, -35,  46,  36, -15, -46])))
    print(prob5())
    print(prob6(np.array([[1,1,0, 1],[0,1,0, 0],[1,1,1, 1]])))
    print(prob7())"""
