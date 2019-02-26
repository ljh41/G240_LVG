import numpy as np
import math
import string
import os
import sys

#name
position = sys.argv[1]

#data
fda21 = np.loadtxt('./data/T/co21ficvlT'+position+'.dat')
fda1321 = np.loadtxt('./data/T/13co21cvlT'+position+'.dat')
n21 = fda21.shape[0]
n1321 = fda1321.shape[0]

#calculate ratio
daratio = np.zeros(n1321)
for i in range(n1321):
    for j in range(n21):
        if abs(fda21[i,0]-fda1321[j,0])<0.1:
            daratio = 
