"""Volume 2: Simplex

<Name>
<Date>
<Class>
"""

import numpy as np


# Problems 1-6
class SimplexSolver(object):
    """Class for solving the standard linear optimization problem

                        minimize        c^Tx
                        subject to      Ax <= b
                                         x >= 0
    via the Simplex algorithm.
    """
    # Problem 1
    def __init__(self, c, A, b):
        """Check for feasibility and initialize the dictionary.

        Parameters:
            c ((n,) ndarray): The coefficients of the objective function.
            A ((m,n) ndarray): The constraint coefficients matrix.
            b ((m,) ndarray): The constraint vector.

        Raises:
            ValueError: if the given system is infeasible at the origin.
        """
        if np.any(b < 0): # If any values of b are negative, then the origin is infeasible
            raise ValueError("System is infeasible at the origin.")

        self._generatedictionary(c, A, b) # If origin is feasible, create the dictionary

    # Problem 2
    def _generatedictionary(self, c, A, b):
        """Generate the initial dictionary.

        Parameters:
            c ((n,) ndarray): The coefficients of the objective function.
            A ((m,n) ndarray): The constraint coefficients matrix.
            b ((m,) ndarray): The constraint vector.
        """
        m = A.shape[0]
        # Create the dictionary
        Abar = np.hstack((A, np.eye(m)))
        cbar = np.hstack((c, np.zeros(m)))
        column1 = np.concatenate((np.zeros(1), b.T)) # Create the 1st column of the dictionary, [0, b.T].T
        columns = np.vstack((cbar, -1*Abar)) # Create the 2nd column of the dictionary, [cbar, -Abar].T
        
        D = np.concatenate((column1[:,np.newaxis], columns), axis=1) # Stack the columns together to get our dictionary
        self.D = D # Store the dictionary as an attribute.



    # Problem 3a
    def _pivot_col(self):
        """Return the column index of the next pivot column.
        """
        val = 0
        index = 0
        while val >= 0: # Find the first negative value of the top row.
            index += 1
            val = self.D[0, index]
        return index 

    # Problem 3b
    def _pivot_row(self, index):
        """Determine the row index of the next pivot row using the ratio test
        (Bland's Rule).
        """
        column = self.D[1:,index] # Get the column from the column index
        mask = np.where(column < 0, column, -1e-10) # Find negative values of column, set positive values to an arbitrary number to avoid dividing by zero
        negative_vals = mask
        
        
        ratios = -1*self.D[1:,0] / negative_vals # Calculate the ratios for the negative numbers
        index = np.argmin(ratios) # Find the least ratio and return the smallest index
        return index+1
        

    # Problem 4
    def pivot(self):
        """Select the column and row to pivot on. Reduce the column to a
        negative elementary vector.
        """
        n = np.shape(self.D)[0]
        col_index = self._pivot_col()
        if np.all(self.D[:,col_index] >= 0): # Check for boundedness
            raise ValueError("System is unbounded.")
        row_index = self._pivot_row(col_index) # Get indices for the pivot value
        pivot_val = self.D[row_index, col_index]
        
        # Perform row operations to zero out all elements of pivot column but the pivot element
        self.D[row_index,:] = -1/pivot_val * self.D[row_index,:]
        pivot_row = self.D[row_index,:]
        for i in range(n):
            if i != row_index:
                mult_value = self.D[i, col_index]
                self.D[i, :] = self.D[i,:] + mult_value * pivot_row
        


    # Problem 5
    def solve(self):
        """Solve the linear optimization problem.

        Returns:
            (float) The minimum value of the objective function.
            (dict): The basic variables and their values.
            (dict): The nonbasic variables and their values.
        """
        while not np.all(self.D[0,1:] >= 0): # Pivot until all values of the 1st row are non-negative
            self.pivot()

        opt_value = self.D[0, 0] # Get the optimal value
        ind = dict()
        dep = dict()
        for i in range(self.D[0, 1:].size): # Create and fill the dictionaries with the corresponding indices and values
            if self.D[0, i+1] == 0: # Check for dependence
                mask = np.where(self.D[:,i+1] != 0, -1, 1)
                dep[i] = self.D[np.argmin(mask), 0] # Add the value of the corresponding index to the dictionary
            else:
                ind[i] = 0 # Add the index of the independent to the dictionary with a value of zero

        return opt_value, dep, ind
        

# Problem 6
def prob6(filename='productMix.npz'):
    """Solve the product mix problem for the data in 'productMix.npz'.

    Parameters:
        filename (str): the path to the data file.

    Returns:
        ((n,) ndarray): the number of units that should be produced for each product.
    """
    data = np.load(filename) # Get data

   

    c = -1*data['p'] # Format as minimization problem
    A = np.vstack((data['A'], np.eye(len(data['d'])))) # Create matrix of coefficients
    b = np.concatenate((data['m'], data['d'])) # Create vector of constraints
    

    productMix = SimplexSolver(c, A, b) # initialize and solve the simplex problem
    opt = productMix.solve()
    n = len(c)
    vals = np.ones(n)
    for i in range(n):
        if i in opt[1]: # Check which dictionary the corresponding index is in.
            vals[i] = opt[1][i]
        else:
            vals[i] = opt[2][i]

    return vals # return vector of coefficients







    
    
    
