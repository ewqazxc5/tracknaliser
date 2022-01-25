from math import *
from random import *
import argparse
import sys
import os
import numpy as np
import pathlib


def cluster(ps, iterations = 10, clusters = 3):
  """
  k-means algorithm for clustering data points
  In the end, each cluster will (ideally) contain points that are close to each other

  Parameters
  ----------
  ps : list
      data point tuple in a list
  iterations: int
      iterations times for calculate k clusters
  cluster: int
  defalult k = 3
  
  Returns
  -------
  centers : tuple list
      the means of k clusters
  alloc : int list
      the cluster indexs for the data points.
  """
  # the number of clusters = 3
  # clusters = 3
  centers = [None]*clusters
  for i in range(clusters):
    centers[i] = ps[randrange(len(ps))]

  alloc = np.zeros(len(ps), dtype=int)
  ps = np.array(ps)

  for n in range(iterations):
    for i in range(len(ps)):
      pointNp = np.array(ps[i])
      mp = np.array(centers)
      distances = (mp-pointNp)**2
      distances = np.sum(distances, axis = 1)
      alloc[i] = np.argmin(distances)

    for i in range(clusters):
      alloc_ps = ps[alloc == i]
      sum = np.sum(alloc_ps, axis = 0)
      centers[i] = sum/len(alloc_ps)
  return centers, alloc.tolist()

if __name__ == '__main__':
  filename = os.path.join(pathlib.Path(__file__).parent.resolve(), "samples.csv")
  iters = 10
  if len(sys.argv) > 1:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument("-I", "--iters", type=int, help="iterations.")

    list = sys.argv
    args = parser.parse_args()
    if args.filename is not None:
      filename = args.filename
    if args.iters is not None:
      iters = args.iters

  lines = open(filename, 'r').readlines()
  ps = []
  for line in lines: 
    numbers = line.strip().split(',')
    ps.append(tuple(map(float, numbers)))

  centers, alloc = cluster(ps, iters)
  clusters = 3
  for i in range(clusters):
    alloc_ps=[point for j, point in enumerate(ps) if alloc[j] == i]
    print("Cluster " + str(i) + " is centred at " + str(centers[i]) + " and has " + str(len(alloc_ps)) + " points.")
    print(alloc_ps)


