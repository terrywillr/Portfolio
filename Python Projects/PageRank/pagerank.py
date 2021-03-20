# solutions.py
"""Volume 1: The Page Rank Algorithm.
<Name>
<Class>
<Date>
"""
import numpy as np
from scipy import linalg as la
import networkx as nx
from itertools import combinations
# Problems 1-2
class DiGraph:
    """A class for representing directed graphs via their adjacency matrices.

    Attributes:
        (fill this out after completing DiGraph.__init__().)
    """
    # Problem 1
    def __init__(self, A, labels=None):
        """Modify A so that there are no sinks in the corresponding graph,
        then calculate Ahat. Save Ahat and the labels as attributes.

        Parameters:
            A ((n,n) ndarray): the adjacency matrix of a directed graph.
                A[i,j] is the weight of the edge from node j to node i.
            labels (list(str)): labels for the n nodes in the graph.
                If None, defaults to [0, 1, ..., n-1].
        """
        n = A.shape[0]
        self.n = n
        Ahat = np.zeros(A.shape)
        for i in range(n):
            Ahat[:,i] = np.where(np.allclose(A[:,i], np.zeros(n)), np.ones(n), A[:,i])

        Abar = np.copy(Ahat)
        for i in range(n):
            Abar[:,i] = 1 / np.sum(Ahat[:,i]) * Ahat[:,i]

        self.A = Abar
        if labels != None:
            if len(labels) != n:
                raise ValueError("Incorrect number of weights")
            self.L = labels
        else:
            self.L = [i for i in range(n)]



    # Problem 2
    def linsolve(self, epsilon=0.85):
        """Compute the PageRank vector using the linear system method.

        Parameters:
            epsilon (float): the damping factor, between 0 and 1.

        Returns:
            dict(str -> float): A dictionary mapping labels to PageRank values.
        """
        dct = dict()
        I = np.eye(self.n)
        RHS = (1 - epsilon) / self.n * np.ones(self.n)

        p = la.solve(I - epsilon*self.A, RHS)

        for i in range(self.n):
            dct[self.L[i]] = p[i]

        return dct

    # Problem 2
    def eigensolve(self, epsilon=0.85):
        """Compute the PageRank vector using the eigenvalue method.
        Normalize the resulting eigenvector so its entries sum to 1.

        Parameters:
            epsilon (float): the damping factor, between 0 and 1.

        Return:
            dict(str -> float): A dictionary mapping labels to PageRank values.
        """
        dct = dict()
        B = epsilon * self.A + (1 - epsilon) / self.n * np.ones(self.A.shape)
        eigval, eigvec = la.eig(B)
        
        index = np.where(np.allclose(eigval, 1.), 1, 0)
        
        p = eigvec[:,index] / la.norm(eigvec[:,index], ord=1)
        p /= np.sum(p)
        

        for i in range(self.n):
            dct[self.L[i]] = p[i]

        return dct



    # Problem 2
    def itersolve(self, epsilon=0.85, maxiter=100, tol=1e-12):
        """Compute the PageRank vector using the iterative method.

        Parameters:
            epsilon (float): the damping factor, between 0 and 1.
            maxiter (int): the maximum number of iterations to compute.
            tol (float): the convergence tolerance.

        Return:
            dict(str -> float): A dictionary mapping labels to PageRank values.
        """
        dct = dict()

        p0 = 1 / self.n * np.ones(self.n)
        p1 = epsilon * np.dot(self.A, p0) + (1 - epsilon) / self.n * np.ones(self.n)
        iter = 1
        while la.norm(p1 - p0) >= tol and iter <= maxiter:
            p0 = p1
            p1 = epsilon * np.dot(self.A, p0) + (1 - epsilon) / self.n * np.ones(self.n)
            iter += 1

        for i in range(self.n):
            dct[self.L[i]] = p1[i]

        return dct




# Problem 3
def get_ranks(d):
    """Construct a sorted list of labels based on the PageRank vector.

    Parameters:
        d (dict(str -> float)): a dictionary mapping labels to PageRank values.

    Returns:
        (list) the keys of d, sorted by PageRank value from greatest to least.
    """
    keys = list(d.keys())
    vals = list(d.values())

    indices = sorted(range(len(vals)), key=vals.__getitem__)[::-1]

    return [keys[i] for i in indices]




# Problem 4
def rank_websites(filename="web_stanford.txt", epsilon=0.85):
    """Read the specified file and construct a graph where node j points to
    node i if webpage j has a hyperlink to webpage i. Use the DiGraph class
    and its itersolve() method to compute the PageRank values of the webpages,
    then rank them with get_ranks(). If two webpages have the same rank,
    resolve ties by listing the webpage with the larger ID number first.

    Each line of the file has the format
        a/b/c/d/e/f...
    meaning the webpage with ID 'a' has hyperlinks to the webpages with IDs
    'b', 'c', 'd', and so on.

    Parameters:
        filename (str): the file to read from.
        epsilon (float): the damping factor, between 0 and 1.

    Returns:
        (list(str)): The ranked list of webpage IDs.
    """
    infile = open(filename, 'r')
    data = infile.read()
    lines = data.split('\n')[:-1]
    numericID = []

    
    Ids = set()
    for line in lines:
        data = line.split("/")
        for ele in data:
            Ids.add(ele)
    
    for Id in Ids:
        numericID.append(int(Id))

    indices = sorted(range(len(numericID)), key=numericID.__getitem__)
    
    mylabels = [list(Ids)[i] for i in indices]
    
    
    
    A = np.zeros((len(mylabels), len(mylabels)))
    for line in lines:
        data = line.split("/")
        for ele in data[1:]:
            A[mylabels.index(ele), mylabels.index(data[0])] = 1
            

    graph = DiGraph(A, labels=mylabels)
    return get_ranks(graph.itersolve(epsilon))

    
    


# Problem 5
def rank_ncaa_teams(filename, epsilon=0.85):
    """Read the specified file and construct a graph where node j points to
    node i with weight w if team j was defeated by team i in w games. Use the
    DiGraph class and its itersolve() method to compute the PageRank values of
    the teams, then rank them with get_ranks().

    Each line of the file has the format
        A,B
    meaning team A defeated team B.

    Parameters:
        filename (str): the name of the data file to read.
        epsilon (float): the damping factor, between 0 and 1.

    Returns:
        (list(str)): The ranked list of team names.
    """
    infile = open(filename, 'r')
    data = infile.read()
    lines = data.split('\n')
    lines = lines[1:-1]
    
    winners = []
    losers = []
    for line in lines:
        game = line.split(',')
        winners.append(game[0])
        losers.append(game[1])
    
    games = []
    for i in range(len(losers)):
        games.append((winners[i], losers[i]))
    teams = list(set(losers + winners))
    A = np.zeros((len(teams), len(teams)))
    
    for i in range(len(games)):
        A[teams.index(games[i][0]), teams.index(games[i][1])] += 1

    graph = DiGraph(A, labels=teams)
    return get_ranks(graph.itersolve(epsilon))
    


# Problem 6
def rank_actors(filename="top250movies.txt", epsilon=0.85):
    """Read the specified file and construct a graph where node a points to
    node b with weight w if actor a and actor b were in w movies together but
    actor b was listed first. Use NetworkX to compute the PageRank values of
    the actors, then rank them with get_ranks().

    Each line of the file has the format
        title/actor1/actor2/actor3/...
    meaning actor2 and actor3 should each have an edge pointing to actor1,
    and actor3 should have an edge pointing to actor2.
    """
    DG = nx.DiGraph()

    infile = open(filename, 'r', encoding='utf-8')
    data = infile.read()
    lines = data.split('\n')
    for line in lines:
        names = line.split('/')[1:]
        combos = list(combinations(names, 2))
        
        for pair in combos:
            if not DG.has_node(pair[0]):
                DG.add_node(pair[0])
            if not DG.has_node(pair[1]):
                DG.add_node(pair[1])
            if not DG.has_edge(pair[1], pair[0]):
                DG.add_edge(pair[1], pair[0], weight=1)
            else:
                DG[pair[1]][pair[0]]['weight'] += 1
        
    
    return get_ranks(nx.pagerank(DG, epsilon))




