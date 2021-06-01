import numpy as np
import math

"""
This module computes the normalized spectral clustering algorithm
it contains all the required calculation such as QR and GramSchmidt.
"""


def genWeightedMatrix(points, n):
    """ input: matrix A of shape nXn and n
        output: weighted adjacency matrix W """
    wMatrix = np.zeros((n, n), np.float32)
    for i in range(0, n):
        for j in range(i + 1, n):
            result = np.exp(np.linalg.norm(points[i] - points[j]) / -2)
            wMatrix[i][j] = result
            wMatrix[j][i] = result
    return wMatrix


def genDiagonalMatrix(matrix, n):
    """input: W matrix in shape nXn and n
    output:D^-0.5 matrix in shape nXn, where D is the diagonal degree matrix 
     """
    dMatrix = np.zeros((n, n), np.float32)
    rowSum = np.sqrt(np.sum(matrix, axis=1))
    if rowSum.any() == 0:
        print("Division by zero in the calculate of D matrix")
        exit(1)
    result = 1 / rowSum
    np.fill_diagonal(dMatrix, result)
    return dMatrix


def genLaplacian(wMat, dMat, n):
    """
        input:  W matrix and D matrix in shape nXn
        output: Lnorm matrix in shape nXn as described in the algorithm
        """
    return np.eye(n) - dMat @ wMat @ dMat


def MGS(A, n):
    """input: matrix in shape nXn
    output: Q and R"""
    U = np.copy(A)
    Q = np.zeros((n, n), np.float32)
    R = np.zeros((n, n), np.float32)
    for i in range(n):
        R[i, i] = np.linalg.norm(U[:, i])
        if R[i, i] != 0:
            Q[:, i] = U[:, i] / (R[i, i])
        # We chose to handle the case when R[i,i] is zero by leaving the columns as it is, filled with zeros
        R[i][i + 1:n] = np.transpose(Q[:, i]) @ U[:, i + 1:n]
        curr = (R[i][:, np.newaxis] * Q[:, i])
        U[:, i + 1:n] = U[:, i + 1:n] - np.transpose(curr)[:, i + 1:n]
    return Q, R


def QR(A, n, eps):
    """ input: matrix nXn, n and epsilon
        output: A and Q matrix"""
    A_bar = np.copy(A)
    Q_bar = np.eye(n)
    for i in range(0, n):
        Q, R = MGS(A_bar, n)
        A_bar = R @ Q
        mulQ = Q_bar @ Q
        res = (np.absolute(Q_bar) - np.absolute(mulQ))
        if (np.abs(res) <= eps).all():
            return A_bar, Q_bar
        Q_bar = mulQ
    return A_bar, Q_bar


def eigenGap(A_matrix, Q_matrix, rand, K, n):
    """ input: A and Q matrix, boolean Random,K and n
        output:k and U matrix"""
    eigenRow = np.diagonal(A_matrix)
    Q = np.vstack((Q_matrix, eigenRow))
    sortedQ = Q[:, Q[-1].argsort()]
    eigenSorted = np.sort(eigenRow)
    diff = np.diff(eigenSorted)
    diff = np.abs(diff)
    diffMax = diff[0:math.ceil(n / 2)]
    if rand:
        k = np.where(diffMax == np.amax(diffMax))
        minIndex = int(k[0]) + 1
    else:
        minIndex = K
    return minIndex, sortedQ[:n, :minIndex]


# the main function that use all the functions above
def spectralNormal(points, K, rand):
    """input: points - array of observations,k and random
    output: k and T matrix"""
    n = len(points)
    eps = 0.0001
    w = genWeightedMatrix(points, n)
    d = genDiagonalMatrix(w, n)
    lap = genLaplacian(w, d, n) + np.eye(n)
    # We added the identity matrix as suggested in the course forum in order to avoid possible division by zero
    A, Q = QR(lap, n, eps)
    k, eigenVectors = eigenGap(A, Q, rand, K, n)
    res = np.linalg.norm(eigenVectors, axis=-1)[:, np.newaxis]
    if res.any() == 0:
        print("Division by zero in the calculation of the T matrix")
        exit(1)
    T = np.divide(eigenVectors, res)
    return T, k
