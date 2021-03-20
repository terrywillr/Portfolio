# gradient_methods.py
"""Volume 2: Gradient Descent Methods.
<Name>
<Class>
<Date>
"""
import numpy as np
from scipy import optimize as opt
from matplotlib import pyplot as plt


# Problem 1
def steepest_descent(f, Df, x0, tol=1e-5, maxiter=100):
    """Compute the minimizer of f using the exact method of steepest descent.

    Parameters:
        f (function): The objective function. Accepts a NumPy array of shape
            (n,) and returns a float.
        Df (function): The first derivative of f. Accepts and returns a NumPy
            array of shape (n,).
        x0 ((n,) ndarray): The initial guess.
        tol (float): The stopping tolerance.
        maxiter (int): The maximum number of iterations to compute.

    Returns:
        ((n,) ndarray): The approximate minimum of f.
        (bool): Whether or not the algorithm converged.
        (int): The number of iterations computed.
    """
    
    converge = False
    totalIter = 0
    for i in range(maxiter): # Iterate maxiter number of times
        a = lambda a : f(x0 - a*Df(x0)) # Find the argmin of a in for f(x - aDf(x))
        a0 = opt.minimize_scalar(a).x
        totalIter += 1
        x0 = x0 - a0 * Df(x0) # Update approximation

        if np.linalg.norm(Df(x0)) < tol: # If the gradient is smaller than the tolerance, we have converged
            converge = True
            break

    return x0, converge, totalIter



    


# Problem 2
def conjugate_gradient(Q, b, x0, tol=1e-4):
    """Solve the linear system Qx = b with the conjugate gradient algorithm.

    Parameters:
        Q ((n,n) ndarray): A positive-definite square matrix.
        b ((n, ) ndarray): The right-hand side of the linear system.
        x0 ((n,) ndarray): An initial guess for the solution to Qx = b.
        tol (float): The convergence tolerance.

    Returns:
        ((n,) ndarray): The solution to the linear system Qx = b.
        (bool): Whether or not the algorithm converged.
        (int): The number of iterations computed.
    """
    # Initialize our variables for Conjugate Gradient Descent
    r0 = np.dot(Q, x0) - b
    d0 = -1 * r0
    k = 0
    n = x0.size
    while np.linalg.norm(r0) >= tol and k < n: # Iterate until convergence, or until we have reached n iterations
        # Implement the Conjugate Gradient Algorithm
        a0 = (r0.T @ r0) / (d0.T @ Q @ d0)
        x1 = x0 + a0 * d0
        r1 = r0 + a0 * Q @ d0
        beta1 = (r1.T @ r1) / (r0.T @ r0)
        d1 = -1 * r1 + beta1 * d0
        k += 1
        r0 = r1
        d0 = d1
        x0 = x1
    return x0, k <= n, k


# Problem 3
def nonlinear_conjugate_gradient(f, df, x0, tol=1e-5, maxiter=250):
    """Compute the minimizer of f using the nonlinear conjugate gradient
    algorithm.

    Parameters:
        f (function): The objective function. Accepts a NumPy array of shape
            (n,) and returns a float.
        Df (function): The first derivative of f. Accepts and returns a NumPy
            array of shape (n,).
        x0 ((n,) ndarray): The initial guess.
        tol (float): The stopping tolerance.
        maxiter (int): The maximum number of iterations to compute.

    Returns:
        ((n,) ndarray): The approximate minimum of f.
        (bool): Whether or not the algorithm converged.
        (int): The number of iterations computed.
    """
    # Run the first iteration
    r0 = -1*df(x0)
    d0 = -1*r0
    a = lambda a : f(x0 + a*d0)
    a0 = opt.minimize_scalar(a).x
    x1 = x0 + a0*d0
    k = 1
    while np.linalg.norm(r0) >= tol and k < maxiter: # Keep running the algorithm until we converge, or iterate maxiter number of times
        r1 = -1 * df(x1)
        beta1 = (r1.T @ r1) / (r0.T @ r0)
        d1 = r1 + beta1 * d0
        a = lambda a : f(x1 + a*d1)
        a1 = opt.minimize_scalar(a).x
        x2 = x1 + a1*d1
        k += 1
        r0 = r1
        d0 = d1
        x1 = x2
    return x1, k < maxiter, k 



# Problem 4
def prob4(filename="linregression.txt",
          x0=np.array([-3482258, 15, 0, -2, -1, 0, 1829])):
    """Use conjugate_gradient() to solve the linear regression problem with
    the data from the given file, the given initial guess, and the default
    tolerance. Return the solution to the corresponding Normal Equations.
    """
    A = np.loadtxt(filename) # Initialize the data
    b = A[:, 0] # Get the y values from the data
    A = np.concatenate((np.ones(b.size)[:, np.newaxis], np.delete(A, 0, axis=1)), axis=1) # Format the data so that it can be used in least squares (add a column of ones to the front)
    Q = A.T @ A # Create our semi-definite matrix Q
    return conjugate_gradient(Q, A.T @ b, x0)[0] # Use our conjugate gradient algorithm to solve the system and return x


# Problem 5
class LogisticRegression1D:
    """Binary logistic regression classifier for one-dimensional data."""

    def fit(self, x, y, guess):
        """Choose the optimal beta values by minimizing the negative log
        likelihood function, given data and outcome labels.

        Parameters:
            x ((n,) ndarray): An array of n predictor variables.
            y ((n,) ndarray): An array of n outcome variables.
            guess (array): Initial guess for beta.
        """
        neg_log = lambda b : np.sum(np.log(1 + np.exp(-1*(b[0] + b[1]*x))) + (1 - y)*(b[0] + b[1]*x)) # Negative log likelihood
        
        b = opt.fmin_cg(neg_log, guess) # Use scipy's optimize library to get b0 and b1
        self.b0, self.b1 = b[0], b[1] # Store b0 and b1 in the class

    def predict(self, x):
        """Calculate the probability of an unlabeled predictor variable
        having an outcome of 1.

        Parameters:
            x (float): a predictor variable with an unknown label.
        """
        return 1 / (1 + np.exp(-1*(self.b0 + self.b1 * x))) # Calculate sigma(x), our probability that x is assigned the label y=1


# Problem 6
def prob6(filename="challenger.npy", guess=np.array([20., -1.])):
    """Return the probability of O-ring damage at 31 degrees Farenheit.
    Additionally, plot the logistic curve through the challenger data
    on the interval [30, 100].

    Parameters:
        filename (str): The file to perform logistic regression on.
                        Defaults to "challenger.npy"
        guess (array): The initial guess for beta.
                        Defaults to [20., -1.]
    """
    data = np.load(filename) # load data and split it into our x and y values
    x, y = data[:, 0], data[:, 1] 
    
    probability = LogisticRegression1D() # Initialize class and fit the data
    probability.fit(x, y, guess)

    domain = np.linspace(30, 100, 100)
    # Plot the probability with our data
    plt.scatter(x, y, label="Previous damage")
    plt.plot(domain, probability.predict(domain), label="Probability of damage")
    plt.scatter(31, probability.predict(31), label="Probability at 31 degrees")

    plt.legend()
    plt.xlabel("Tempurature")
    plt.ylabel("O-Ring Damage")
    plt.show()

    return probability.predict(31)









    