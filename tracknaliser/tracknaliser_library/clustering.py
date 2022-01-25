from math import *
from random import *
import os
import pathlib
import argparse
import sys


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
  
  Returns
  -------
  centers : tuple list
      the means of k clusters
  alloc : int list
      the cluster indexs for the data points.
  """
  # clusters = 3
  centers = [None]*clusters
  for i in range(clusters):
    centers[i] = ps[randrange(len(ps))]

  alloc = [None]*len(ps)

  for n in range(iterations):
    for i in range(len(ps)):
      point = ps[i]
      distances = [None] * clusters
      for di in range(clusters):
        mi = centers[di]
        distances[di] = sqrt((point[0]-mi[0])**2 + (point[1]-mi[1])**2 + (point[2]-mi[2])**2)
      alloc[i] = distances.index(min(distances))

    for i in range(clusters):
      alloc_ps = [point for j, point in enumerate(ps) if alloc[j] == i]
      sum0 = sum1 = sum2 = 0
      for a in alloc_ps:
        sum0 += a[0]
        sum1 += a[1]
        sum2 += a[2]
      new_mean=(sum0 / len(alloc_ps), sum1 / len(alloc_ps), sum2 / len(alloc_ps))
      centers[i] = new_mean
  return centers, alloc

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


