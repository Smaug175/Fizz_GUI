import array
import numpy as np
set=[]
for i in range(10):
    for j in range(10):
        for k in range(10):
            set.append([i,j,k])
print(set)
a=np.array(set)
print(a)
print(a[0][-1:])