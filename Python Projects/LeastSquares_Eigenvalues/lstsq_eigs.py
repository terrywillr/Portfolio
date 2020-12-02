# lstsq_eigs.py
"""Volume 1: Least Squares and Computing Eigenvalues.
<Name>
<Class>
<Date>
"""

# (Optional) Import functions from your QR Decomposition lab.
# import sys
# sys.path.insert(1, "../QR_Decomposition")
# from qr_decomposition import qr_gram_schmidt, qr_householder, hessenberg

import numpy as np
from matplotlib import pyplot as plt
from scipy import linalg as la
import cmath


# Problem 1
def least_squares(A, b):
    """Calculate the least squares solutions to Ax = b by using the QR
    decomposition.

    Parameters:
        A ((m,n) ndarray): A matrix of rank n <= m.
        b ((m, ) ndarray): A vector of length m.

    Returns:
        x ((n, ) ndarray): The solution to the normal equations.
    """
    Q, R = la.qr(A, mode="economic")
    return la.solve_triangular(R, np.dot(Q.T, b))

# Problem 2
def line_fit():
    """Find the least squares line that relates the year to the housing price
    index for the data in housing.npy. Plot both the data points and the least
    squares line.
    """
    grid = np.load("housing.npy")
    m, n = grid.shape
    ones = np.ones(m)
    years = grid[:,0]
    A = np.column_stack((years, ones))
    y = grid[:,1]
    x = least_squares(A, y)
    

    plt.scatter(years, y, label="Data Points")
    plt.plot(years, x[0] * years + x[1], label="Least Squares Fit")

    plt.legend()
    plt.show()




# Problem 3
def polynomial_fit():
    """Find the least squares polynomials of degree 3, 6, 9, and 12 that relate
    the year to the housing price index for the data in housing.npy. Plot both
    the data points and the least squares polynomials in individual subplots.
    """
    grid = np.load("housing.npy")
    m, n = grid.shape

    domain = np.linspace(0, 17, m)
    deg3 = np.vander(grid[:,0], 3)
    deg6 = np.vander(grid[:,0], 6)
    deg9 = np.vander(grid[:,0], 9)
    
    y = grid[:,1]

    f_3 = np.poly1d(la.lstsq(deg3, y)[0])
    f_6 = np.poly1d(la.lstsq(deg6, y)[0])
    f_9 = np.poly1d(la.lstsq(deg9, y)[0])

    ax1 = plt.subplot(221)
    ax1.scatter(domain, y)
    ax1.plot(domain, f_3(domain))
    ax1.set_title("Degree 3")

    ax2 = plt.subplot(222)
    ax2.scatter(domain, y)
    ax2.plot(domain, f_6(domain))
    ax2.set_title("Degree 6")
    
    ax3 = plt.subplot(223)
    ax3.scatter(domain, y)
    ax3.plot(domain, f_6(domain))
    ax3.set_title("Degree 9")

    plt.tight_layout()
    plt.show()



def plot_ellipse(a, b, c, d, e):
    """Plot an ellipse of the form ax^2 + bx + cxy + dy + ey^2 = 1."""
    theta = np.linspace(0, 2*np.pi, 200)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    A = a*(cos_t**2) + c*cos_t*sin_t + e*(sin_t**2)
    B = b*cos_t + d*sin_t
    r = (-B + np.sqrt(B**2 + 4*A)) / (2*A)

    plt.plot(r*cos_t, r*sin_t)
    plt.gca().set_aspect("equal", "datalim")

# Problem 4
def ellipse_fit():
    """Calculate the parameters for the ellipse that best fits the data in
    ellipse.npy. Plot the original data points and the ellipse together, using
    plot_ellipse() to plot the ellipse.
    """
    xk, yk = np.load("ellipse.npy").T
    m = xk.shape
    A = np.column_stack((xk ** 2, xk, xk * yk, yk, yk ** 2))
    x = la.lstsq(A, np.ones(m))[0]
    plt.scatter(xk, yk)
    plot_ellipse(x[0], x[1], x[2], x[3], x[4])
    plt.show()


# Problem 5
def power_method(A, N=20, tol=1e-12):
    """Compute the dominant eigenvalue of A and a corresponding eigenvector
    via the power method.

    Parameters:
        A ((n,n) ndarray): A square matrix.
        N (int): The maximum number of iterations.
        tol (float): The stopping tolerance.

    Returns:
        (float): The dominant eigenvalue of A.
        ((n,) ndarray): An eigenvector corresponding to the dominant
            eigenvalue of A.
    """
    m, n = A.shape
    x = np.random.random(n)
    x = x / la.norm(x)
    x_2 = x
    for k in range(N):
       x_1 = x_2     
       x_2 = np.dot(A, x_2)
       if la.norm(x_2 - x_1) < tol:
           break
       x_2 = x_2 / la.norm(x_2)

    return np.dot(x_1.T, np.dot(A, x_1)), x_1



# Problem 6
def qr_algorithm(A, N=50, tol=1e-12):
    """Compute the eigenvalues of A via the QR algorithm.

    Parameters:
        A ((n,n) ndarray): A square matrix.
        N (int): The number of iterations to run the QR algorithm.
        tol (float): The threshold value for determining if a diagonal S_i
            block is 1x1 or 2x2.

    Returns:
        ((n,) ndarray): The eigenvalues of A.
    """
    m, n = A.shape
    S = la.hessenberg(A)
    for k in range(N):
        Q, R = la.qr(S)
        S = np.dot(R, Q)

    eigs = []
    i = 0
    while i < n:
        if (S[i,i] == S[n-1,n-1]) or (abs(S[i+1, i]) < tol):
            eigs.append(S[i,i])
        else:
            a = 1
            b = -1 * (S[i,i] + S[i+1,i+1])
            c = (S[i][i] * S[i+1,i+1]) - (S[i+1,i] * S[i,i+1])
            eigs.append((-b / (2 * a) + cmath.sqrt(b**2 - (4 * a * c)) / (2 * a)))
            eigs.append((-b / (2 * a) - cmath.sqrt(b**2 - (4 * a * c)) / (2 * a)))
            i += 1
        i += 1

    return eigs


"""if __name__ == "__main__":
    A = np.random.randint(10, size=(3,3))
    print(A, qr_algorithm(A))"""