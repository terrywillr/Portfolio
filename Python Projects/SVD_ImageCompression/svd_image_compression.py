# solutions.py
"""Volume 1: The SVD and Image Compression. Solutions File."""
import numpy as np
from scipy import linalg as la
from matplotlib import pyplot as plt
from imageio import imread

# Problem 1
def compact_svd(A, tol=1e-6):
    """Compute the truncated SVD of A.

    Parameters:
        A ((m,n) ndarray): The matrix (of rank r) to factor.
        tol (float): The tolerance for excluding singular values.

    Returns:
        ((m,r) ndarray): The orthonormal matrix U in the SVD.
        ((r,) ndarray): The singular values of A as a 1-D array.
        ((r,n) ndarray): The orthonormal matrix V^H in the SVD.
    """
    A_H = A.conj().T
    
    lamb, V = la.eig(A_H @ A)
    sing_vals = np.sqrt(lamb)

    indices = np.argsort(sing_vals)

    sing_vals = sing_vals[indices[::-1]]
    V = V[:,indices[::-1]]

    r = 0
    for val in sing_vals:
        if val > tol:
            r += 1

    sing_vals = sing_vals[:r]
    V = V[:,:r]
    U = A @ V / sing_vals
    return U, sing_vals, V.conj().T


# Problem 2
def visualize_svd(A):
    """Plot the effect of the SVD of A as a sequence of linear transformations
    on the unit circle and the two standard basis vectors.
    """
    theta = np.linspace(0, 2 * np.pi, 200)
    S = np.array([np.cos(theta), np.sin(theta)])
    
    E = np.array([[1, 0, 0], [0, 0, 1]])
    U, s, Vh = la.svd(A)
    M2 = np.diag(s) @ Vh
    M3 = U @ np.diag(s) @ Vh
    
    
    ax1 = plt.subplot(221)
    
    ax1.plot(S[0], S[1])
    ax1.plot(E[0], E[1])

    ax2 = plt.subplot(222)
   
    ax2.plot((Vh @ S)[0], (Vh @ S)[1])
    ax2.plot((Vh @ E)[0], (Vh @ E)[1])

    ax3 = plt.subplot(223)
    
    ax3.plot((M2 @ S)[0], (M2 @ S)[1])
    ax3.plot((M2 @ E)[0], (M2 @ E)[1])

    ax4 = plt.subplot(224)
    
    ax4.plot((M3 @ S)[0], (M3 @ S)[1])
    ax4.plot((M3 @ E)[0], (M3 @ E)[1])

    plt.suptitle('SVD decomposition')
    plt.axis("equal")
    plt.show()






# Problem 3
def svd_approx(A, s):
    """Return the best rank s approximation to A with respect to the 2-norm
    and the Frobenius norm, along with the number of bytes needed to store
    the approximation via the truncated SVD.

    Parameters:
        A ((m,n), ndarray)
        s (int): The rank of the desired approximation.

    Returns:
        ((m,n), ndarray) The best rank s approximation of A.
        (int) The number of entries needed to store the truncated SVD.
    """
    m, n = A.shape
    if s > np.linalg.matrix_rank(A):
        raise ValueError("s must be less than the rank of A")

    U, sig, Vh = la.svd(A, full_matrices = False)
    U1 = U[:,:s]
    sig1 = sig[:s]
    Vh1 = Vh[:s,:]
    A_s = U1 @ np.diag(sig1) @ Vh1

    return A_s, U1.size + sig1.size + Vh1.size

# Problem 4
def lowest_rank_approx(A, err):
    """Return the lowest rank approximation of A with error less than 'err'
    with respect to the matrix 2-norm, along with the number of bytes needed
    to store the approximation via the truncated SVD.

    Parameters:
        A ((m, n) ndarray)
        err (float): Desired maximum error.

    Returns:
        A_s ((m,n) ndarray) The lowest rank approximation of A satisfying
            ||A - A_s||_2 < err.
        (int) The number of entries needed to store the truncated SVD.
    """
    m, n = A.shape
    U, s, Vh = la.svd(A, full_matrices=False)
    if (err <= s[-1]):
        raise ValueError("A cannot be approximated within the given tolerance")

    mask = np.where(err <= s, 1, 0)
    print(mask)
    print(s, s[-1])
    
    rank = np.sum(mask)
    
    
    U1 = U[:,:rank]
    s1 = s[:rank]
    Vh1 = Vh[:rank, :]
    A_s = U1 @ np.diag(s1) @ Vh1

    return A_s, U1.size + s1.size + Vh1.size
    
    



# Problem 5
def compress_image(filename, s):
    """Plot the original image found at 'filename' and the rank s approximation
    of the image found at 'filename.' State in the figure title the difference
    in the number of entries used to store the original image and the
    approximation.

    Parameters:
        filename (str): Image file path.
        s (int): Rank of new image.
    """
    image = imread(filename) / 255
    

    if len(image.shape) > 2:

        R = image[:,:,0]
        G = image[:,:,1]
        B = image[:,:,2]

        R_s, num1 = svd_approx(R, s)
        G_s, num2 = svd_approx(G, s)
        B_s, num3 = svd_approx(B, s)

        num = num1 + num2 + num3

        im = np.clip(np.dstack((R_s, G_s, B_s)), 0, 1)

        ax1 = plt.subplot(121)
        ax1.imshow(image)

        ax2 = plt.subplot(122)
        ax2.imshow(im)
    else:
        im, num = svd_approx(image, s)
        im = np.clip(im, 0, 1)
        
        ax1 = plt.subplot(121)
        ax1.imshow(image, cmap="gray")

        ax2 = plt.subplot(122)
        ax2.imshow(im, cmap="gray")

    

    plt.suptitle(str(image.size - num))
    plt.axis("off")
    plt.show()


"""if __name__ == "__main__":
    compress_image("hubble.jpg", 120)"""