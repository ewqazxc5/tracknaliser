The k-means algorithm
=====================
1. Pick k points randomly to be the initial centres of the clusters.
2. Assign each data point to a cluster.Computeits distance from all cluster centres,and assign it to the nearest centre.
3. Update the centre of each cluster by setting it to the average of all points assigned to the cluster.
4. Repeat steps 2-3 for the desired number of times.

skip sqrt
---------
Compute its distance from all cluster centres, and assign it to the nearest centre.
So I skip the sqrt for d = x^2+y^2+z^2, just get the index of the smallest distance. 

Refactoring kmeans for readability
----------------------------------
1. use variable k and iterations intead of magic number.
2. make code read file clearly.
3. modify distances calculated part with k value.
4. modify new mean update part with k value.
5. refacter code for initial centres of the clusters.
6. change while to for loop.
7. Remove use of single letter variable names etc.

Using Numpy
-----------
1. use np.array to convert list to numnpy object.
2. use np.sum to calculate the distance to k centre points.
3. use np.argmin to get the index of the nearest cluster.



