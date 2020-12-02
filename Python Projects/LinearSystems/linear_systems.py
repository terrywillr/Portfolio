# linear_systems.py
"""Volume 1: Linear Systems.
<Name>
<Class>
<Date>
"""
import numpy as np
from scipy import linalg as la
from matplotlib import pyplot as plt
import time
from scipy import sparse
from scipy.sparse import linalg as spla

# Problem 1
def ref(A):
    """Reduce the square matrix A to REF. You may assume that A is invertible
    and that a 0 will never appear on the main diagonal. Avoid operating on
    entries that you know will be 0 before and after a row operation.

    Parameters:
        A ((n,n) ndarray): The square invertible matrix to be reduced.

    Returns:
        ((n,n) ndarray): The REF of A.
    """
    r, c = A.shape
    if r == 0 or c == 0:
        return A

    for i in range(len(A)):
        if A[i,0] != 0:
            break
        else:
            B = ref(A[:,1:])
            return np.hstack([A[:,:1], B])

        if i < 0:
            ith_row = A[i].copy()
            A[i] = A[0]
            A[0] = ith_row

    A[0] = A[0] / A[0,0]
    A[1:] -= A[0] * A[1:,0:1]

    A[1:] -= A[0] * A[1:,0:1]

    B = ref(A[1:,1:])

    return np.vstack([A[:1], np.hstack([A[1:,:1], B]) ])



# Problem 2
def lu(A):
    """Compute the LU decomposition of the square matrix A. You may
    assume that the decomposition exists and requires no row swaps.

    Parameters:
        A ((n,n) ndarray): The matrix to decompose.

    Returns:
        L ((n,n) ndarray): The lower-triangular part of the decomposition.
        U ((n,n) ndarray): The upper-triangular part of the decomposition.
    """
    m, n = A.shape
    U = A.copy()
    L = np.eye(m)

    for i in range(n - 1):
        for j in range(i + 1, m):
            L[j,i] = U[j,i] / U[i,i]
            U[j,i:] = U[j,i:] - L[j,i] * U[i,i:]

    return  L, U


# Problem 3
def solve(A, b):
    """Use the LU decomposition and back substitution to solve the linear
    system Ax = b. You may again assume that no row swaps are required.

    Parameters:
        A ((n,n) ndarray)
        b ((n,) ndarray)

    Returns:
        x ((m,) ndarray): The solution to the linear system.
    """
    n = A.shape[0]
    L, U = lu(A)

    y = np.zeros((n,))
    x = np.zeros((n,))

    y[0] = b[0]
    for k in range(1, n):
        y[k] = b[k]
        for j in range(k):
            y[k] -= L[k][j] * y[j]


    for k in range(n-1, -1, -1):
        x[k] = (1 / U[k][k]) * y[k]
        for j in range(k + 1, n):
            x[k] -= (1 / U[k][k]) * U[k][j] * x[j]

    return x

# Problem 4
def prob4():
    """Time different scipy.linalg functions for solving square linear systems.

    For various values of n, generate a random nxn matrix A and a random
    n-vector b using np.random.random(). Time how long it takes to solve the
    system Ax = b with each of the following approaches:

        1. Invert A with la.inv() and left-multiply the inverse to b.
        2. Use la.solve().
        3. Use la.lu_factor() and la.lu_solve() to solve the system with the
            LU decomposition.
        4. Use la.lu_factor() and la.lu_solve(), but only time la.lu_solve()
            (not the time it takes to do the factorization).

    Plot the system size n versus the execution times. Use log scales if
    needed.
    """
    domain = 2**np.arange(1,7)

    times1 = []
    for n in domain:
        A = np.random.random((n, n))
        b = np.random.random(n)
        start = time.time()
        x = la.inv(A) @ b
        times1.append(time.time() - start)

    times2 = []
    for n in domain:
        A = np.random.random((n, n))
        b = np.random.random(n)
        start = time.time()
        x = la.solve(A, b)
        times2.append(time.time() - start)

    times3 = []
    for n in domain:
        A = np.random.random((n, n))
        b = np.random.random(n)
        start = time.time()
        L, P = la.lu_factor(A)
        x = la.lu_solve((L,P), b)
        times3.append(time.time() - start)

    times4 = []
    for n in domain:
        A = np.random.random((n, n))
        b = np.random.random(n)
        L, P = la.lu_factor(A)
        start = time.time()
        x = la.lu_solve((L,P), b)
        times4.append(time.time() - start)

    plt.xlabel("n")
    plt.ylabel("Seconds")
    plt.plot(domain, times1, label="inv()")
    plt.plot(domain, times2, label="solve()")
    plt.plot(domain, times3, label="lu_factor, lu_solve")
    plt.plot(domain, times4, label="lu_solve")
    plt.legend()

    plt.show()

# Problem 5
def prob5(n):
    """Let I be the n × n identity matrix, and define
                    [B I        ]        [-4  1            ]
                    [I B I      ]        [ 1 -4  1         ]
                A = [  I . .    ]    B = [    1  .  .      ],
                    [      . . I]        [          .  .  1]
                    [        I B]        [             1 -4]
    where A is (n**2,n**2) and each block B is (n,n).
    Construct and returns A as a sparse matrix.

    Parameters:
        n (int): Dimensions of the sparse matrix B.

    Returns:
        A ((n**2,n**2) SciPy sparse matrix)
    """
    I = sparse.diags(([1], [1]), [-n, n], shape=(n**2, n**2))
    diagonals = ([1], [-4], [1])
    offsets = [-1, 0, 1]
    B = sparse.diags(diagonals, offsets, shape=(n, n))
    A = sparse.block_diag([B] * n)
    A += I
    """plt.spy(A, markersize=1)
    plt.show()"""

    return A


# Problem 6
def prob6():
    """Time regular and sparse linear system solvers.

    For various values of n, generate the (n**2,n**2) matrix A described of
    prob5() and vector b of length n**2. Time how long it takes to solve the
    system Ax = b with each of the following approaches:

        1. Convert A to CSR format and use scipy.sparse.linalg.spsolve()
        2. Convert A to a NumPy array and use scipy.linalg.solve().

    In each experiment, only time how long it takes to solve the system (not
    how long it takes to convert A to the appropriate format). Plot the system
    size n**2 versus the execution times. As always, use log scales where
    appropriate and use a legend to label each line.
    """
    domain = np.arange(1, 20)
    times1 = []
    times2 = []
    for n in domain:
        A = prob5(n)
        b = np.random.random(n**2)
        Acsr = A.tocsr()
        start = time.time()
        x = spla.spsolve(Acsr, b)
        times1.append(time.time() - start)

        Anp = A.toarray()
        start = time.time()
        x = la.solve(Anp, b)
        times2.append(time.time() - start)


    plt.xlabel("n")
    plt.ylabel("seconds")
    plt.plot(domain, times1, label="CSR format")
    plt.plot(domain, times2, label="NumPy format")
    plt.legend(loc="upper right")

    plt.show()


