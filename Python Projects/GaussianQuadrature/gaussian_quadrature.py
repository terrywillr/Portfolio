# quassian_quadrature.py
"""Volume 2: Gaussian Quadrature.
<Name>
<Class>
<Date>
"""
import numpy as np
from scipy import linalg as la;
from scipy.integrate import quad
from scipy.integrate import nquad
from scipy.stats import norm
from matplotlib import pyplot as plt


class GaussianQuadrature:
    """Class for integrating functions on arbitrary intervals using Gaussian
    quadrature with the Legendre polynomials or the Chebyshev polynomials.
    """
    # Problems 1 and 3
    def __init__(self, n, polytype="legendre"):
        """Calculate and store the n points and weights corresponding to the
        specified class of orthogonal polynomial (Problem 3). Also store the
        inverse weight function w(x)^{-1} = 1 / w(x).

        Parameters:
            n (int): Number of points and weights to use in the quadrature.
            polytype (string): The class of orthogonal polynomials to use in
                the quadrature. Must be either 'legendre' or 'chebyshev'.

        Raises:
            ValueError: if polytype is not 'legendre' or 'chebyshev'.
        """
        # Check to see if polytype is legendre or chebyshev
        self.type = polytype
        self.n = n
        if self.type != "legendre" and self.type != "chebyshev":
            raise ValueError("polytype must be legendre or chebyshev")

        # Define w(x)^-1 depending on type of polynomials
        if self.type == "legendre":
            self.reciprocal = lambda x : 1
        if self.type == "chebyshev":
            self.reciprocal = lambda x : np.sqrt(1 - x**2)

        
        # Calculate the points and weights used for Gaussian Quadrature.
        self.points, self.weights = self.points_weights(n)

    # Problem 2
    def points_weights(self, n):
        """Calculate the n points and weights for Gaussian quadrature.

        Parameters:
            n (int): The number of desired points and weights.

        Returns:
            points ((n,) ndarray): The sampling points for the quadrature.
            weights ((n,) ndarray): The weights corresponding to the points.
        """
        if self.type == "legendre":
            # Calculate a and b points
            a = np.zeros(n)
            b = np.arange(1, n, 1)
            b = np.square(b) / (4 * np.square(b) - 1)

            # Create the matrix J from points of a and b
            J = np.zeros((n, n))
            for i in range(n - 1):
                J[i+1, i] = np.sqrt(b[i])
                J[i, i+1] = np.sqrt(b[i])

            # Calculate eigvals and eigvectors, apply measure of the weight function
            eigvals, eigvec = np.linalg.eig(J)
            measure = 2
            weights = np.ones(n)
            for i in range(n):
                weights[i] = measure * np.square(eigvec[0][i])

        if self.type == "chebyshev":
            # Same process as for legendre polynomials
            a = np.zeros(n)
            b = 1/4 * np.ones(n)
            b[0] *= 2
            J = np.zeros((n,n))
            for i in range(n - 1):
                J[i+1, i] = np.sqrt(b[i])
                J[i, i+1] = np.sqrt(b[i])

            eigvals, eigvec = np.linalg.eig(J)
            measure = np.pi
            
            weights = np.ones(n)
            for i in range(n):
                weights[i] = measure * np.square(eigvec[0][i])

        # Correctly order eigvectors and eigvalues.
        index = np.argsort(weights)
        return np.real(eigvals)[index], weights[index]


    # Problem 3
    def basic(self, f):
        """Approximate the integral of a f on the interval [-1,1]."""
        # Calculate g(x) = f(x)/w(x) and compute approximation using sum of g(points) * weights.
        g = lambda x : f(x) * self.reciprocal(x)
        return np.sum(g(self.points) * self.weights)

    # Problem 4
    def integrate(self, f, a, b):
        """Approximate the integral of a function on the interval [a,b].

        Parameters:
            f (function): Callable function to integrate.
            a (float): Lower bound of integration.
            b (float): Upper bound of integration.

        Returns:
            (float): Approximate value of the integral.
        """
        # Use a and b to redefine the function f(x) and approximate the integral on the new function
        h = lambda x : f((b - a) / 2 * x + (a + b) / 2)
        return (b - a) / 2 * self.basic(h)

    # Problem 6.
    def integrate2d(self, f, a1, b1, a2, b2):
        """Approximate the integral of the two-dimensional function f on
        the interval [a1,b1]x[a2,b2].

        Parameters:
            f (function): A function to integrate that takes two parameters.
            a1 (float): Lower bound of integration in the x-dimension.
            b1 (float): Upper bound of integration in the x-dimension.
            a2 (float): Lower bound of integration in the y-dimension.
            b2 (float): Upper bound of integration in the y-dimension.

        Returns:
            (float): Approximate value of the integral.
        """
        # Redefine f(x) to h(x) using the points a1, b1, a2, b2 and calculate g(x,y) = h(x,y) / w(x)w(y)
        h = lambda x, y : f((b1 - a1) / 2 * x + (a1 + b1) / 2, (b2 - a2) / 2 * y + (a2 + b2) / 2)
        g = lambda x, y : h(x, y) * (self.reciprocal(x) * self.reciprocal(y))

        # Calculate the approximation by taking the double sum of wi*wj*g(zi, zj)
        out = 0
        for i in range(self.n):
            for j in range(self.n):
                out += ((b1 - a1) * (b2 - a2)) / 4 * self.weights[i] * self.weights[j] * g(self.points[i], self.points[j])

        return  out


# Problem 5
def prob5():
    """Use scipy.stats to calculate the "exact" value F of the integral of
    f(x) = (1/sqrt(2 pi))e^((-x^2)/2) from -3 to 2. Then repeat the following
    experiment for n = 5, 10, 15, ..., 50.
        1. Use the GaussianQuadrature class with the Legendre polynomials to
           approximate F using n points and weights. Calculate and record the
           error of the approximation.
        2. Use the GaussianQuadrature class with the Chebyshev polynomials to
           approximate F using n points and weights. Calculate and record the
           error of the approximation.
    Plot the errors against the number of points and weights n, using a log
    scale for the y-axis. Finally, plot a horizontal line showing the error of
    scipy.integrate.quad() (which doesn’t depend on n).
    """
    # Calculate the exact value of the cdf
    exact = norm.cdf(2) - norm.cdf(-3)

    # Create values of n to use and initialize lists for errors
    nums = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    leg_err = []
    cheb_err = []
    sci_err = []

    # define our cdf function
    f = lambda x : 1 / np.sqrt(2 * np.pi) * np.exp(-1 * x**2 / 2)

    
    for n in nums:
        legendre = GaussianQuadrature(n, polytype="legendre")
        cheby = GaussianQuadrature(n, polytype="chebyshev")

        # Calculate errors for each method of approximation and put in lists
        leg_err.append(np.abs(exact - legendre.integrate(f, -2, 3)))
        cheb_err.append(np.abs(exact - cheby.integrate(f, -2, 3)))
        sci_err.append(np.abs(exact - quad(f, -2, 3)[0]))

    # Plot errors against number of points and weights used
    plt.plot(nums, leg_err, label="Legendre")
    plt.plot(nums, cheb_err, label="Chebyshev")
    plt.plot(nums, sci_err, label="SciPy")

    plt.yscale('log')
    plt.xlabel("Number of Points")
    plt.ylabel("Error")
    plt.legend()
    plt.show()






