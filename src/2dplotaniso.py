#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

#read the relative parameters
f = open("input.elastic","r")
inputfile = f.readlines()
numbers = int(inputfile[23].split()[0]) #numbers of curve
cal_type = inputfile[24].split()[0]
f.close()

#read the modulus
f = open("modulus.txt","r")
lines = f.readlines()
c= []
for i in lines:
    c.append(list(map(float,i.split())))
c = np.array(c)

#get the s tensor
s = np.linalg.inv(c)

#get the degree list
phi = np.linspace(0,2*np.pi,numbers)

if cal_type == "E":
    E = 1/(s[0,0]*np.cos(phi)**4+s[1,1]*np.sin(phi)**4+(s[2,2]+2*s[0,1])*\
            np.cos(phi)**2*np.sin(phi)**2+2*s[0,2]*np.cos(phi)**3*np.sin(phi)+\
            2*s[1,2]*np.cos(phi)*np.sin(phi)**3)
elif cal_type == "G":
    G = 1/(4*((s[0,0]+s[1,1]-2*s[0,1])*np.cos(phi)**2*np.sin(phi)**2+s[2,2]*\
            (np.cos(phi)**2-np.sin(phi)**2)**2/4-(s[0,2]-s[1,2])*(np.cos(phi)**3*\
            np.sin(phi)-np.cos(phi)*np.sin(phi)**3)))
elif cal_type == "V":
    E = 1/(s[0,0]*np.cos(phi)**4+s[1,1]*np.sin(phi)**4+(s[2,2]+2*s[0,1])*\
            np.cos(phi)**2*np.sin(phi)**2+2*s[0,2]*np.cos(phi)**3*np.sin(phi)+\
            2*s[1,2]*np.cos(phi)*np.sin(phi)**3)     
    V = E*((s[0,0]+s[1,1]-s[2,2])*np.cos(phi)**2*np.sin(phi)**2+s[0,1]*(\
            np.cos(phi)**4+np.sin(phi)**4)+(s[0,2]-s[1,2])*(np.cos(phi)*\
            np.sin(phi)**3-np.cos(phi)**3*np.sin(phi)))
    #divide the V into Vp Vn(positive,negtive Possion's ratio)
    Vp = np.zeros(numbers)
    Vn = np.zeros(numbers)
    for i in range(numbers):
        if V[i] >= 0:
            Vp[i] = V[i]
            Vn[i] = 0.0
        else:
            Vp[i] = 0.0
            Vn[i] = -V[i]
#plot 
plt.rc('grid',color='#316931',linewidth=1,linestyle='-')
plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)
ax = plt.subplot(111,projection='polar')
if cal_type == "E":
    ax.plot(phi,E,lw=3)
    ax.set_title("Young's modulus",fontsize=20)
elif cal_type == "G":
    ax.plot(phi,G,lw=3)
    ax.set_title("Shear's modulus",fontsize=20)
elif cal_type == "V":
    ax.plot(phi,Vp,lw=3,color='blue',label='positive')
    ax.plot(phi,Vn,lw=3,color='#ee8d18',label='negative')
    ax.set_title("Possion's ratio",fontsize=20)
    ax.legend()
ax.grid(True)
plt.show()

