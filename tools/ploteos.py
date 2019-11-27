#!/usr/bin/python3
#this script plot the EOS curve 
#two files needed: oldeos.txt neweos.txt 
#ponychen
#20191127

import numpy as np
from matplotlib import pyplot as plt

#read date
(X,Y) = np.loadtxt("oldeos.txt",dtype=float,unpack=True)
(CX,CY) = np.loadtxt("neweos.txt",dtype=float,unpack=True,skiprows=1)
with open("neweos.txt","r") as f:
    label = f.readlines()[0]

#plot
fig, ax = plt.subplots()
ax.plot(CX,CY,linewidth=2,color='red')
ax.set(xlabel="Volume/angstrom^3",ylabel="Energy/eV",title=label)
ax.grid()
ax.scatter(X,Y,c='grey')

plt.show()
