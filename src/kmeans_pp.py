import numpy as np
import mykmeanssp as kl
"""This module contains the algorithm of kmeansPP as described in hw2, it initializes the K centroids that will be used in
kmeans.c"""


def kmeansPP(observation, k, n, d):
    """input: an array of observations,k,n,d
        output: an array that contains the number of the cluster that each observation belongs to """
    MAX_ITER = 300
    curr_cent = np.zeros((k, d), np.float32)
    np.random.seed(0)
    index = np.random.choice(n, 1)
    x = index[0]
    curr_cent[0] = observation[x]
    centNum = 0
    distances = np.full(n, np.inf, np.float32)
    for j in range(1, k):
        centNum += 1
        distances = np.minimum(distances, np.sum(np.power(curr_cent[j - 1] - observation, 2), axis=1))
        sum_distance = np.sum(distances)
        if sum_distance == 0:
            print("Division by zero in the calculation of the probability")
            exit(1)
        probs = np.true_divide(distances, sum_distance)
        index = np.random.choice(n, 1, p=probs)
        curr_cent[centNum] = observation[index]

    result = kl.getMeans(k, n, d, MAX_ITER, curr_cent.tolist(), observation.tolist())
    return result
