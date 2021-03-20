# newtons_method.py
"""Volume 1: Newton's Method.
<Name>
<Class>
<Date>
"""
import numpy as np
from matplotlib import pyplot as plt
import autograd
from autograd import numpy as anp
from scipy import linalg as la
# Problems 1, 3, and 5
def newton(f, x0, Df, tol=1e-5, maxiter=15, alpha=1.):
    """Use Newton's method to approximate a zero of the function f.

    Parameters:
        f (function): a function from R^n to R^n (assume n=1 until Problem 5).
        x0 (float or ndarray): The initial guess for the zero of f.
        Df (function): The derivative of f, a function from R^n to R^(nxn).
        tol (float): Convergence tolerance. The function should returns when
            the difference between successive approximations is less than tol.
        maxiter (int): The maximum number of iterations to compute.
        alpha (float): Backtracking scalar (Problem 3).

    Returns:
        (float or ndarray): The approximation for a zero of f.
        (bool): Whether or not Newton's method converged.
        (int): The number of iterations computed.
    """
    if np.isscalar(x0):
        converge = False
        totalIter = 0
        for k in range(maxiter):
            totalIter += 1
            x1 = x0 - alpha*(f(x0) / Df(x0))
            if abs(x1 - x0) < tol:
                converge = True
                break
            x0 = x1
        return x0, converge, totalIter

    else:
        converge = False
        totalIter = 0
        for k in range(maxiter):
            totalIter += 1
            y = la.solve(Df(x0), f(x0))
            x1 = x0 - alpha*y
            if la.norm(x1 - x0) < tol:
                converge = True
                break
            x0 = x1
        return x0, converge, totalIter



# Problem 2
def prob2(N1, N2, P1, P2):
    """Use Newton's method to solve for the constant r that satisfies

                P1[(1+r)**N1 - 1] = P2[1 - (1+r)**(-N2)].

    Use r_0 = 0.1 for the initial guess.

    Parameters:
        P1 (float): Amount of money deposited into account at the beginning of
            years 1, 2, ..., N1.
        P2 (float): Amount of money withdrawn at the beginning of years N1+1,
            N1+2, ..., N1+N2.
        N1 (int): Number of years money is deposited.
        N2 (int): Number of years money is withdrawn.

    Returns:
        (float): the value of r that satisfies the equation.
    """
    r0 = 0.1
    f = lambda r : P1*((1 + r)**N1 - 1) - P2*(1 - (1+r)**-N2)
    Df = lambda r : P1*(N1*(1+r)**(N1-1)) - P2*(N2*(1+r)**(-N2 - 1))
    approx, converge, iter = newton(f, r0, Df)

    return approx


# Problem 4
def optimal_alpha(f, x0, Df, tol=1e-5, maxiter=15):
    """Run Newton's method for various values of alpha in (0,1].
    Plot the alpha value against the number of iterations until convergence.

    Parameters:
        f (function): a function from R^n to R^n (assume n=1 until Problem 5).
        x0 (float or ndarray): The initial guess for the zero of f.
        Df (function): The derivative of f, a function from R^n to R^(nxn).
        tol (float): Convergence tolerance. The function should returns when
            the difference between successive approximations is less than tol.
        maxiter (int): The maximum number of iterations to compute.

    Returns:
        (float): a value for alpha that results in the lowest number of
            iterations.
    """
    domain = np.linspace(0.01, 1, 50)
    alphaVals = []
    convergeVals = []
    bestAlpha = 0
    iter = 15
    for alpha in domain:
        approx, converge, newIter = newton(f, x0, Df, alpha=alpha)
        alphaVals.append(alpha)
        convergeVals.append(newIter)
        if newIter < iter:
            bestAlpha = alpha
            iter = newIter

    plt.plot(convergeVals, alphaVals, marker='o')
    plt.xlabel("number of iterations")
    plt.ylabel("alpha")
    plt.show()
    
    return bestAlpha


# Problem 6
def prob6():
    """Consider the following Bioremediation system.

                              5xy − x(1 + y) = 0
                        −xy + (1 − y)(1 + y) = 0

    Find an initial point such that Newton’s method converges to either
    (0,1) or (0,−1) with alpha = 1, and to (3.75, .25) with alpha = 0.55.
    Return the intial point as a 1-D NumPy array with 2 entries.
    """
    f = lambda x : np.array([5*x[0] * x[1] - x[0] * (1 + x[1]), -x[0] * x[1] + (1 - x[1])*(1 + x[1])])
    Df = lambda x : np.array(([5*x[1] - (1 + x[1]), 5*x[0] - x[0]], [-x[1], -x[0] + 2*x[1]]))

    alpha2 = 0.55
    alpha1 = 1

    xdomain = np.linspace(-1/4, 0, 10)
    ydomain = np.linspace(0, 1/4, 10)
    
    for x in xdomain:
        for y in ydomain:
            approx1 = newton(f, np.array((x, y)), Df, alpha=alpha1)[0]

            if np.allclose(np.array((0, 1)), approx1) or np.allclose(np.array((0, -1)), approx1):

                approx2 = newton(f, np.array((x, y)), Df, alpha=alpha2)[0]

                if la.norm(np.array((3.75, 0.25)) - approx2) < 0.01:
                    return np.array((x, y))


# Problem 7
def plot_basins(f, Df, zeros, domain, res=1000, iters=15):
    """Plot the basins of attraction of f on the complex plane.

    Parameters:
        f (function): A function from C to C.
        Df (function): The derivative of f, a function from C to C.
        zeros (ndarray): A 1-D array of the zeros of f.
        domain ([r_min, r_max, i_min, i_max]): A list of scalars that define
            the window limits and grid domain for the plot.
        res (int): A scalar that determines the resolution of the plot.
            The visualized grid has shape (res, res).
        iters (int): The exact number of times to iterate Newton's method.
    """
    x_real = np.linspace(domain[0], domain[1], res)
    x_imag = np.linspace(domain[2], domain[3], res)
    X_real, X_imag = np.meshgrid(x_real, x_imag)
    X_0 = X_real + 1j*X_imag
    
    for k in range(iters):
        X_1 = X_0 - f(X_0)/Df(X_0)
        X_0 = X_1

    Y = np.zeros((res, res))
    for i in range(res):
        for j in range(res):
            Y[i, j] = np.argmin(np.abs(zeros - X_0[i, j]))
    
    
    plt.pcolormesh(X_real, X_imag, Y, cmap="brg", shading='nearest')
    plt.show()





