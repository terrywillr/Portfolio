# image_segmentation.py
"""Volume 1: Image Segmentation.
<Name>
<Class>
<Date>
"""

import numpy as np
from scipy import linalg as la
from imageio import imread
from matplotlib import pyplot as plt
from scipy import sparse
from scipy.sparse import csgraph
from scipy.sparse.linalg import eigsh
import math


# Problem 1
def laplacian(A):
    """Compute the Laplacian matrix of the graph G that has adjacency matrix A.

    Parameters:
        A ((N,N) ndarray): The adjacency matrix of an undirected graph G.

    Returns:
        L ((N,N) ndarray): The Laplacian matrix of G.
    """
    m, n = A.shape
    diags = [sum(A[i,]) for i in range(n)]
    D = np.diag(diags)
    return D - A


# Problem 2
def connectivity(A, tol=1e-8):
    """Compute the number of connected components in the graph G and its
    algebraic connectivity, given the adjacency matrix A of G.

    Parameters:
        A ((N,N) ndarray): The adjacency matrix of an undirected graph G.
        tol (float): Eigenvalues that are less than this tolerance are
            considered zero.

    Returns:
        (int): The number of connected components in G.
        (float): the algebraic connectivity of G.
    """
    numConnected = 0
    L = laplacian(A)
    eigs = np.real(la.eigvals(L))
    np.sort(eigs)
    for i in range(eigs.shape[0]):
        if eigs[i] < tol:
            numConnected += 1
    return numConnected, float(eigs[1]), eigs


# Helper function for problem 4.
def get_neighbors(index, radius, height, width):
    """Calculate the flattened indices of the pixels that are within the given
    distance of a central pixel, and their distances from the central pixel.

    Parameters:
        index (int): The index of a central pixel in a flattened image array
            with original shape (radius, height).
        radius (float): Radius of the neighborhood around the central pixel.
        height (int): The height of the original image in pixels.
        width (int): The width of the original image in pixels.

    Returns:
        (1-D ndarray): the indices of the pixels that are within the specified
            radius of the central pixel, with respect to the flattened image.
        (1-D ndarray): the euclidean distances from the neighborhood pixels to
            the central pixel.
    """
    # Calculate the original 2-D coordinates of the central pixel.
    row, col = index // width, index % width

    # Get a grid of possible candidates that are close to the central pixel.
    r = int(radius)
    x = np.arange(max(col - r, 0), min(col + r + 1, width))
    y = np.arange(max(row - r, 0), min(row + r + 1, height))
    X, Y = np.meshgrid(x, y)

    # Determine which candidates are within the given radius of the pixel.
    R = np.sqrt(((X - col)**2 + (Y - row)**2))
    mask = R < radius
    return (X[mask] + Y[mask]*width).astype(np.int), R[mask]


# Problems 3-6
class ImageSegmenter:
    """Class for storing and segmenting images."""

    # Problem 3
    def __init__(self, filename):
        """Read the image file. Store its brightness values as a flat array."""
        image = imread(filename)
        self.scaled = image / 255
        if len(image.shape) > 2:
            self.brightness = np.ravel(self.scaled.mean(axis=2))
        else:
            self.brightness = np.ravel(self.scaled)

    # Problem 3
    def show_original(self):
        """Display the original image."""
        if len(self.scaled.shape) > 2:
            plt.imshow(self.scaled)
            plt.axis("off")
            plt.show()
        else:
            plt.imshow(self.scaled, cmap="gray")
            plt.axis("off")
            plt.show()
        

    # Problem 4
    def adjacency(self, r=5., sigma_B2=.02, sigma_X2=3.):
        """Compute the Adjacency and Degree matrices for the image graph."""
        m, n = self.scaled.shape[0], self.scaled.shape[1]

        A = sparse.lil_matrix((m * n, m * n))
        D = np.zeros(m * n)

        for i in range(m * n):
            indices, dists = get_neighbors(i, r, m, n)
            weights = [math.exp(-1 * (abs(self.brightness[i] - self.brightness[indices[j]]) / sigma_B2) - dists[j] / sigma_X2) for j in range(indices.shape[0])] 
            A[i, indices] = weights
            D[i] = np.sum(A[i])
             
        
        return A.tocsc(), D

    # Problem 5
    def cut(self, A, D):
        """Compute the boolean mask that segments the image."""
        m, n = self.scaled.shape[0], self.scaled.shape[1]

        L = csgraph.laplacian(A)
        to_diag = 1 / np.sqrt(D)
        D_invsqrt = sparse.diags(to_diag, offsets=0)
        C = D_invsqrt.dot(L.dot(D_invsqrt))

        eigvals, eigvects = eigsh(C, k=2, which="SM")
        eig = eigvects[:,1]
        
        eig = np.reshape(eig, (m, n))
        mask = eig > 0

        return mask


    # Problem 6
    def segment(self, r=5., sigma_B=.02, sigma_X=3.):
        """Display the original image and its segments."""
        A, D = self.adjacency(r, sigma_B, sigma_X)
        

        if len(self.scaled.shape) > 2:
            positive = np.dstack((self.cut(A, D), self.cut(A, D), self.cut(A, D)))
            negated = ~positive
            positive_image = self.scaled * positive
            negative_image = self.scaled * negated
            ax1 = plt.subplot(131)
            ax1.imshow(self.scaled)
            ax1.axis("off")

            ax2 = plt.subplot(132)
            ax2.imshow(positive_image)
            ax2.axis("off")

            ax3 = plt.subplot(133)
            ax3.imshow(negative_image)
            ax3.axis("off")

        else:
            positive = self.scaled * self.cut(A, D)
            negative = self.scaled * ~self.cut(A, D)
            ax1 = plt.subplot(131)
            ax1.imshow(self.scaled, cmap="gray")
            ax1.axis("off")

            ax2 = plt.subplot(132)
            ax2.imshow(positive, cmap="gray")
            ax2.axis("off")

            ax3 = plt.subplot(133)
            ax3.imshow(negative, cmap="gray")
            ax3.axis("off")

        plt.show()







