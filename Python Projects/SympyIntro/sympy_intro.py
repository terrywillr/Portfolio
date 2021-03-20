# sympy_intro.py
"""Python Essentials: Introduction to SymPy.
<Name>
<Class>
<Date>
"""
import sympy as sy
import numpy as np
from matplotlib import pyplot as plt

# Problem 1
def prob1():
    """Return an expression for

        (2/5)e^(x^2 - y)cosh(x+y) + (3/7)log(xy + 1).

    Make sure that the fractions remain symbolic.
    """
    y = sy.symbols('y')
    x = sy.symbols('x')

    return sy.Rational(2, 5) * sy.E ** (x ** 2 - y) * sy.cosh(x + y) + sy.Rational(3, 7) * sy.log(x * y + 1)


# Problem 2
def prob2():
    """Compute and simplify the following expression.

        product_(i=1 to 5)[ sum_(j=i to 5)[j(sin(x) + cos(x))] ]
    """
    x = sy.symbols('x')
    i = sy.symbols('i')
    j = sy.symbols('j')


    return sy.simplify(sy.product(sy.summation(j * (sy.sin(x) + sy.cos(x)), (j, i, 5)), (i, 1, 5)))


# Problem 3
def prob3(N):
    """Define an expression for the Maclaurin series of e^x up to order N.
    Substitute in -y^2 for x to get a truncated Maclaurin series of e^(-y^2).
    Lambdify the resulting expression and plot the series on the domain
    y in [-3,3]. Plot e^(-y^2) over the same domain for comparison.
    """
    domain = np.linspace(-2, 2, 100)


    x = sy.symbols('x')
    n = sy.symbols('n')
    y = sy.symbols('y')
    
    sym = sy.summation(x**n / sy.factorial(n), (n, 0, N))
    new_expr = sym.subs({x: -1 * y**2})
    
    f = lambda n : np.exp(-1 * n**2)
    g = sy.lambdify(y, new_expr, "numpy")

    plt.plot(domain, f(domain), label="function")
    plt.plot(domain, g(domain), label="series")

    plt.legend()
    plt.show()
    


# Problem 4
def prob4():
    """The following equation represents a rose curve in cartesian coordinates.

    0 = 1 - [(x^2 + y^2)^(7/2) + 18x^5 y - 60x^3 y^3 + 18x y^5] / (x^2 + y^2)^3

    Construct an expression for the nonzero side of the equation and convert
    it to polar coordinates. Simplify the result, then solve it for r.
    Lambdify a solution and use it to plot x against y for theta in [0, 2pi].
    """
    x = sy.symbols('x')
    y = sy.symbols('y')
    r = sy.symbols('r')
    th = sy.symbols('theta')
    
    expr = 1 - ((x**2 + y**2)**sy.Rational(7, 2) + 18 * x**5 * y - 60 * x**3 * y**3 + 18 * x * y**5) / (x**2 + y**2)**3

    new_expr = expr.subs({x:r * sy.cos(th), y:r * sy.sin(th)})
    simple = sy.simplify(new_expr)

    solved = sy.solve(simple, r)

    f = sy.lambdify(th, solved[0] * sy.cos(th), "numpy")
    g = sy.lambdify(th, solved[0] * sy.sin(th), "numpy")

    domain = np.linspace(0, 2 * np.pi, 100)


    plt.plot(f(domain), g(domain))

    plt.show()
    

# Problem 5
def prob5():
    """Calculate the eigenvalues and eigenvectors of the following matrix.

            [x-y,   x,   0]
        A = [  x, x-y,   x]
            [  0,   x, x-y]

    Returns:
        (dict): a dictionary mapping eigenvalues (as expressions) to the
            corresponding eigenvectors (as SymPy matrices).
    """
    x, y, lamb = sy.symbols('x y lambda')
    A = sy.Matrix(([x - y, x, 0],
                  [x, x - y, x],
                  [0, x, x - y]))

    I = sy.eye(3)

    eigvals = sy.solve((A - lamb * I).det(), lamb)
    eigvectors = [(A - eig * I).nullspace() for eig in eigvals]

    out = {eigvals[i] : eigvectors[i] for i in range(len(eigvals))}
    return out

                            

# Problem 6
def prob6():
    """Consider the following polynomial.

        p(x) = 2*x^6 - 51*x^4 + 48*x^3 + 312*x^2 - 576*x - 100

    Plot the polynomial and its critical points. Determine which points are
    maxima and which are minima.

    Returns:
        (set): the local minima.
        (set): the local maxima.
    """
    x = sy.symbols('x')
    expr = 2 * x**6 - 51 * x**4 + 48 * x**3 + 312 * x**2 - 576 * x - 100
    df = sy.Derivative(expr).doit()
    vals = sy.solve(df, x)

    dff = sy.Derivative(df).doit()
    f = sy.lambdify(x, dff)

    maximum = []
    minimum = []

    for x0 in vals:
        if f(x0) > 0:
            minimum.append(x0)
        elif f(x0) < 0:
            maximum.append(x0)

    g = sy.lambdify(x, expr)
    ymax = []
    ymin = []

    for x in maximum:
        ymax.append(g(x))

    for x in minimum:
        ymin.append(g(x))
    
    domain = np.linspace(-5, 5, 100)
    plt.plot(domain, g(domain), label="p(x)")
    plt.plot(maximum, ymax, 'o', color='red', label="local maxima")
    plt.plot(minimum, ymin, 'o', color='black', label="local minima")

    plt.legend()
    plt.show()


    return set(minimum), set(maximum)


# Problem 7
def prob7():
    """Calculate the integral of f(x,y,z) = (x^2 + y^2 + z^2)^2 over the
    sphere of radius r. Lambdify the resulting expression and plot the integral
    value for r in [0,3]. Return the value of the integral when r = 2.

    Returns:
        (float): the integral of f over the sphere of radius 2.
    """
    x, y, z, p, theta, phi, r = sy.symbols('x y z p theta phi r')
    expr = (x**2 + y**2 + z**2)**2
    new_expr = expr.subs({x:p * sy.sin(phi) * sy.cos(theta), y:p * sy.sin(phi) * sy.sin(theta), z:p * sy.cos(phi)})
    h = sy.Matrix(([p * sy.sin(phi) * sy.cos(theta)],
                   [p * sy.sin(phi) * sy.sin(theta)],
                   [p * sy.cos(phi)]))
    J = h.jacobian([p, theta, phi])

    integral = sy.integrate(sy.integrate(sy.integrate(new_expr * -1 * J.det(), (p, 0, r)), (theta, 0, 2 * sy.pi)), (phi, 0, sy.pi))
    simple = sy.simplify(integral)
    f = sy.lambdify(r, simple, "numpy")
    domain = np.linspace(0, 3, 100)

    plt.plot(domain, f(domain))
    plt.show()

    return f(2)



