# cvxpy_intro.py
"""Volume 2: Intro to CVXPY.
<Name>
<Class>
<Date>
"""
import numpy as np
import cvxpy as cp

def prob1():
    """Solve the following convex optimization problem:

    minimize        2x + y + 3z
    subject to      x  + 2y         <= 3
                         y   - 4z   <= 1
                    2x + 10y + 3z   >= 12
                    x               >= 0
                          y         >= 0
                                z   >= 0

    Returns (in order):
        The optimizer x (ndarray)
        The optimal value (float)
    """
    x = cp.Variable(3, nonneg=True)
    c = np.array([2, 1, 3])
    objective = cp.Minimize(c.T @ x) # Initialize objective function with its coefficients

    # Create constraint coefficients
    G = np.array([1, 2, 0]) 
    H = np.array([0, 1, -4])
    J = np.array([2, 10, 3])
    
    constraints = [G @ x <= 3, H @ x <= 1, J @ x >= 12] # Initialize constraint functions

    problem = cp.Problem(objective, constraints)

    # Solve optimization problem and return optimal value and optimizing vector.
    opt_value = problem.solve()
    optimizer = x.value
    
    return optimizer, opt_value

# Problem 2
def l1Min(A, b):
    """Calculate the solution to the optimization problem

        minimize    ||x||_1
        subject to  Ax = b

    Parameters:
        A ((m,n) ndarray)
        b ((m, ) ndarray)

    Returns:
        The optimizer x (ndarray)
        The optimal value (float)
    """
    x = cp.Variable(A.shape[1]) 

    objective = cp.Minimize(cp.norm(x, 1)) # Create objective function by taking the 1-norm of an n-size vector.
    constraints = [A @ x == b] # Use A and b to create constraint

    problem = cp.Problem(objective, constraints)
    opt_value = problem.solve() # solve problem and return optimal value and optimizing vector
    optimizer = x.value

    return optimizer, opt_value



# Problem 3
def prob3():
    """Solve the transportation problem by converting the last equality constraint
    into inequality constraints.

    Returns (in order):
        The optimizer x (ndarray)
        The optimal value (float)
    """
    p = cp.Variable(6, nonneg=True)
    c = np.array([4, 7, 6, 8, 8, 9])
    objective = cp.Minimize(c.T @ p) # Create objective function using cost of each route.
    # Create constraints by using the supply and demand from each of the supply and demand locations
    constraints = [p[0] + p[1] <= 7, p[2] + p[3] <= 2, p[4] + p[5] <= 4, p[0] + p[2] + p[4] == 5, p[1] + p[3] + p[5] == 8] 

    problem = cp.Problem(objective, constraints) # Initialize and solve problem. Return optimal value and optimizing vector
    opt_value = problem.solve()
    optimizer = p.value
    return optimizer, opt_value


# Problem 4
def prob4():
    """Find the minimizer and minimum of

    g(x,y,z) = (3/2)x^2 + 2xy + xz + 2y^2 + 2yz + (3/2)z^2 + 3x + z

    Returns (in order):
        The optimizer x (ndarray)
        The optimal value (float)
    """
    Q = np.array([[3, 2, 1], [2, 4, 2], [1, 2, 3]]) # Use the given function to create the Q and r matrices
    r = np.array([3, 0, 1])
    x = cp.Variable(3)

    problem = cp.Problem(cp.Minimize(.5 * cp.quad_form(x, Q) + r.T @ x)) # intialize quad-form minimization problem.
    opt_value = problem.solve() # Solve problem and return optimal value
    optimizer = x.value
    
    return optimizer, opt_value


# Problem 5
def prob5(A, b):
    """Calculate the solution to the optimization problem
        minimize    ||Ax - b||_2
        subject to  ||x||_1 == 1
                    x >= 0
    Parameters:
        A ((m,n), ndarray)
        b ((m,), ndarray)
        
    Returns (in order):
        The optimizer x (ndarray)
        The optimal value (float)
    """
    x = cp.Variable(A.shape[1], nonneg=True)

    objective = cp.Minimize(cp.norm(A @ x - b, 2))
    constraints = [cp.sum(x) == 1] # Since variables must be nonnegative, the affine function sum() can be used in place of the 1-norm.

    problem = cp.Problem(objective, constraints)

    opt_value = problem.solve()
    optimizer = x.value

    return optimizer, opt_value


# Problem 6
def prob6():
    """Solve the college student food problem. Read the data in the file 
    food.npy to create a convex optimization problem. The first column is 
    the price, second is the number of servings, and the rest contain
    nutritional information. Use cvxpy to find the minimizer and primal 
    objective.
    
    Returns (in order):
        The optimizer x (ndarray)
        The optimal value (float)
    """	 
    data = np.load("food.npy", allow_pickle=True) # load in data and split it by column.
    p = data[:,0]
    s = data[:,1]
    c = data[:,2]
    f = data[:,3]
    su = data[:,4]
    calc = data[:,5]
    fib = data[:,6]
    pro = data[:,7]
    
    x = cp.Variable(18, nonneg=True)
    objective = cp.Minimize(p.T @ x) # Create minimization problem.
    # multiply each column by serving size and create constraints from the given information
    constraints = [cp.sum(np.multiply(c, s).T @ x) <= 2000,
                   cp.sum(np.multiply(f, s).T @ x) <= 65,
                   cp.sum(np.multiply(su, s).T @ x) <= 50,
                   cp.sum(np.multiply(calc, s).T @ x) >= 1000,
                   cp.sum(np.multiply(fib, s).T @ x) >= 25,
                   cp.sum(np.multiply(pro, s).T @ x) >= 46]

    problem = cp.Problem(objective, constraints) # initizlie and solve problem, then return optimal value and vector.

    opt_value = problem.solve()
    optimizer = x.value

    return optimizer, opt_value





