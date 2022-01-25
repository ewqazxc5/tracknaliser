import timeit
#from clustering import *

code = """[4, 2, 3, 1, 5].sort()"""

#how many times to run the code to get a list of times
execution_time = timeit.timeit(code, number=1)


print(execution_time)