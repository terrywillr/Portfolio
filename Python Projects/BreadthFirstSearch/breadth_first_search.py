# breadth_first_search.py
"""Volume 2: Breadth-First Search.
<Name>
<Class>
<Date>
"""

from collections import deque
import networkx as nx
from matplotlib import pyplot as plt

# Problems 1-3
class Graph:
    """A graph object, stored as an adjacency dictionary. Each node in the
    graph is a key in the dictionary. The value of each key is a set of
    the corresponding node's neighbors.

    Attributes:
        d (dict): the adjacency dictionary of the graph.
    """
    def __init__(self, adjacency={}):
        """Store the adjacency dictionary as a class attribute"""
        self.d = dict(adjacency)

    def __str__(self):
        """String representation: a view of the adjacency dictionary."""
        return str(self.d)

    # Problem 1
    def add_node(self, n):
        """Add n to the graph (with no initial edges) if it is not already
        present.

        Parameters:
            n: the label for the new node.
        """
        self.d[n] = set()

    # Problem 1
    def add_edge(self, u, v):
        """Add an edge between node u and node v. Also add u and v to the graph
        if they are not already present.

        Parameters:
            u: a node label.
            v: a node label.
        """
        if u in self.d and v in self.d:
            self.d[u].add(v)
            self.d[v].add(u)

        else:
            if u in self.d:
                self.add_node(v)
                self.d[u].add(v)
                self.d[v].add(u)

            elif v in self.d:
                self.add_node(u)
                self.d[u].add(v)
                self.d[v].add(u)

            else:
                self.add_node(u)
                self.add_node(v)
                self.d[u].add(v)
                self.d[v].add(u)




    # Problem 1
    def remove_node(self, n):
        """Remove n from the graph, including all edges adjacent to it.

        Parameters:
            n: the label for the node to remove.

        Raises:
            KeyError: if n is not in the graph.
        """
        if n in self.d:
            self.d.pop(n)
        else:
            raise KeyError("Node not in graph")

        for node in self.d:
            if n in self.d[node]:
                self.d[node].remove(n)
        

    # Problem 1
    def remove_edge(self, u, v):
        """Remove the edge between nodes u and v.

        Parameters:
            u: a node label.
            v: a node label.

        Raises:
            KeyError: if u or v are not in the graph, or if there is no
                edge between u and v.
        """
        if u not in self.d or v not in self.d:
            raise KeyError("One or more nodes not in graph")
        if v not in self.d[u] or v not in self.d[u]:
            raise KeyError("No edge between nodes")

        self.d[u].remove(v)
        self.d[v].remove(u)

    # Problem 2
    def traverse(self, source):
        """Traverse the graph with a breadth-first search until all nodes
        have been visited. Return the list of nodes in the order that they
        were visited.

        Parameters:
            source: the node to start the search at.

        Returns:
            (list): the nodes in order of visitation.

        Raises:
            KeyError: if the source node is not in the graph.
        """
        if source not in self.d:
            raise KeyError("Source not in graph")
        V = []
        Q = deque()
        M = set()

        Q.appendleft(source)
        M.add(source)

        while len(Q) != 0:
            current = Q.pop()
            V.append(current)

            for edge in self.d[current]:
                if edge not in M:
                    Q.appendleft(edge)
                    M.add(edge)

        return V


    # Problem 3
    def shortest_path(self, source, target):
        """Begin a BFS at the source node and proceed until the target is
        found. Return a list containing the nodes in the shortest path from
        the source to the target, including endoints.

        Parameters:
            source: the node to start the search at.
            target: the node to search for.

        Returns:
            A list of nodes along the shortest path from source to target,
                including the endpoints.

        Raises:
            KeyError: if the source or target nodes are not in the graph.
        """
        if source not in self.d or target not in self.d:
            raise KeyError("Source node or target node not in graph")
        V = []
        Q = deque()
        M = set()
        explored = dict()
        
        
        Q.appendleft(source)
        M.add(source)

        while len(Q) != 0:
            current = Q.pop()
            V.append(current)

            for edge in self.d[current]:
                if edge not in explored:
                    if edge not in M:
                        Q.appendleft(edge)
                        M.add(edge)
                        explored[edge] = current
        Output = []
        Output.insert(0, target)
        next = explored[target]
        Output.insert(0, next)
        while next != source:
            next = explored[next]
            Output.insert(0, next)


        return Output


# Problems 4-6
class MovieGraph:
    """Class for solving the Kevin Bacon problem with movie data from IMDb."""

    # Problem 4
    def __init__(self, filename="movie_data.txt"):
        """Initialize a set for movie titles, a set for actor names, and an
        empty NetworkX Graph, and store them as attributes. Read the speficied
        file line by line, adding the title to the set of movies and the cast
        members to the set of actors. Add an edge to the graph between the
        movie and each cast member.

        Each line of the file represents one movie: the title is listed first,
        then the cast members, with entries separated by a '/' character.
        For example, the line for 'The Dark Knight (2008)' starts with

        The Dark Knight (2008)/Christian Bale/Heath Ledger/Aaron Eckhart/...

        Any '/' characters in movie titles have been replaced with the
        vertical pipe character | (for example, Frost|Nixon (2008)).
        """
        self.movies = set()
        self.actors = set()
        self.graph = nx.Graph()

        infile = open(filename, 'r', encoding="utf-8")
        alldata = infile.read()
        alldata_lst = alldata.split("\n")

        for ele in alldata_lst:
            line = ele.split("/")
            self.movies.add(line[0])
            self.graph.add_node(line[0])

            for data in line[1:]:
                self.graph.add_edge(line[0], data)
                self.actors.add(data)


        



    # Problem 5
    def path_to_actor(self, source, target):
        """Compute the shortest path from source to target and the degrees of
        separation between source and target.

        Returns:
            (list): a shortest path from source to target, including endpoints and movies.
            (int): the number of steps from source to target, excluding movies.
        """
        length = 0
        path = nx.shortest_path(self.graph, source, target)

        for actor in path:
            if actor in self.actors and actor != target:
                length += 1

        return path, length

    # Problem 6
    def average_number(self, target):
        """Calculate the shortest path lengths of every actor to the target
        (not including movies). Plot the distribution of path lengths and
        return the average path length.

        Returns:
            (float): the average path length from actor to target.
        """
        
        distances = []
        
        paths = nx.shortest_path(self.graph, target)
        length = 0

        for path in paths.values():
            for actor in path:
                if actor in self.actors and actor != target:
                    length += 1

            distances.append(length)
            length = 0

        plt.hist(distances, bins=[i-.5 for i in range(8)])
        plt.show()
        return sum(distances) / len(self.actors)

"""if __name__ == "__main__":
    graph = Graph({'A': {'C', 'B'}, 'B': {'D', 'E', 'A'}, 'C': {'F', 'G', 'A'}, 'D': {'I', 'B', 'H'}, 'E': {'K', 'J', 'B'}, 'F': {'M', 'C', 'L'}, 'G': {'N', 'C', 'O'}, 'H': {'D'}, 'I': {'D'}, 'J': {'E'}, 'K': {'E'}, 'L': {'F'}, 'M': {'F'}, 'N': {'G'}, 'O': {'G'}})
    print(graph.shortest_path('A', 'N'))"""