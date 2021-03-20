# condition_stability.py
"""Volume 1: Conditioning and Stability.
<Name>
<Class>
<Date>
"""

import numpy as np
import sympy as sy
import scipy as sp
from scipy import linalg as la
from matplotlib import pyplot as plt


# Problem 1
def matrix_cond(A):
    """Calculate the condition number of A with respect to the 2-norm."""
    vals = la.svdvals(A)
    a_max = vals[0]
    a_min = vals[-1]
    if a_min == 0:
        return np.inf
    
    return a_max / a_min


# Problem 2
def prob2():
    """Randomly perturb the coefficients of the Wilkinson polynomial by
    replacing each coefficient c_i with c_i*r_i, where r_i is drawn from a
    normal distribution centered at 1 with standard deviation 1e-10.
    Plot the roots of 100 such experiments in a single figure, along with the
    roots of the unperturbed polynomial w(x).

    Returns:
        (float) The average absolute condition number.
        (float) The average relative condition number.
    """
    w_roots = np.arange(1, 21)
    abs_condition = 0
    rel_condition = 0
    # Get the exact Wilkinson polynomial coefficients using SymPy.
    x, i = sy.symbols('x i')
    w = sy.poly_from_expr(sy.product(x-i, (i, 1, 20)))[0]
    w_coeffs = np.array(w.all_coeffs())
    points = np.ones(20)
    for n in range(100):
        r_i = np.random.normal(1, 1e-10, size=w_roots.size + 1)
        perturb = w_coeffs * r_i
        
        new_roots = np.roots(np.poly1d(perturb))
        if n == 0:
            points = new_roots
        else:
            points = np.concatenate((points, new_roots))
        w_roots, new_roots = np.sort(w_roots), np.sort(new_roots)

        k = la.norm(new_roots - w_roots, np.inf) / la.norm(r_i, np.inf)
        rel = k * la.norm(w_coeffs, np.inf) / la.norm(w_roots, np.inf)

        abs_condition += (k - abs_condition) / (n+1)
        rel_condition += (rel - rel_condition) / (n+1)

    plt.scatter(np.real(w_roots), np.imag(w_roots), label="Original")
    plt.scatter(np.real(points), np.imag(points), 1, label="Perturbed", marker=',', color='k')
    plt.legend()
    plt.show()

    return abs_condition, rel_condition
        


# Problem 3
def eig_cond(A):
    """Approximate the condition numbers of the eigenvalue problem at A.

    Parameters:
        A ((n,n) ndarray): A square matrix.

    Returns:
        (float) The absolute condition number of the eigenvalue problem at A.
        (float) The relative condition number of the eigenvalue problem at A.
    """
    real = np.random.normal(0, 1e-10, A.shape)
    imag = np.random.normal(0, 1e-10, A.shape)
    H = real + 1j*imag

    lamb = la.eigvals(A)
    lamb_line = la.eigvals(A + H)

    abs_condition = la.norm(lamb - lamb_line, 2) / la.norm(H, 2)
    rel_condition = abs_condition * la.norm(A, 2) / la.norm(lamb, 2)

    return abs_condition, rel_condition


# Problem 4
def prob4(domain=[-100, 100, -100, 100], res=50):
    """Create a grid [x_min, x_max] x [y_min, y_max] with the given resolution. For each
    entry (x,y) in the grid, find the relative condition number of the
    eigenvalue problem, using the matrix   [[1, x], [y, 1]]  as the input.
    Use plt.pcolormesh() to plot the condition number over the entire grid.

    Parameters:
        domain ([x_min, x_max, y_min, y_max]):
        res (int): number of points along each edge of the grid.
    """
    x = np.linspace(domain[0], domain[1], res)
    y = np.linspace(domain[2], domain[3], res)

    X = np.zeros((res, res))
    
    for i in range(res - 1):
        for j in range(res - 1):
            
            M = np.array(([1, x[i]],[y[j], 1]))
            ab, rel = eig_cond(M)
            
            X[i][j] = rel

    plt.pcolormesh(x, y, X, cmap='gray_r', shading='nearest')
    plt.show()


# Problem 5
def prob5(n):
    """Approximate the data from "stability_data.npy" on the interval [0,1]
    with a least squares polynomial of degree n. Solve the least squares
    problem using the normal equation and the QR decomposition, then compare
    the two solutions by plotting them together with the data. Return
    the mean squared error of both solutions, ||Ax-b||_2.

    Parameters:
        n (int): The degree of the polynomial to be used in the approximation.

    Returns:
        (float): The forward error using the normal equations.
        (float): The forward error using the QR decomposition.
    """
    xk, yk = np.load('stability_data.npy').T
    A = np.vander(xk, n+1)

    x1 = la.inv(A.T @ A) @ A.T @ yk

    Q, R = la.qr(A, mode='economic')
    x2 = la.solve_triangular(R, Q.T@yk)

    err1 = la.norm(A@x1 - yk, 2)
    err2 = la.norm(A@x2 - yk, 2)
    domain = np.linspace(0, 1, xk.size)
    plt.scatter(domain, yk, label="data", s=15)
    plt.plot(domain, np.polyval(x1, domain), label="la.inv()", color='green')
    plt.plot(domain, np.polyval(x2, domain), label="la.solve_triangular()", color='orange')

    plt.legend()
    plt.show()

    return err1, err2


# Problem 6
def prob6():
    """For n = 5, 10, ..., 50, compute the integral I(n) using SymPy (the
    true values) and the subfactorial formula (may or may not be correct).
    Plot the relative forward error of the subfactorial formula for each
    value of n. Use a log scale for the y-axis.
    """
    x, n1 = sy.symbols('x n1')
    expr2 = (-1)**n1*(sy.subfactorial(n1) - (sy.factorial(n1) / np.e))

    domain = np.arange(5, 51, 5)
    exact_vals = np.zeros(domain.size)
    approx_sy = np.zeros(domain.size)
    i=0
    for n in range(5, 51, 5):
        expr = x**n * sy.exp(x-1)
        exact_vals[i] = sy.integrate(expr, (x, 0, 1))
        
        approx_sy[i] = expr2.subs(n1, n)
        i += 1
    forward_error = np.abs(exact_vals - approx_sy) / np.abs(exact_vals)

    plt.plot(domain, forward_error)
    plt.yscale('log')
    plt.show()








