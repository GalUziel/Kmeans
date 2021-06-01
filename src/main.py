import argparse
from outputFiles import genFiles
import numpy as np
from sklearn.datasets import make_blobs
import random
from spectral import spectralNormal
from kmeans_pp import kmeansPP

"""
This is the main module which is used to run the whole project"""

def main():
    # The project's arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("k", type=int)
    parser.add_argument("n", type=int)
    parser.add_argument('--no-Random', dest='Random', action='store_false', default=True)
    args = parser.parse_args()
    K = args.k
    n = args.n
    rand = args.Random
    d = random.choice([2, 3])
    # checking the correctness of the input 
    if (not rand) and (K <= 0 or n <= 0 or K >= n):
        print("Wrong arguments given")
        exit(1)

    # maximum capacity that our program can process
    maxCapK2 = 16
    maxCapN2 = 420
    maxCapK3 = 16
    maxCapN3 = 400

    # if rand is true k and n will be chosen randomly
    if rand:
        if d == 2:
            K = random.randint(int(maxCapK2 / 2), maxCapK2)
            n = random.randint(int(maxCapN2 / 2), maxCapN2)
        else:
            K = random.randint(int(maxCapK3 / 2), maxCapK3)
            n = random.randint(int(maxCapN3 / 2), maxCapN3)

    # generating n observations with K centers and d dimensions
    points = make_blobs(n_samples=n, centers=K, n_features=d)
    obs = np.array(points[0], copy=True)

    # blobsClusters includes the original cluster of each point
    blobsClusters = np.asarray(points[1])

    # spectralNormal is the algorithm in the spectral module that calculates T and k as required
    T, k = spectralNormal(obs, K, rand)

    # kmeansPP is the algorithm which computes which observation belong to each cluster
    resultSpectral = np.array(kmeansPP(T, k, n, T.shape[1])).astype(int)
    resultKmeansPP = np.array(kmeansPP(obs, k, n, d)).astype(int)

    # genFiles is the module that builds the plots and creates the output files
    genFiles(resultSpectral, resultKmeansPP, blobsClusters, k, K, d, obs, n)

# calling the main algorithm
main()
