#!/usr/bin/python
#this script rotate the stiffness tensor by rotate matrix from rotate.txt
#format of rotate matrix in rotate.txt:
###### an 3x3 array  
###### the (i,j)(i:colomn number,j:row number) valuse is the cosine of angle
###### between the relative ith axis after rotatation and jth axis before 
###### rotation. 
###### original rotate.txt in tool means a anticlock 90 degree rotation along
###### x axis
#author: ponychen
#2019/10/19

import numpy as np

#read the modulus
f = open("modulus.txt","r+")
lines = f.readlines()
c = []
for i in lines:
    c.append(list(map(float,i.split())))
c = np.array(c)
f.close()

#read the rotate matrix (cosine of rotate angle)
f = open("rotate.txt","r+")
lines = f.readlines()
r = []
for i in range(3):
    r.append(list(map(float,lines[i].split())))
r = np.array(r)
f.close()

#get  the s matrix 
def indice2vogit(m,n):
    if [m,n] == [0,0]:
        return 0
    elif [m,n] == [1,1]:
        return 1
    elif [m,n] == [2,2]:
        return 2
    elif [m,n] == [1,2] or [m,n] == [2,1]:
        return 3
    elif [m,n] == [0,2] or [m,n] == [2,0]:
        return 4
    elif [m,n] == [0,1] or [m,n] == [1,0]:
        return 5
    else:
        print("something wrong....")

s = np.zeros([3,3,3,3])
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                tmp = 0
                for m in range(3):
                    for n in range(3):
                        for p in range(3):
                            for q in range(3):
                                u = int(indice2vogit(m,n))
                                v = int(indice2vogit(p,q))
                                tmp += r[i,m]*r[j,n]*r[k,p]*r[l,q]*c[u,v]
                s[i,j,k,l] = tmp

#transform s to c_new
c_new = np.zeros([6,6])
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                u = indice2vogit(i,j)
                v = indice2vogit(k,l)
                if u == v:
                    c_new[u,v] = s[i,j,k,l]
                else:
                    c_new[u,v] = s[i,j,k,l]
                    c_new[v,u] = s[i,j,k,l]

#output the new modulus tensor
f = open("rotate_modulus.txt","w+")
for i in range(6):
    f.write("%9.2f  %9.2f  %9.2f  %9.2f  %9.2f  %9.2f\n" % \
            (c_new[i,0],c_new[i,1],c_new[i,2],c_new[i,3],c_new[i,4],c_new[i,5]))
f.close()

