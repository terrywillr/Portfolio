# linear_transformations.py
"""Volume 1: Linear Transformations.
<Name>
<Class>
<Date>
"""

from random import random
import numpy as np
from matplotlib import pyplot as plt


# Problem 1
def stretch(A, a, b):
    """Scale the points in A by a in the x direction and b in the
    y direction.

    Parameters:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        a (float): scaling factor in the x direction.
        b (float): scaling factor in the y direction.
    """
    matrixStretch = np.array([[a, 0], [0, b]])
    return np.dot(matrixStretch, A)




def shear(A, a, b):
    """Slant the points in A by a in the x direction and b in the
    y direction.

    Parameters:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        a (float): scaling factor in the x direction.
        b (float): scaling factor in the y direction.
    """
    matrixShear = np.array([[1, a], [b, 1]])
    return np.dot(matrixShear, A)

def reflect(A, a, b):
    """Reflect the points in A about the line that passes through the origin
    and the point (a,b).

    Parameters:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        a (float): x-coordinate of a point on the reflecting line.
        b (float): y-coordinate of the same point on the reflecting line.
    """
    matrixReflect = (1 / (a**2 + b**2)) * np.array([[a**2 - b**2, 2 * a * b], [2 * a * b, b**2 - a **2]])
    return np.dot(matrixReflect, A)

def rotate(A, theta):
    """Rotate the points in A about the origin by theta radians.

    Parameters:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        theta (float): The rotation angle in radians.
    """
    matrixRotate = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    return np.dot(matrixRotate, A)


# Problem 2
def solar_system(T, x_e, x_m, omega_e, omega_m):
    """Plot the trajectories of the earth and moon over the time interval [0,T]
    assuming the initial position of the earth is (x_e,0) and the initial
    position of the moon is (x_m,0).

    Parameters:
        T (int): The final time.
        x_e (float): The earth's initial x coordinate.
        x_m (float): The moon's initial x coordinate.
        omega_e (float): The earth's angular velocity.
        omega_m (float): The moon's angular velocity.
    """
    def p_e(t):
        return rotate(np.array([x_e, 0]), t * omega_e)
    def p_m(t):
        moon_to_earth = rotate(np.array([x_m, 0]) - np.array([x_e, 0]), t * omega_m)
        return moon_to_earth + p_e(t)

    times = np.linspace(0, T, 100)
    earth_positions = []
    for time in times:
        earth_position = p_e(time)
        earth_positions.append(earth_position)

    moon_positions = []
    for time in times:
        moon_position = p_m(time)
        moon_positions.append(moon_position)

    x1 = np.asarray(earth_positions)[:,0]
    y1 = np.asarray(earth_positions)[:,1]
    x2 = np.asarray(moon_positions)[:,0]
    y2 = np.asarray(moon_positions)[:,1]

    plt.plot(x1, y1, x2, y2)
    plt.gca().set_aspect("equal")
    plt.show()


def random_vector(n):
    """Generate a random vector of length n as a list."""
    return [random() for i in range(n)]

def random_matrix(n):
    """Generate a random nxn matrix as a list of lists."""
    return [[random() for j in range(n)] for i in range(n)]

def matrix_vector_product(A, x):
    """Compute the matrix-vector product Ax as a list."""
    m, n = len(A), len(x)
    return [sum([A[i][k] * x[k] for k in range(n)]) for i in range(m)]

def matrix_matrix_product(A, B):
    """Compute the matrix-matrix product AB as a list of lists."""
    m, n, p = len(A), len(B), len(B[0])
    return [[sum([A[i][k] * B[k][j] for k in range(n)])
                                    for j in range(p) ]
                                    for i in range(m) ]
import time
# Problem 3
def prob3():
    """Use time.time(), timeit.timeit(), or %timeit to time
    matrix_vector_product() and matrix-matrix-mult() with increasingly large
    inputs. Generate the inputs A, x, and B with random_matrix() and
    random_vector() (so each input will be nxn or nx1).
    Only time the multiplication functions, not the generating functions.

    Report your findings in a single figure with two subplots: one with matrix-
    vector times, and one with matrix-matrix times. Choose a domain for n so
    that your figure accurately describes the growth, but avoid values of n
    that lead to execution times of more than 1 minute.
    """
    domain1 = 2**np.arange(1,9)
    times1 = []
    for n in domain1:
        A = random_matrix(n)
        v = random_vector(n)
        start = time.time()
        matrix_vector_product(A, v)
        times1.append(time.time() - start)

    domain2 = 2**np.arange(1,9)
    times2 = []
    for n in domain2:
        A = random_matrix(n)
        B = random_matrix(n)
        start = time.time()
        matrix_matrix_product(A, B)
        times2.append(time.time() - start)

    ax1 = plt.subplot(121)
    ax1.set_title("Matrix-Vector Multiplication")
    ax1.set_xlabel("n")
    ax1.set_ylabel("Seconds")
    ax1.plot(domain1, times1, 'g.-')


    ax2 = plt.subplot(122)
    ax2.set_title("Matrix-Matrix Multiplication")
    ax2.set_xlabel("n")
    ax2.set_ylabel("Seconds")
    ax2.plot(domain2, times2, 'b.-')

    plt.show()


# Problem 4
def prob4():
    """Time matrix_vector_product(), matrix_matrix_product(), and np.dot().

    Report your findings in a single figure with two subplots: one with all
    four sets of execution times on a regular linear scale, and one with all
    four sets of exections times on a log-log scale.
    """
    domain1 = 2**np.arange(1,7)
    domain2 = 2**np.arange(1,7)
    domain3 = 2**np.arange(1,7)
    domain4 = 2**np.arange(1,7)
    times1 = []
    for n in domain1:
        A = random_matrix(n)
        v = random_vector(n)
        start = time.time()
        matrix_vector_product(A, v)
        end = time.time()
        times1.append(end - start)

    times2 = []
    for n in domain2:
        A = random_matrix(n)
        B = random_matrix(n)
        start = time.time()
        matrix_matrix_product(A, B)
        end = time.time()
        times2.append(end - start)

    times3 = []
    for n in domain3:
        A = random_matrix(n)
        v = random_vector(n)
        start = time.time()
        end = time.time()
        np.dot(A, v)
        times3.append(end - start)

    times4 = []
    for n in domain4:
        A = random_matrix(n)
        B = random_matrix(n)
        start = time.time()
        np.dot(A, B)
        end = time.time()
        times4.append(end - start)

    ax1 = plt.subplot(121)
    ax1.set_xlabel("n")
    ax1.set_ylabel("Seconds")
    ax1.plot(domain1, times1)
    ax1.plot(domain2, times2)
    ax1.plot(domain3, times3)
    ax1.plot(domain4, times4)

    ax2 = plt.subplot(122)
    ax2.set_xlabel("n")
    ax2.set_ylabel("Seconds")
    ax2.loglog(domain1, times1, basex=2, basey=2)
    ax2.loglog(domain2, times2, basex=2, basey=2)
    ax2.loglog(domain3, times3, basex=2, basey=2)
    ax2.loglog(domain4, times4, basex=2, basey=2)

    plt.show()



def test_prob1():
    data = reflect(np.load("horse.npy"), 0, 1)
    plt.plot(data[0], data[1], 'k,')
    plt.axis([-1, 1, -1, 1])
    plt.gca().set_aspect("equal")
    plt.show()


"""if __name__ == "__main__":
    prob4()"""



