# profiling.py
"""Python Essentials: Profiling.
<Name>
<Class>
<Date>
"""

# Note: for problems 1-4, you need only implement the second function listed.
# For example, you need to write max_path_fast(), but keep max_path() unchanged
# so you can do a before-and-after comparison.

import numpy as np
import string
from numba import jit
from time import time
from matplotlib import pyplot as plt


# Problem 1
def max_path(filename="triangle.txt"):
    """Find the maximum vertical path in a triangle of values."""
    with open(filename, 'r') as infile:
        data = [[int(n) for n in line.split()]
                        for line in infile.readlines()]
    def path_sum(r, c, total):
        """Recursively compute the max sum of the path starting in row r
        and column c, given the current total.
        """
        total += data[r][c]
        if r == len(data) - 1:          # Base case.
            return total
        else:                           # Recursive case.
            return max(path_sum(r+1, c,   total),   # Next row, same column
                       path_sum(r+1, c+1, total))   # Next row, next column

    return path_sum(0, 0, 0)            # Start the recursion from the top.

def max_path_fast(filename="triangle_large.txt"):
    """Find the maximum vertical path in a triangle of values."""
    with open(filename, 'r') as infile:
        data = [[int(n) for n in line.split()]
                for line in infile.readlines()]

    i = len(data) - 1
    while i > 0:
        for j in range(len(data[i]) - 1):
            
            if j == 0:
                data[i-1][j] += data[i][j]
            elif j == len(data[i]) - 1:
                
                data[i-1][j] += data[i][j]
            else:
                data[i][j] += data[i-1][j-1] + data[i-1][j]
        i -= 1

    return data[0][0]

        



    


# Problem 2
def primes(N):
    """Compute the first N primes."""
    primes_list = []
    current = 2
    while len(primes_list) < N:
        isprime = True
        for i in range(2, current):     # Check for nontrivial divisors.
            if current % i == 0:
                isprime = False
        if isprime:
            primes_list.append(current)
        current += 1
    return primes_list

def primes_fast(N):
    """Compute the first N primes."""
    primes_list = [2]
    current = 3
    
    while len(primes_list) < N:
        isprime = True
        for i in range(2, int(np.sqrt(current))): # Check for nontrivial divisors.s
            if current % i == 0:
                isprime = False
                break
            
        if isprime:
            primes_list.append(current)
        
        current += 2
    return primes_list



# Problem 3
def nearest_column(A, x):
    """Find the index of the column of A that is closest to x.

    Parameters:
        A ((m,n) ndarray)
        x ((m, ) ndarray)

    Returns:
        (int): The index of the column of A that is closest in norm to x.
    """
    distances = []
    for j in range(A.shape[1]):
        distances.append(np.linalg.norm(A[:,j] - x))
    return np.argmin(distances)

def nearest_column_fast(A, x):
    """Find the index of the column of A that is closest in norm to x.
    Refrain from using any loops or list comprehensions.

    Parameters:
        A ((m,n) ndarray)
        x ((m, ) ndarray)

    Returns:
        (int): The index of the column of A that is closest in norm to x.
    """
    return np.argmin(np.linalg.norm(A - x, axis=0))


# Problem 4
def name_scores(filename="names.txt"):
    """Find the total of the name scores in the given file."""
    with open(filename, 'r') as infile:
        names = sorted(infile.read().replace('"', '').split(','))
    total = 0
    for i in range(len(names)):
        name_value = 0
        for j in range(len(names[i])):
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            for k in range(len(alphabet)):
                if names[i][j] == alphabet[k]:
                    letter_value = k + 1
            name_value += letter_value
        total += (names.index(names[i]) + 1) * name_value
    return total


def name_scores_fast(filename='names.txt'):
    """Find the total of the name scores in the given file."""
    with open(filename, 'r') as infile:
        names = sorted(infile.read().replace('"', '').split(','))
    total = 0
    name_dict = dict(zip(names, range(1, len(names) + 1)))
    alphabet = dict(zip(string.ascii_uppercase, range(1,27)))
    for name in names:
        name_value = 0
        for letter in name:
            name_value += alphabet[letter]
            
            
        total += (name_dict[name] + 1) * name_value
    return total


# Problem 5
def fibonacci():
    """Yield the terms of the Fibonacci sequence with F_1 = F_2 = 1."""
    F_1 = 0
    F_2 = 1
    while True:
        yield F_1
        F_1, F_2 = F_2, F_1 + F_2

def fibonacci_digits(N=10000):
    """Return the index of the first term in the Fibonacci sequence with
    N digits.

    Returns:
        (int): The index.
    """
    for i, x in enumerate(fibonacci()):
        if len(str(x)) == N:
            return i



# Problem 6
def prime_sieve(N):
    """Yield all primes that are less than N."""
    nums = [n for n in range(2, N + 1)]
    while len(nums) != 0:
        yield nums[0]
        nums = [n for n in nums if n % nums[0] != 0]
        
        
# Problem 7
def matrix_power(A, n):
    """Compute A^n, the n-th power of the matrix A."""
    product = A.copy()
    temporary_array = np.empty_like(A[0])
    m = A.shape[0]
    for power in range(1, n):
        for i in range(m):
            for j in range(m):
                total = 0
                for k in range(m):
                    total += product[i,k] * A[k,j]
                temporary_array[j] = total
            product[i] = temporary_array
    return product


@jit
def matrix_power_numba(A, n):
    """Compute A^n, the n-th power of the matrix A, with Numba optimization."""
    product = A.copy()
    temporary_array = np.empty_like(A[0])
    m = A.shape[0]
    for power in range(1, n):
        for i in range(m):
            for j in range(m):
                total = 0
                for k in range(m):
                    total += product[i,k] * A[k,j]
                temporary_array[j] = total
            product[i] = temporary_array
    return product
    

def prob7(n=10):
    """Time matrix_power(), matrix_power_numba(), and np.linalg.matrix_power()
    on square matrices of increasing size. Plot the times versus the size.
    """
    matrix_power_numba(np.random.random((2, 2)), 2)
    time_reg = []
    time_numba = []
    time_numpy = []
    for m in range(2, 8):
        A = np.random.random((2**m, 2**m))

        start = time()
        matrix_power(A, n)
        end = time()
        time_reg.append(end - start)

        start = time()
        matrix_power_numba(A, n)
        end = time()
        time_numba.append(end - start)

        start = time()
        np.linalg.matrix_power(A, n)
        end = time()
        time_numpy.append(end - start)

    domain = [2**i for i in range(2, 8)]

    plt.loglog(domain, time_reg, label="matrix_power()", base=2)
    plt.loglog(domain, time_numba, label="matrix_power_numba()", base=2)
    plt.loglog(domain, time_numpy, label="np.linalg.matrix_power()", base=2)

    plt.legend()
    plt.show()
    print(time_reg, time_numba, time_numpy, domain, sep="\n")

    
    

        





    
