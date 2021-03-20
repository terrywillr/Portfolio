# polynomial_interpolation.py
"""Volume 2: Polynomial Interpolation.
<Name>
<Class>
<Date>
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import BarycentricInterpolator
from scipy import linalg as la
from numpy.fft import fft
# Problems 1 and 2
def lagrange(xint, yint, points):
    """Find an interpolating polynomial of lowest degree through the points
    (xint, yint) using the Lagrange method and evaluate that polynomial at
    the specified points.

    Parameters:
        xint ((n,) ndarray): x values to be interpolated.
        yint ((n,) ndarray): y values to be interpolated.
        points((m,) ndarray): x values at which to evaluate the polynomial.

    Returns:
        ((m,) ndarray): The value of the polynomial at the specified points.
    """
    n = len(xint)
    m = len(points)
    denominators = np.ones(n)
    # create the denominator values for each Lj
    for j in range(n):
        denominators[j] = np.product(xint[j] - np.delete(xint, j))

    evaluated = np.ones((n, m))
    # Create an n*m matrix containing Lj for each point in the domain
    for j in range(n):
        L = np.ones(m)
        for k in range(m):
            L[k] = np.product(points[k] - np.delete(xint, j)) / denominators[j]
        evaluated[j, :] = L
    # Evaluate the interpolating polynomial at each point in the domain.
    p = np.ones(m)
    for k in range(m):
        p[k] = np.sum(yint * evaluated[:,k])

    return p

        


# Problems 3 and 4
class Barycentric:
    """Class for performing Barycentric Lagrange interpolation.

    Attributes:
        w ((n,) ndarray): Array of Barycentric weights.
        n (int): Number of interpolation points.
        x ((n,) ndarray): x values of interpolating points.
        y ((n,) ndarray): y values of interpolating points.
    """

    def __init__(self, xint, yint):
        """Calculate the Barycentric weights using initial interpolating points.

        Parameters:
            xint ((n,) ndarray): x values of interpolating points.
            yint ((n,) ndarray): y values of interpolating points.
        """
        self.n = len(xint)
        self.x = xint
        self.y = yint
        self.w = np.ones(self.n)
        # Calculate Capcity of the interval
        C = (np.max(xint) - np.min(xint)) / 4
        shuffle = np.random.permutation(self.n - 1)

        # Evaluate the weights using a random order to evaluate the product
        for j in range(self.n):
            temp = (xint[j] - np.delete(xint, j)) / C
            temp = temp[shuffle]
            self.w[j] /= np.product(temp)


    def __call__(self, points):
        """Using the calcuated Barycentric weights, evaluate the interpolating polynomial
        at points.

        Parameters:
            points ((m,) ndarray): Array of points at which to evaluate the polynomial.

        Returns:
            ((m,) ndarray): Array of values where the polynomial has been computed.
        """
        eval = np.ones(len(points))
        for k in range(len(points)):
            eval[k] = np.sum((self.w * self.y) / (points[k] - self.x)) / np.sum(self.w / (points[k] - self.x))
        
        return eval

    # Problem 4
    def add_weights(self, xint, yint):
        """Update the existing Barycentric weights using newly given interpolating points
        and create new weights equal to the number of new points.

        Parameters:
            xint ((m,) ndarray): x values of new interpolating points.
            yint ((m,) ndarray): y values of new interpolating points.
        """
        m = len(xint)
        C = (np.max(xint) - np.min(xint)) / 4
        new_w = np.ones(m)
        # Find the values of the new weights
        for j in range(m):
            new_w[j] = 1 / np.product((xint[j] - self.x) / C)

        # Reevalute old weights
        for j in range(m):
            for k in range(self.n):
                self.w[k] = C * self.w[k] / (self.x[k] - xint[j])
        # Add the new weights to the class attributes and put them in order.
        self.x = np.concatenate((self.x, xint))
        indices = np.argsort(self.x)
        self.x = np.concatenate((self.x, xint))[indices]
        self.y = np.concatenate((self.y, yint))[indices]
        self.w = np.concatenate((self.w, new_w))[indices]
         


# Problem 5
def prob5():
    """For n = 2^2, 2^3, ..., 2^8, calculate the error of intepolating Runge's
    function on [-1,1] with n points using SciPy's BarycentricInterpolator
    class, once with equally spaced points and once with the Chebyshev
    extremal points. Plot the absolute error of the interpolation with each
    method on a log-log plot.
    """
    f = lambda x : 1 / (1 + 25 * x ** 2)
    domain = np.linspace(-1, 1, 400)
    num = [2, 3, 4, 5, 6, 7, 8]
    nums = [2**i for i in num]
    uniform_error = []
    extreme_error = []
    print(nums)
    for n in nums:
        # Create the interpolating polynomial using uniform points and evaulate the error
        pts = np.linspace(-1, 1, n)
        poly = BarycentricInterpolator(pts, f(pts))
        evaluated = poly._evaluate(domain)
        error = la.norm(f(domain) - evaluated, ord=np.inf)

        # Calculate chebyshev extremal pointss
        j = np.arange(0, n+1)
        cheb_points = np.cos(j * np.pi / n)

        # Calculate the interpolating polynomal using chebyshev extremal points and evaluate the error
        poly2 = BarycentricInterpolator(cheb_points, f(cheb_points))
        evaluated2 = poly2._evaluate(domain)
        error2 = la.norm(f(domain) - evaluated2, ord=np.inf)
        
        uniform_error.append(error)
        extreme_error.append(error2)
    print(uniform_error, extreme_error, sep='\n')
    plt.loglog(nums, uniform_error, label="Uniform points", base=2)
    plt.loglog(nums, extreme_error, label="Chebyshev points", base=2)

    plt.legend()
    plt.show()


# Problem 6
def chebyshev_coeffs(f, n):
    """Obtain the Chebyshev coefficients of a polynomial that interpolates
    the function f at n points.

    Parameters:
        f (function): Function to be interpolated.
        n (int): Number of points at which to interpolate.

    Returns:
        coeffs ((n+1,) ndarray): Chebyshev coefficients for the interpolating polynomial.
    """
    y = np.cos((np.pi * np.arange(2*n)) / n)
    samples = f(y)

    # Use the FFT to evaluate the chebyshev coefficients for an interpolating polynomial.
    coeffs = np.real(fft(samples))[:n+1] / n
    coeffs[0] = coeffs[0] / 2
    coeffs[n] = coeffs[n] / 2

    return coeffs


# Problem 7
def prob7(n):
    """Interpolate the air quality data found in airdata.npy using
    Barycentric Lagrange interpolation. Plot the original data and the
    interpolating polynomial.

    Parameters:
        n (int): Number of interpolating points to use.
    """
    # Load the data, and find the chebyshev points
    data = np.load("airdata.npy")
    fx = lambda a, b, n :  .5*(a+b + (b-a) * np.cos(np.arange(n+1) * np.pi / n))
    a, b = 0, 366 - 1/24
    domain = np.linspace(0, b, 8784)
    points = fx(a, b, n)
    
    # Create the interpolating polynomial
    temp = np.abs(points - domain.reshape(8784, 1))
    temp2 = np.argmin(temp, axis=0)
    poly = Barycentric(domain[temp2], data[temp2])

    # Small change to the domain to prevent a divide-by-zero error
    new_domain = np.copy(domain)
    new_domain += 0.0000001

    # Plot the data and the interpolating polynomial.
    plt.plot(domain, data, label="Original data")
    plt.plot(domain, poly(new_domain), label="Interpolated polynomial")

    plt.legend()
    plt.show()

 
    


