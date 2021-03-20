# montecarlo_integration.py
"""Volume 1: Monte Carlo Integration.
<Name>
<Class>
<Date>
"""
import numpy as np
from numpy import linalg as la
from scipy import stats
from matplotlib import pyplot as plt

# Problem 1
def ball_volume(n, N=10000):
    """Estimate the volume of the n-dimensional unit ball.

    Parameters:
        n (int): The dimension of the ball. n=2 corresponds to the unit circle,
            n=3 corresponds to the unit sphere, and so on.
        N (int): The number of random points to sample.

    Returns:
        (float): An estimate for the volume of the n-dimensional unit ball.
    """
    points = np.random.uniform(-1, 1, (n, N))
    lengths = la.norm(points, axis=0)
    num_within = np.count_nonzero(lengths < 1)

    return 2**n * (num_within / N)



# Problem 2
def mc_integrate1d(f, a, b, N=10000):
    """Approximate the integral of f on the interval [a,b].

    Parameters:
        f (function): the function to integrate. Accepts and returns scalars.
        a (float): the lower bound of interval of integration.
        b (float): the lower bound of interval of integration.
        N (int): The number of random points to sample.

    Returns:
        (float): An approximation of the integral of f over [a,b].

    Example:
        >>> f = lambda x: x**2
        >>> mc_integrate1d(f, -4, 2)    # Integrate from -4 to 2.
        23.734810301138324              # The true value is 24.
    """
    points = np.random.uniform(a, b, N)
    y = f(points)
    vol = b - a
    return vol / N * np.sum(y)


# Problem 3
def mc_integrate(f, mins, maxs, N=10000):
    """Approximate the integral of f over the box defined by mins and maxs.

    Parameters:
        f (function): The function to integrate. Accepts and returns
            1-D NumPy arrays of length n.
        mins (list): the lower bounds of integration.
        maxs (list): the upper bounds of integration.
        N (int): The number of random points to sample.

    Returns:
        (float): An approximation of the integral of f over the domain.

    Example:
        # Define f(x,y) = 3x - 4y + y^2. Inputs are grouped into an array.
        >>> f = lambda x: 3*x[0] - 4*x[1] + x[1]**2

        # Integrate over the box [1,3]x[-2,1].
        >>> mc_integrate(f, [1, -2], [3, 1])
        53.562651072181225              # The true value is 54.
    """
    vol = 1

    all_points = np.zeros(N)
    
    for i in range(0, len(mins)):
        points = np.random.uniform(mins[i], maxs[i], N)
        vol *= maxs[i] - mins[i]
        
        all_points = np.column_stack((all_points, points))
        
    totalsum = 0
    all_points = all_points[:, 1:]
    for i in range(N):
        y = f(all_points[i, :])
        totalsum += y
    
    return float(vol / N * totalsum)


    


# Problem 4
def prob4():
    """Let n=4 and Omega = [-3/2,3/4]x[0,1]x[0,1/2]x[0,1].
    - Define the joint distribution f of n standard normal random variables.
    - Use SciPy to integrate f over Omega.
    - Get 20 integer values of N that are roughly logarithmically spaced from
        10**1 to 10**5. For each value of N, use mc_integrate() to compute
        estimates of the integral of f over Omega with N samples. Compute the
        relative error of estimate.
    - Plot the relative error against the sample size N on a log-log scale.
        Also plot the line 1 / sqrt(N) for comparison.
    """
    n=4
    f = lambda x : 1 / (2*np.pi)**(n/2) * np.exp(-1/2 * np.dot(x.T, x))
    Omega = ([3/4, 1, 1/2, 1], [-3/2, 0, 0, 0])
    
    min = np.array([-3/2, 0, 0, 0])
    max = np.array([3/4, 1, 1/2, 1])

    means, cov = np.zeros(4), np.eye(4)

    exact = stats.mvn.mvnun(min, max, means, cov)[0]

    num = np.logspace(1, 5, 20, dtype = np.int64, base=10)

    rel_list = []
    for N in num:
        estimate = mc_integrate(f, Omega[1], Omega[0], N)
        
        rel_list.append(np.abs(exact - estimate) / np.abs(exact))

    plt.loglog(num, rel_list, label="Relative error")
    plt.loglog(num, 1 / np.sqrt(num), label="f = 1 / sqrt(N)")

    plt.legend()
    plt.show()
    


"""if __name__ == "__main__":
    f = lambda x : x[0]**2 + x[1]**2
    mins = [0, 0]
    max = [1, 1]
    print(mc_integrate(f, mins, max), type(mc_integrate(f, mins, max)))"""

   



