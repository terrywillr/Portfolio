# interior_point_linear.py
"""Volume 2: Interior Point for Linear Programs.
<Name>
<Class>
<Date>
"""

import numpy as np
from scipy import linalg as la
from scipy.stats import linregress
from matplotlib import pyplot as plt


# Auxiliary Functions ---------------------------------------------------------
def starting_point(A, b, c):
    """Calculate an initial guess to the solution of the linear program
    min c^T x, Ax = b, x>=0.
    Reference: Nocedal and Wright, p. 410.
    """
    # Calculate x, lam, mu of minimal norm satisfying both
    # the primal and dual constraints.
    B = la.inv(A @ A.T)
    x = A.T @ B @ b
    lam = B @ A @ c
    mu = c - (A.T @ lam)

    # Perturb x and s so they are nonnegative.
    dx = max((-3./2)*x.min(), 0)
    dmu = max((-3./2)*mu.min(), 0)
    x += dx*np.ones_like(x)
    mu += dmu*np.ones_like(mu)

    # Perturb x and mu so they are not too small and not too dissimilar.
    dx = .5*(x*mu).sum()/mu.sum()
    dmu = .5*(x*mu).sum()/x.sum()
    x += dx*np.ones_like(x)
    mu += dmu*np.ones_like(mu)

    return x, lam, mu

# Use this linear program generator to test your interior point method.
def randomLP(j,k):
    """Generate a linear program min c^T x s.t. Ax = b, x>=0.
    First generate m feasible constraints, then add
    slack variables to convert it into the above form.
    Parameters:
        j (int >= k): number of desired constraints.
        k (int): dimension of space in which to optimize.
    Returns:
        A ((j, j+k) ndarray): Constraint matrix.
        b ((j,) ndarray): Constraint vector.
        c ((j+k,), ndarray): Objective function with j trailing 0s.
        x ((k,) ndarray): The first 'k' terms of the solution to the LP.
    """
    A = np.random.random((j,k))*20 - 10
    A[A[:,-1]<0] *= -1
    x = np.random.random(k)*10
    b = np.zeros(j)
    b[:k] = A[:k,:] @ x
    b[k:] = A[k:,:] @ x + np.random.random(j-k)*10
    c = np.zeros(j+k)
    c[:k] = A[:k,:].sum(axis=0)/k
    A = np.hstack((A, np.eye(j)))
    return A, b, -c, x


# Problems --------------------------------------------------------------------
def interiorPoint(A, b, c, niter=20, tol=1e-16, verbose=False):
    """Solve the linear program min c^T x, Ax = b, x>=0
    using an Interior Point method.

    Parameters:
        A ((m,n) ndarray): Equality constraint matrix with full row rank.
        b ((m, ) ndarray): Equality constraint vector.
        c ((n, ) ndarray): Linear objective function coefficients.
        niter (int > 0): The maximum number of iterations to execute.
        tol (float > 0): The convergence tolerance.

    Returns:
        x ((n, ) ndarray): The optimal point.
        val (float): The minimum value of the objective function.
    """
    


    def _F(x, lamb, mu):
        row1 = A.T @ lamb + mu - c
        row2 = A @ x - b
        row3 = np.diag(mu) @ x

        return np.concatenate((row1, row2, row3))

    def _grad(x, lamb, mu, sigma=.1):
        n = x.size
        m = lamb.size
        
        row1 = np.hstack((np.zeros((n, n)), A.T, np.eye(n)))
        row2 = np.hstack((A, np.zeros((m, n)), np.zeros((m, m))))
        row3 = np.hstack((np.diag(mu), np.zeros((n, m)), np.diag(x)))
        
        DF = np.vstack((row1, row2, row3))

        v = (x.T @ mu) / n
        e = np.ones(n)
        RHS = -_F(x, lamb, mu) + np.hstack((np.zeros(n + m), sigma * v * e))

        lu, piv = la.lu_factor(DF)
        dir = la.lu_solve((lu, piv), RHS)

        return dir

    def _step(x, lamb, mu, dir):
        n = x.size
        if np.mean(dir[-n:] > 0) == 1:
            amax = 1
        else:
            mu_indices = np.argwhere(dir[-n:] < 0)
            
            amax = np.min((-1*mu / dir[-n:])[mu_indices])
        if np.mean(dir[:n] > 0) == 1:
            delmax = 1
        else:
            x_indices = np.argwhere(dir[:n] < 0)
            delmax = np.min((-1*x / dir[:n])[x_indices])

        
        a = min((1, 0.95*amax))
        delta = min((1, 0.95*delmax))
        

        return a, delta


    x, lamb, mu = starting_point(A, b, c)
    n = x.size
    m = lamb.size
    v = (x.T @ mu) / n
    
    for i in range(niter):
        if v < tol:
            break
        
        dir = _grad(x, lamb, mu)
        a, delta = _step(x, lamb, mu, dir)
        x += delta * dir[:n]
        lamb += a*dir[n:n+m]
        mu += a*dir[-n:]

        v = (x.T @ mu) / n
        

    return x, c.T @ x


def leastAbsoluteDeviations(filename='simdata.txt'):
    """Generate and show the plot requsested in the lab."""
    data = np.loadtxt(filename)

    m = data.shape[0]
    n = data.shape[1] - 1
    c = np.zeros(3*m + 2*(n+1))
    c[:m] = 1
    y = np.empty(2*m)
    y[::2] = -data[:, 0]
    y[1::2] = data[:, 0]
    x = data[:, 1:]

    A = np.ones((2*m, 3*m + 2*(n+1)))
    A[::2, :m] = np.eye(m)
    A[1::2, :m] = np.eye(m)
    A[::2, m:m+n] = -x
    A[1::2, m:m+n] = x
    A[::2, m+n:m+2*n] = x
    A[1::2, m+n:m+2*n] = -x
    A[::2, m+2*n] = -1
    A[1::2, m+2*n+1] = -1
    A[:, m+2*n+2:] = -np.eye(2*m, 2*m)

    sol = interiorPoint(A, y, c, niter=10)[0]

    beta = sol[m:m+n] - sol[m+n:m+2*n]
    b = sol[m+2*n] - sol[m+2*n+1]


    slope, intercept = linregress(data[:,1], data[:,0])[:2]
    domain = np.linspace(0, 10, 200)
    plt.plot(domain, domain*slope + intercept, label="Least Squares")
    plt.plot(domain, beta*domain + b, label="Least Absolute Deviations", color="orange")
    plt.scatter(data[:,1], data[:,0], label="data", color='g')

    plt.legend()
    plt.show()






if __name__ == "__main__":
    leastAbsoluteDeviations()
