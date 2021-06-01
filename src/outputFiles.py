import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""This module calculates the Jacquard score of each algorithm and creates all the output files"""


def genDataFile(obs, blobsClusters, n):
    """input: original observations and their clusters
        output:a text file with the observations and its original clustering"""
    dataFile = open("data.txt", "w")
    for i in range(0, n - 1):
        curr = np.array(obs[i])
        np.savetxt(dataFile, curr, fmt="%0.8f", newline=",")
        dataFile.write(str(blobsClusters[i]))
        dataFile.write("\n")
    np.savetxt(dataFile, np.array(obs[n - 1]), fmt="%0.8f", newline=",")
    dataFile.write(str(blobsClusters[n - 1]))
    dataFile.close()


def calcJacquard(result, blobsClusters, n):
    """input: the result is the output of each algorithm and blobsClusters are the original clusters
    output: the calculated Jacquard measure"""
    sameCluster = 0  # the amount of pairs in the same cluster
    totalPairs = 0  # the total amount of pairs
    for j in range(0, n):
        for h in range(j + 1, n):
            if result[j] == result[h] or blobsClusters[j] == blobsClusters[h]:
                totalPairs = totalPairs + 1
            if result[j] == result[h] and blobsClusters[j] == blobsClusters[h]:
                sameCluster = sameCluster + 1
    if totalPairs == 0:  # in the case the total pairs is 0 - the Jacquard set to 1
        return 1
    return sameCluster / totalPairs


def printClusters(arr, file, k):
    """input: arr is the list of K lists where each list contains the indices of the observations in the cluster and filename
     output: printing each list as a different row in the given file"""
    rowNumber = 0
    for i in arr:
        rowNumber += 1
        counter = len(i)
        for j in i:
            file.write("%i" % j)
            counter -= 1
            if counter != 0:
                file.write(",")
        if rowNumber != k:  # checking if its not the last row
            file.write("\n")
    return


def createClusterFile(k, spectralIndex, kmeansIndex):
    """input: k and 2 lists of lists which contain the indices
    output: generating clusters.txt file"""
    with open('clusters.txt', 'w') as file:
        file.write(str(k))
        file.write("\n")
        printClusters(spectralIndex, file, k)
        file.write("\n")
        printClusters(kmeansIndex, file, k)
    file.close()


def plotGen(d, spectralJacquard, meansJacquard, resultSpectral, resultKmeansPP, obs, k1, n, k):
    """input: the parameters used to process the data and the Jacquard scores that were calculated from 2 algorithms
    output: generate the clusters.txt pdf with the plots and Jacquard measure"""

    if d == 2:
        col = ['x', 'y']
    else:
        col = ['x', 'y', 'z']

    spectralDF = pd.DataFrame(obs, columns=col)
    spectralDF.insert(d, "cluster", resultSpectral)
    meansDF = pd.DataFrame(obs, columns=col)
    meansDF.insert(d, "cluster", resultKmeansPP)

    fig = plt.figure()
    x = spectralDF.iloc[:, 0]
    y = spectralDF.iloc[:, 1]
    a = meansDF.iloc[:, 0]
    b = meansDF.iloc[:, 1]

    if d == 3:
        ax = fig.add_subplot(121, projection='3d')
        plt.title("Normalized Spectral Clustering")
        z = spectralDF.iloc[:, 2]
        ax.scatter(x, y, z, c=spectralDF['cluster'], cmap='tab20')
        bx = fig.add_subplot(122, projection='3d')
        plt.title("Kmeans")
        c = meansDF.iloc[:, 2]
        bx.scatter(a, b, c, c=meansDF['cluster'], cmap='tab20')
    else:
        ax = fig.add_subplot(121)
        ax.scatter(x, y, c=spectralDF['cluster'], cmap='tab20')
        plt.title("Normalized Spectral Clustering")
        bx = fig.add_subplot(122)
        bx.scatter(a, b, c=meansDF['cluster'], cmap='tab20')
        plt.title("Kmeans")

    info = "Data was generated from the values:" + "\n" + "n=" + str(n) + ", k=" + str(
        k1) + "\n" + "The k that was used for both algorithms was " + str(
        k, ) + "\n" + "The Jaccard measure for Spectral Clustering: " + "{:.2f}".format(
        spectralJacquard) + "\n" + "The Jaccard measure for K-means: " + "{:.2f}".format(meansJacquard)

    plt.figtext(0.5, 0.01, info, ha='center', fontsize=16, va='top', fontstyle='oblique')
    plt.savefig("clusters.pdf", bbox_inches='tight', dpi=100)
    plt.tight_layout()


def genFiles(resultSpectral, resultKmeansPP, blobsClusters, k, k1, d, obs, n):
    """this is the main function that call all the functions above and creates all the files that required"""
    spectralJacquard = calcJacquard(resultSpectral, blobsClusters, n)
    meansJacquard = calcJacquard(resultKmeansPP, blobsClusters, n)
    spectralIndex, kmeansIndex = [], []
    for i in range(k):
        spectralIndex.append((np.where(resultSpectral == i)[0].tolist()))
        kmeansIndex.append((np.where(resultKmeansPP == i)[0].tolist()))
    createClusterFile(k, spectralIndex, kmeansIndex)
    plotGen(d, spectralJacquard, meansJacquard, resultSpectral, resultKmeansPP, obs, k1, n, k)
    genDataFile(obs, blobsClusters, n)
