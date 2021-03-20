# differentiation.py
"""Volume 1: Differentiation.
<Name>
<Class>
<Date>
"""
import sympy as sy
from matplotlib import pyplot as plt
import numpy as np
from autograd import numpy as anp
from autograd import grad
from autograd import elementwise_grad
from time import time


# Problem 1
def prob1():
    """Return the derivative of (sin(x) + 1)^sin(cos(x)) using SymPy."""
    x = sy.symbols('x')
    expr = (sy.sin(x) + 1) ** sy.sin(sy.cos(x))
    f = sy.lambdify(x, expr, "numpy")
    diff_expr = sy.diff(expr)
    fprime = sy.lambdify(x, diff_expr, "numpy")

    """domain = np.linspace(-1 * np.pi, np.pi, 200)
    plt.plot(domain, f(domain), label="f(x)")
    plt.plot(domain, fprime(domain), label="f'(x)")


    ax = plt.gca()
    ax.spines["bottom"].set_position("zero")

    plt.legend()
    plt.show() """

    return fprime



# Problem 2
def fdq1(f, x, h=1e-5):
    """Calculate the first order forward difference quotient of f at x."""
    return (f(x + h) - f(x)) / h

def fdq2(f, x, h=1e-5):
    """Calculate the second order forward difference quotient of f at x."""
    return (-3 * f(x) + 4 * f(x + h) - f(x + 2 * h)) / (2 * h)

def bdq1(f, x, h=1e-5):
    """Calculate the first order backward difference quotient of f at x."""
    return (f(x) - f(x - h)) / h

def bdq2(f, x, h=1e-5):
    """Calculate the second order backward difference quotient of f at x."""
    return (3 * f(x) - 4 * f(x - h) + f(x - 2*h)) / (2 * h)

def cdq2(f, x, h=1e-5):
    """Calculate the second order centered difference quotient of f at x."""
    return (f(x + h) - f(x - h)) / (2*h)

def cdq4(f, x, h=1e-5):
    """Calculate the fourth order centered difference quotient of f at x."""
    return (f(x - 2*h) - 8 * f(x - h) + 8 * f(x + h) - f(x + 2*h)) / (12 * h)


# Problem 3
def prob3(x0):
    """Let f(x) = (sin(x) + 1)^(sin(cos(x))). Use prob1() to calculate the
    exact value of f'(x0). Then use fdq1(), fdq2(), bdq1(), bdq2(), cdq1(),
    and cdq2() to approximate f'(x0) for h=10^-8, 10^-7, ..., 10^-1, 1.
    Track the absolute error for each trial, then plot the absolute error
    against h on a log-log scale.

    Parameters:
        x0 (float): The point where the derivative is being approximated.
    """
    x = sy.symbols('x')
    expr = (sy.sin(x) + 1) ** sy.sin(sy.cos(x))
    f = sy.lambdify(x, expr, "numpy")
    fx0 = prob1()(x0)
    domain = np.logspace(-8, 0, 9)

    plt.loglog(domain, np.abs(fx0 - fdq1(f, x0, domain)), label="Order 1 Forward", marker='o')
    plt.loglog(domain, np.abs(fx0 - fdq2(f, x0, domain)), label="Order 2 Forward", marker='o')
    plt.loglog(domain, np.abs(fx0 - bdq1(f, x0, domain)), label="Order 1 Backward", marker='o')
    plt.loglog(domain, np.abs(fx0 - bdq2(f, x0, domain)), label="Order 2 Backward", marker='o')
    plt.loglog(domain, np.abs(fx0 - cdq2(f, x0, domain)), label="Order 2 Centered", marker='o')
    plt.loglog(domain, np.abs(fx0 - cdq4(f, x0, domain)), label="Order 4 Centered", marker='o')

    plt.xlabel("h")
    plt.ylabel("Absolute Error")
    plt.legend()
    plt.show()


# Problem 4
def prob4():
    """The radar stations A and B, separated by the distance 500m, track a
    plane C by recording the angles alpha and beta at one-second intervals.
    Your goal, back at air traffic control, is to determine the speed of the
    plane.

    Successive readings for alpha and beta at integer times t=7,8,...,14
    are stored in the file plane.npy. Each row in the array represents a
    different reading; the columns are the observation time t, the angle
    alpha (in degrees), and the angle beta (also in degrees), in that order.
    The Cartesian coordinates of the plane can be calculated from the angles
    alpha and beta as follows.

    x(alpha, beta) = a tan(beta) / (tan(beta) - tan(alpha))
    y(alpha, beta) = (a tan(beta) tan(alpha)) / (tan(beta) - tan(alpha))

    Load the data, convert alpha and beta to radians, then compute the
    coordinates x(t) and y(t) at each given t. Approximate x'(t) and y'(t)
    using a first order forward difference quotient for t=7, a first order
    backward difference quotient for t=14, and a second order centered
    difference quotient for t=8,9,...,13. Return the values of the speed at
    each t.
    """
    f = lambda x, y : np.sqrt(x**2, y**2)
    data = np.load("plane.npy")
    print(data)
    a = np.deg2rad(data[:, 1])
    b = np.deg2rad(data[:, 2])
    h = 1
    print(a)
    x = a * np.tan(b) / (np.tan(b) - np.tan(a))
    y = a * ((np.tan(b) * np.tan(a)) / (np.tan(b) - np.tan(a)))

    x_prime = x.copy()
    y_prime = y.copy()
    

    x_prime[0] = (x[0 + h] - x[0]) / h
    y_prime[0] = (y[0 + h] - y[0]) / h
    for i in range(1, len(x) - 1):
        print("i=", i + 7, i)
        x_prime[i] = (x[i + h] - x[i - h]) / (2 * h)
        y_prime[i] = (y[i + h] - y[i - h]) / (2 * h)

    x_prime[-1] = (x[-1] - x[-1 - h]) / h
    y_prime[-1] = (y[-1] - y[-1 - h]) / h

    speeds = np.sqrt(np.square(x_prime)+ np.square(y_prime))


    return speeds


# Problem 5
def jacobian_cdq2(f, x, h=1e-5):
    """Approximate the Jacobian matrix of f:R^n->R^m at x using the second
    order centered difference quotient.

    Parameters:
        f (function): the multidimensional function to differentiate.
            Accepts a NumPy (n,) ndarray and returns an (m,) ndarray.
            For example, f(x,y) = [x+y, xy**2] could be implemented as follows.
            >>> f = lambda x: np.array([x[0] + x[1], x[0] * x[1]**2])
        x ((n,) ndarray): the point in R^n at which to compute the Jacobian.
        h (float): the step size in the finite difference quotient.

    Returns:
        ((m,n) ndarray) the Jacobian matrix of f at x.
    """
    n = len(x)
    m = len(f(x))
    I = np.eye(n)
    

    solution = np.zeros((m, n))

    for i in range(n):
        solution[:,i] = (f(x + h * I[:,i]) - f(x - h * I[:,i])) / (2*h)

    return solution




# Problem 6
def cheb_poly(x, n):
    """Compute the nth Chebyshev polynomial at x.

    Parameters:
        x (autograd.ndarray): the points to evaluate T_n(x) at.
        n (int): The degree of the polynomial.
    """
    T0 = anp.ones_like(x)
    T1 = x
    def _poly(x, n):
        if n == 1:
            return x
        if n == 0:
            return anp.ones_like(x)
        return 2 * x * _poly(x, n-1) - _poly(x, n-2)
        
    return _poly(x, n)

def prob6():
    """Use Autograd and cheb_poly() to create a function for the derivative
    of the Chebyshev polynomials, and use that function to plot the derivatives
    over the domain [-1,1] for n=0,1,2,3,4.
    """
    x = anp.linspace(-1, 1, 100)
    g = lambda x, n : cheb_poly(x, n)

    dg = elementwise_grad(g)
    
    
    plt.plot(x, dg(x, 0), label="DT0")
    plt.plot(x, dg(x, 1), label="DT1")
    plt.plot(x, dg(x, 2), label="DT2")
    plt.plot(x, dg(x, 3), label="DT3")
    plt.plot(x, dg(x, 4), label="DT4")

    plt.legend()
    plt.show()



# Problem 7
def prob7(N=200):
    """Let f(x) = (sin(x) + 1)^sin(cos(x)). Perform the following experiment N
    times:

        1. Choose a random value x0.
        2. Use prob1() to calculate the “exact” value of f′(x0). Time how long
            the entire process takes, including calling prob1() (each
            iteration).
        3. Time how long it takes to get an approximation of f'(x0) using
            cdq4(). Record the absolute error of the approximation.
        4. Time how long it takes to get an approximation of f'(x0) using
            Autograd (calling grad() every time). Record the absolute error of
            the approximation.

    Plot the computation times versus the absolute errors on a log-log plot
    with different colors for SymPy, the difference quotient, and Autograd.
    For SymPy, assume an absolute error of 1e-18.
    """
    x = sy.symbols('x')
    expr = (sy.sin(x) + 1) ** sy.sin(sy.cos(x))
    f = sy.lambdify(x, expr, "numpy")
    f0 = lambda x : (anp.sin(x) + 1) ** anp.sin(anp.cos(x)) 
    symptime = []
    difftime = []
    autotime = []

    symperror = []
    differror = []
    autoerror = []

    for i in range(N):
        x = 10 * np.random.normal()
        start = time()
        exact = prob1()(x)
        symptime.append(time() - start)
        symperror.append(1e-18)

        start = time()
        approx = cdq4(f, x)
        difftime.append(time() - start)
        differror.append(np.abs(approx - exact))

        start = time()
        df = grad(f0)
        approx = df(x)
        autotime.append(time() - start)
        autoerror.append(np.abs(approx - exact))

    plt.loglog(symptime, symperror, 'o', label="SymPy")
    plt.loglog(difftime, differror, 'o', label="Difference Quotient")
    plt.loglog(autotime, autoerror, 'o', label="Autograd")

    plt.xlabel("Time")
    plt.ylabel("Absolute Error")
    plt.legend()
    plt.show()




