#!/usr/bin/python3
#this module plot the graph of single crystal mechanical properties
#written by ponychen
#20190910


import numpy as np
from mayavi import mlab

#some default parameters
f = open("input.elastic","r")
inputfile = f.readlines()
f.close()
numbers = int(inputfile[12].split()[0])  #number of points of polar system
caltype = inputfile[13].split()[0]  #E:Young's modulus B:linear compressibility G:shear modulus V:possoin radio
sheartype = inputfile[14].split()[0] #max,min,ave

#read the modulus
f = open("modulus.txt","r+")
lines = f.readlines()
c = []
for i in lines:
    c.append(list(map(float,i.split())))
c = np.array(c)

#get the s tensor
tmp = np.linalg.inv(c)
#create the initial 4 dimension s
#first create a function to transfer the 4 indicies m n p q to vogit 
def indice2vogit(m,n):
    if [ m,n]==[0,0]:
        return 0
    elif [m,n]==[1,1]:
        return 1
    elif [m,n]==[2,2]:
        return 2
    elif [m,n]==[1,2] or [m,n]==[2,1]:
        return 3
    elif [m,n]==[0,2] or [m,n]==[2,0]:
        return 4
    elif [m,n]==[0,1] or [m,n]==[1,0]:
        return 5
    else:
        print("something wrong....")

s = np.zeros([3,3,3,3])
for m in range(3):
    for n in range(3):
        for p in range(3):
            for q in range(3):
                u = indice2vogit(m,n)
                v = indice2vogit(p,q)
                if u in [0,1,2] and v in [0,1,2]:
                    s[m,n,p,q] = tmp[u,v]
                elif u in [3,4,5] and v in [3,4,5]:
                    s[m,n,p,q] = 0.25*tmp[u,v]
                else:
                    s[m,n,p,q] = 0.5*tmp[u,v]

#now calculating the E 
#get two virants of polar system
theta, phi = np.mgrid[0:np.pi+np.pi/numbers:np.pi/numbers,0:2*np.pi+2*np.pi/numbers:2*np.pi/numbers]

#get the direction cosine
def getE(l,s):
    #get the Young's modulus
    tmp = 0.0
    for m in range(3):
        for n in range(3):
            for p in range(3):
                for q in range(3):
                    tmp += s[m,n,p,q]*l[m]*l[n]*l[p]*l[q]
    return tmp

def getB(l,s):
    #get the linear compressibility
    tmp = 0.0
    for m in range(3):
        for n in range(3):
            for p in range(3):
                for q in range(3):
                    if p == q:
                        tmp += s[m,n,p,q]*l[m]*l[n]
    return tmp

l = np.array([np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),np.cos(theta)])
if caltype == "E":
    E = 1/getE(l,s)
    xyz = E*l
elif caltype == "B":
    B = getB(l,s)
    xyz = B*l

#now calculating the G
def getG(l,k,s):
    #get the shear modulus 
    tmp = 0.0
    for m in range(3):
        for n in range(3):
            for p in range(3):
                for q in range(3):
                    tmp += l[m]*k[n]*l[p]*k[q]*s[m,n,p,q]
    return tmp
def getV(l,k,s):
    #get the poisson's ratio
    tmp = 0.0
    for m in range(3):
        for n in range(3):
            for p in range(3):
                for q in range(3):
                    tmp += l[m]*l[n]*k[p]*k[q]*s[m,n,p,q]
    return tmp

if caltype == "G":
    gam = np.linspace(0,2*np.pi,numbers+1).tolist()

    Gtmp = []
    for i in gam:
        k = np.array([np.cos(theta)*np.cos(phi)*np.cos(i)-np.sin(phi)*np.sin(i),\
                np.cos(theta)*np.sin(phi)*np.cos(i)+np.cos(phi)*np.sin(i),\
                -np.sin(theta)*np.cos(i)])
        Gtmp.append(1/(4*getG(l,k,s)))
    Gtmp = np.array(Gtmp)
    
    G = np.zeros([numbers+1,numbers+1])
    for i in range(numbers+1):
        for j in range(numbers+1):
            if sheartype == "max":
                G[i,j] = max(Gtmp[:,i,j])
            elif sheartype == "min":
                G[i,j] = min(Gtmp[:,i,j])
            else:
                G[i,j] = sum(Gtmp[:,i,j])/(numbers+1)
    xyz = G*l

if caltype == "V":
    gam = np.linspace(0,2*np.pi,numbers+1).tolist()

    Vtmp = []
    for i in gam:
        k = np.array([np.cos(theta)*np.cos(phi)*np.cos(i)-np.sin(phi)*np.sin(i),\
                np.cos(theta)*np.sin(phi)*np.cos(i)+np.cos(phi)*np.sin(i),\
                -np.sin(theta)*np.cos(i)])
        Vtmp.append(-getV(l,k,s)/getE(l,s))
    Vtmp = np.array(Vtmp)
    
    V = np.zeros([numbers+1,numbers+1])
    for i in range(numbers+1):
        for j in range(numbers+1):
            if sheartype == "max":
                V[i,j] = max(Vtmp[:,i,j])
            elif sheartype == "min":
                V[i,j] = min(Vtmp[:,i,j])
            else:
                V[i,j] = sum(Vtmp[:,i,j])/(numbers+1)
    xyz = V*l
#save E to E.txt
if caltype == "E":
    f = open("E.txt","w+")
    for i in range(numbers):
        for j in range(numbers):
            f.write("%9.6f  %9.6f  %9.6f  %9.3f\n" % (xyz[0,i,j],xyz[1,i,j],xyz[2,i,j],E[i,j]))
elif caltype == "G":
    f = open("G.txt","w+")
    for i in range(numbers):
        for j in range(numbers):
            f.write("%9.6f  %9.6f  %9.6f  %9.3f\n" % (xyz[0,i,j],xyz[1,i,j],xyz[2,i,j],G[i,j]))
elif caltype == "B":
    f = open("B.txt","w+")
    for i in range(numbers):
        for j in range(numbers):
            f.write("%9.6f  %9.6f  %9.6f  %9.3f\n" % (xyz[0,i,j],xyz[1,i,j],xyz[2,i,j],B[i,j]))
else:
    f = open("V.txt","w+")
    for i in range(numbers):
        for j in range(numbers):
            f.write("%9.6f  %9.6f  %9.6f  %9.3f\n" % (xyz[0,i,j],xyz[1,i,j],xyz[2,i,j],V[i,j]))

f.close()

#plot 
mlab.options.backend = 'envisage'

if caltype == "E":
    s = mlab.mesh(xyz[0],xyz[1],xyz[2],representation="wireframe",line_width=3.0,scalars=E)
    mlab.title("Young's modulus")
elif caltype == "B":
    s = mlab.mesh(xyz[0],xyz[1],xyz[2],representation="wireframe",line_width=3.0,scalars=B)
    mlab.title("linear compressibility")
elif caltype == "G":
    s = mlab.mesh(xyz[0],xyz[1],xyz[2],representation="wireframe",line_width=3.0,scalars=G)
    mlab.title("Shear modulus")
else:
    s = mlab.mesh(xyz[0],xyz[1],xyz[2],representation="wireframe",line_width=3.0,scalars=V)
    mlab.title("Poisson's ratio")
if caltype == "B" or "V":
    mlab.colorbar(label_fmt="%6.4f",orientation='vertical')
else:
    mlab.colorbar(label_fmt="%6.1f",orientation='vertical')
mlab.axes(xlabel='[100]',ylabel='[010]',zlabel='[001]',line_width=5.0,nb_labels=0)
mlab.show()
