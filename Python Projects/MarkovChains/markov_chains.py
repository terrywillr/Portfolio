# markov_chains.py
"""Volume 2: Markov Chains.
<Name>
<Class>
<Date>
"""

import numpy as np
from scipy import linalg as la


class MarkovChain:
    """A Markov chain with finitely many states.

    Attributes:
        A: The column stochastic transition matrix
        states: List of labels used to classify the data
        dict: The dictionary mapping state labels to row/column that they correspond to in A
    """
    # Problem 1
    def __init__(self, A, states=None):
        """Check that A is column stochastic and construct a dictionary
        mapping a state's label to its index (the row / column of A that the
        state corresponds to). Save the transition matrix, the list of state
        labels, and the label-to-index dictionary as attributes.

        Parameters:
        A ((n,n) ndarray): the column-stochastic transition matrix for a
            Markov chain with n states.
        states (list(str)): a list of n labels corresponding to the n states.
            If not provided, the labels are the indices 0, 1, ..., n-1.

        Raises:
            ValueError: if A is not square or is not column stochastic.

        Example:
            >>> MarkovChain(np.array([[.5, .8], [.5, .2]], states=["A", "B"])
        corresponds to the Markov Chain with transition matrix
                                   from A  from B
                            to A [   .5      .8   ]
                            to B [   .5      .2   ]
        and the label-to-index dictionary is {"A":0, "B":1}.
        """
        m, n = A.shape

        if m != n:
            raise ValueError("Matrix is not square")
        if not np.allclose(A.sum(axis=0), np.ones(A.shape[1])):
            raise ValueError("A is not column stochastic")

        self.A = A
        self.states = states
        self.dict = dict()

        if states == None:
            self.states = list()

            for row in range(n):
                self.states.append(n)
                self.dict[row] = row

        else:
            for row in range(n):
                self.dict[states[row]] = row


    # Problem 2
    def transition(self, state):
        """Transition to a new state by making a random draw from the outgoing
        probabilities of the state with the specified label.

        Parameters:
            state (str): the label for the current state.

        Returns:
            (str): the label of the state to transitioned to.
        """
        column = self.dict[state]
        row = np.random.multinomial(1, self.A[:,column])
        
        value = np.argmax(row)
        
        return list(self.dict.keys())[value]

    # Problem 3
    def walk(self, start, N):
        """Starting at the specified state, use the transition() method to
        transition from state to state N-1 times, recording the state label at
        each step.

        Parameters:
            start (str): The starting state label.

        Returns:
            (list(str)): A list of N state labels, including start.
        """
        lst = [start]
        i = 0
        state = start

        while i < N:
            state = self.transition(state)
            lst.append(state)
            i += 1

        return lst


    # Problem 3
    def path(self, start, stop):
        """Beginning at the start state, transition from state to state until
        arriving at the stop state, recording the state label at each step.

        Parameters:
            start (str): The starting state label.
            stop (str): The stopping state label.

        Returns:
            (list(str)): A list of state labels from start to stop.
        """
        state = start
        lst = [start]
        while state != stop:
            state = self.transition(state)
            lst.append(state)

        return lst

    # Problem 4
    def steady_state(self, tol=1e-12, maxiter=40):
        """Compute the steady state of the transition matrix A.

        Parameters:
            tol (float): The convergence tolerance.
            maxiter (int): The maximum number of iterations to compute.

        Returns:
            ((n,) ndarray): The steady state distribution vector of A.

        Raises:
            ValueError: if there is no convergence within maxiter iterations.
        """
        m, n = self.A.shape
        x_0 = abs(np.random.normal(0, 1, size=(n)))
        x_0 = x_0 / np.sum(x_0)
        x_1 = np.zeros(n)
        k = 0
        while la.norm(x_1 - x_0, ord=1) > tol:
            if k == maxiter:
                raise ValueError("No convergence within specified iterations")
            k += 1
            x_1 = np.dot(self.A, x_0)
            x_0 = x_1

        return x_1


class SentenceGenerator(MarkovChain):
    """A Markov-based simulator for natural language.

    Attributes:
        states: the set of all unique words from the file
        A: The transition Matrix
    """
    # Problem 5
    def __init__(self, filename):
        """Read the specified file and build a transition matrix from its
        contents. You may assume that the file has one complete sentence
        written on each line.
        """
        infile = open(filename, 'r')
        data = infile.read()
        unique = sorted(set(data.split()), key=data.split().index)
        
        self.states = unique
        self.states.insert(0, "$tart")
        self.states.append("$top")
        self.dict = dict()

        n = len(self.states)
        self.A = np.zeros((n,n))
        sentences = data.split('\n')
        

        for row in range(n):
            self.dict[self.states[row]] = row
        
        
        for sentence in sentences:
            
            lst = sentence.split()
            lst.append("$top")
            lst.insert(0, "$tart")
            
            
            i = 0
            j = 1
            while j < len(lst):
                
                self.A[self.dict[lst[j]], self.dict[lst[i]]] += 1
                i += 1
                j += 1
            
        self.A[n-1, n-1] = 1
        
        # self.A = self.A / np.sum(self.A, axis=0)
        
        self.A = self.A / np.sum(self.A, axis=0)
        
        MarkovChain.__init__(self, self.A, self.states)

    # Problem 6
    def babble(self):
        """Create a random sentence using MarkovChain.path().

        Returns:
            (str): A sentence generated with the transition matrix, not
                including the labels for the $tart and $top states.

        Example:
            >>> yoda = SentenceGenerator("yoda.txt")
            >>> print(yoda.babble())
            The dark side of loss is a path as one with you.
        """
        lst = self.path("$tart", "$top")
        lst.remove("$tart")
        lst.remove("$top")
        sentence = ' '.join(lst)
        return sentence


"""if __name__ == "__main__":
    yoda = SentenceGenerator("bee.txt")
    for _ in range(100):
        print(yoda.babble())"""