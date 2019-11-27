#!/usr/bin/python3
#this modulue calculate the stifftensor
#author:ponychen
#email:18709821294@outlook.com
#20190831

import numpy as np
from scipy.linalg import solve
from scipy.optimize import leastsq
from scipy.optimize import curve_fit

def getparameter(results,types,numbers,max_strain,axis,bravi_type):
    #this function output the b in Ax=b
    step = 2*max_strain/(numbers-1)
    X = np.array([-max_strain+i*step for i in range(numbers) ])
    volume = getvolume(axis,bravi_type)
    parameters = np.zeros(types)
    for i in range(types):
        tmp = results[i,int((numbers-1)/2)]
        for j in range(numbers):
            if results[i,j] < tmp:
                print("type"+str(i+1)+" parabola wrong!check!!!\n")
        results[i] -= tmp
        results[i] /= volume
        Y = results[i]
        p0 = [10]
        para = leastsq(error,p0,args=(X,Y))
        parameters[i] = para[0]*160.2
    return parameters

def getparameter3(results,types,numbers,max_strain,axis,bravi_type):
    #this function output the b in Ax=b
    step = 2*max_strain/(numbers-1)
    X = np.array([-max_strain+i*step for i in range(numbers) ])
    volume = getvolume(axis,bravi_type)
    parameters = np.zeros(types)
    for i in range(types):
        tmp = results[i,int((numbers-1)/2)]
        for j in range(numbers):
            if results[i,j] < tmp:
                print("type"+str(i+1)+" parabola wrong!check!!!\n")
        results[i] -= tmp
        results[i] /= volume
        Y = results[i]
        p0 = [10,10,10]
        para = leastsq(error3,p0,args=(X,Y))
        parameters[i] = para[0][1]*160.2
    return parameters

def getparameter4(results,types,numbers,max_strain,axis,bravi_type):
    #this function output the b in Ax=b
    step = 2*max_strain/(numbers-1)
    X = np.array([-max_strain+i*step for i in range(numbers) ])
    volume = getvolume(axis,bravi_type)
    parameters = np.zeros(types)
    for i in range(types):
        tmp = results[i,int((numbers-1)/2)]
        for j in range(numbers):
            if results[i,j] < tmp:
                print("type"+str(i+1)+" parabola wrong!check!!!\n")
        results[i] -= tmp
        results[i] /= volume
        Y = results[i]
        p0 = [10,10,10]
        para = leastsq(error3,p0,args=(X,Y))
        parameters[i] = para[0][2]*160.2
    return parameters        

def getmodulus(parameters,bravi_type):
    #this function get the modulus
    b = parameters
    if bravi_type == "cubic":
        #c44 c11 c12
        a = np.array([[1.5,0,0],[0,1,1],[0,1.5,3]])
        tmp = solve(a,b)
        c44,c11,c12 = tmp
        modulus = np.array([[c11,c12,c12,0,0,0],[c12,c11,c12,0,0,0],[c12,c12,c11,0,0,0],\
                [0,0,0,c44,0,0],[0,0,0,0,c44,0],[0,0,0,0,0,c44]])

    elif bravi_type == "hex":
        #c11 c12 c13 c33 c44
        a = np.array([[1,1,0,0,0],[0.25,-0.25,0,0,0],[0,0,0,0.5,0],[0,0,0,0,1],\
                [1,1,2,0.5,0]])
        tmp = solve(a,b)
        c11,c12,c13,c33,c44 = tmp
        modulus = np.array([[c11,c12,c13,0,0,0],[c12,c11,c13,0,0,0],[c13,c13,c33,0,0,0],\
                [0,0,0,c44,0,0],[0,0,0,0,c44,0],[0,0,0,0,0,(c11-c12)/2]])
    elif bravi_type == "trig6":
        #c11 c12 c13 c33 c44 c14
        a = np.array([[1,1,0,0,0,0],[0.25,-0.25,0,0,0,0],[0,0,0,0.5,0,0],[0,0,0,0,1,0],\
                [1,1,2,0.5,0,0],[0,0,0,0,0,1]])
        tmp = solve(a,b)
        c11,c12,c13,c33,c44,c14 = tmp
        modulus = np.array([[c11.c12,c13,c14,0,0],[c12,c11,c13,-c14,0,0],[c13,c13,c33,0,0,0],\
                [c14,-c14,0,c44,0,0],[0,0,0,0,c44,c14],[0,0,0,0,c14,(c11-c12)/2]])
    elif bravi_type == "trig8":
        #c11 c12 c13 c33 c44 c14 c15 c45
        a = np.array([[1,1,0,0,0,0,0,0],[0.25,-0.25,0,0,0,0,0,0],[0,0,0,0.5,0,0,0,0],[0,0,0,0,1,0,0,0],\
                [1,1,2,0.5,0,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,-1,0],[0,0,0,0,0,0,0,-1]])
        tmp = solve(a,b)
        c11,c12,c13,c33,c44,c14,c15,c45 = tmp
        modulus = np.array([[c11,c12,c13,c14,c15,0],[c12,c11,c13,-c14,-c15,0],[c13,c13,c33,0,0,0],\
                [c14,-c14,0,c44,0,-c45],[c15,-c15,0,0,c44,c14],[0,0,0,-c45,c14,(c11-c12)/2]])
    elif bravi_type == "tetra6":
        #c11 c12 c13 c33 c44 c66
        a = np.array([[1,1,0,0,0,0],[0,0,0,0,0,0.5],[0,0,0,0.5,0,0],[0,0,0,0,1,0],\
                [1,1,2,0.5,0,0],[0.5,0,1,0.5,0,0]])
        tmp = solve(a,b)
        c11,c12,c13,c33,c44,c66 = tmp
        modulus = np.array([[c11,c12,c13,0,0,0],[c12,c11,c13,0,0,0],[c13,c13,c33,0,0,0],\
                [0,0,0,c44,0,0],[0,0,0,0,c44,0],[0,0,0,0,0,c66]])
    elif bravi_type == "tetra7":
        #c11 c12 c13 c16 c33 c44 c66
        a = np.array([[1,1,0,0,0,0,0],[0,0,0,0,0,0,0.5],[0,0,0,0,0.5,0,0],[0,0,0,0,0,1,0],\
                [1,1,2,0,0.5,0,0],[0.5,0,1,0,0.5,0,0,0],[0,0,0,1,0,0,0]])
        tmp = solve(a,b)
        c11,c12,c13,c16,c33,c44,c66 = tmp
        modulus = np.array([[c11,c12,c13,0,0,c16],[c12,c11,c13,0,0,-c16],[c13,c13,c33,0,0,0],\
                [0,0,0,c44,0,0],[0,0,0,0,c44,0],[c16,-c16,0,0,0,c66]])
    elif bravi_type == "ortho":
        #c11 c22 c33 c44 c55 c66 c12 c13 c23
        a = np.array([[0.5,0,0,0,0,0,0,0,0],[0,0.5,0,0,0,0,0,0,0],[0,0,0.5,0,0,0,0,0,0],\
                [0,0,0,0.5,0,0,0,0,0],[0,0,0,0,0.5,0,0,0,0],[0,0,0,0,0,0.5,0,0,0],\
                [0.5,0.5,0,0,0,0,1,0,0],[0,0.5,0.5,0,0,0,0,0,1],[0.5,0,0.5,0,0,0,0,1,0]])
        tmp = solve(a,b)
        c11,c22,c33,c44,c55,c66,c12,c13,c23 = tmp
        modulus = np.array([[c11,c12,c13,0,0,0],[c12,c22,c23,0,0,0],[c13,c23,c33,0,0,0],\
                [0,0,0,c44,0,0],[0,0,0,0,c55,0],[0,0,0,0,0,c66]])
    elif bravi_type == "mono":
        #c11 c22 c33 c44 c55 c66 c12 c13 c16 c23 c26 c36 c45
        a = np.array([[0.5,0,0,0,0,0,0,0,0,0,0,0,0],\
                [0,0.5,0,0,0,0,0,0,0,0,0,0,0],\
                [0,0,0.5,0,0,0,0,0,0,0,0,0,0],\
                [0,0,0,0.5,0,0,0,0,0,0,0,0,0],\
                [0,0,0,0,0.5,0,0,0,0,0,0,0,0],\
                [0,0,0,0,0,0.5,0,0,0,0,0,0,0],\
                [0.5,0.5,0,0,0,0,1,0,0,0,0,0,0],\
                [0,0.5,0.5,0,0,0,0,0,0,1,0,0,0],\
                [0.5,0,0.5,0,0,0,0,1,0,0,0,0,0],\
                [0,0,0,0.5,0.5,0,0,0,0,0,0,0,1],\
                [0.5,0,0,0,0,0.5,0,0,1,0,0,0,0],\
                [0,0.5,0,0,0,0.5,0,0,0,0,1,0,0],\
                [0,0,0.5,0,0,0.5,0,0,0,0,0,1,0]])
        tmp = solve(a,b)
        c11,c22,c33,c44,c55,c66,c12,c13,c16,c23,c26,c36,c45 = tmp
        modulus = np.array([[c11,c12,c13,0,0,c16],[c12,c22,c23,0,0,c26],[c13,c23,c33,0,0,c36],\
                [0,0,0,c44,c45,0],[0,0,0,c45,c55,0],[c16,c26,c36,0,0,c66]])
    elif bravi_type == "tric":
        #c11 c22 c33 c44 c55 c66 c12 c13 c14 c15 c16 c23 c24 c25 c26 c34 c35 c36 c45 c46 c56
        a = np.array([[0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
                [0,0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
                [0,0,0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
                [0,0,0,0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
                [0,0,0,0,0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
                [0,0,0,0,0,0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
                [0.5,0.5,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
                [0,0.5,0.5,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],\
                [0.5,0,0.5,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],\
                [0,0,0,0.5,0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],\
                [0.5,0,0,0,0,0.5,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],\
                [0,0.5,0,0,0,0.5,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],\
                [0.5,0,0,0.5,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],\
                [0.5,0,0,0,0.5,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],\
                [0,0.5,0,0.5,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],\
                [0,0.5,0,0,0.5,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],\
                [0,0,0.5,0.5,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],\
                [0,0,0.5,0,0.5,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],\
                [0,0,0,0.5,0,0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],\
                [0,0,0,0,0.5,0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],\
                [0,0,0.5,0,0,0.5,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]])
        tmp = solve(a,b)
        c11,c22,c33,c44,c55,c66,c12,c13,c14,c15,c16,c23,c24,c25,c26,c34,c35,c36,c45,c46,c56 = tmp
        modulus = np.array([[c11,c12,c13,c14,c15,c16],[c12,c22,c23,c24,c25,c26],[c13,c23,c33,c34,c35,c36],\
                [c14,c24,c34,c44,c45,c46],[c15,c25,c35,c45,c55,c56],[c16,c26,c36,c46,c56,c66]])
    elif bravi_type == "iso":
        #c11 c12
        a = np.array([[0.5,0],[0.25,-0.25]])
        tmp = solve(a,b)
        c11,c12 = tmp
        modulus = np.array([[c11,c12,c12,0,0,0],[c12,c11,c12,0,0,0],[c12,c12,c11,0,0,0],\
                [0,0,0,(c11-c12)/2,0,0],[0,0,0,0,(c11-c12)/2,0],[0,0,0,0,0,(c11-c12)/2]])
        #2d block
    elif bravi_type == "sq":
        #c11 c12 c33
        a = np.array([[1,0,0],[1,1,0],[0,0,1]])
        tmp = solve(a,b)
        c11,c12,c33 = tmp
        modulus = np.array([[c11,c12,0],[c12,c11,0],[0,0,c33]])
    elif bravi_type == "hexa":
        #c11 c12
        a = np.array([[1,1],[0.25,-0.25]])
        tmp = solve(a,b)
        c11,c12 = tmp
        modulus = np.array([[c11,c12,0],[c12,c11,0],[0,0,0.5*(c11-c12)]])
    elif bravi_type == "rec":
        #c11 c22 c33 c12
        a = np.array([[0.5,0,0,0],[0,0.5,0,0],[0,0,0.5,0],[0.5,0.5,0,1]])
        tmp = solve(a,b)
        c11,c22,c33,c12 = tmp
        modulus = np.array([[c11,c12,0],[c12,c22,0],[0,0,c33]])
    elif bravi_type == "obl":
        #c11 c22 c33 c12 c13 c23
        a = np.array([[0.5,0,0,0,0,0],[0,0.5,0,0,0,0],[0,0,0.5,0,0,0],\
                [0.5,0.5,0,1,0,0],[0.5,0,0.5,0,1,0],[0,0.5,0.5,0,0,1]])
        tmp = solve(a,b)
        c11,c22,c33,c12,c13,c23 = tmp
        modulus = np.array([[c11,c12,c13],[c12,c22,c23],[c13,c23,c33]])
    elif bravi_type == "cubic3rd":
        #c111 c112 c144 c155 c456 c123
        a = np.array([[1/6,0,0,0,0,0],[1/3,1,0,0,0,0],[1/6,0,2,0,0,0],\
                [1/6,0,0,2,0,0],[0,0,0,0,8,0],[0.5,3,0,0,0,1]])
        tmp = solve(a,b)
        c111,c112,c144,c155,c456,c123 = tmp
        modulus = np.array([c111,c112,c144,c155,c456,c123])
    elif bravi_type == "cubic4rd":
        #c1111 c1112 c1122 c1144 c4444 c1155 c4455 c1266 c1255 c1456 c1123
        a = np.array([[1/24,0,0,0,0,0,0,0,0,0,0],[1/12,1/3,1/4,0,0,0,0,0,0,0,0],\
                [1/12,-1/3,1/4,0,0,0,0,0,0,0,0],[1/24,0,0,1,2/3,0,0,0,0,0,0],\
                [1/24,0,0,0,2/3,1,0,0,0,0,0],[0,0,0,0,2,0,12,0,0,0,0],\
                [0,0,0,0,2/3,0,0,0,0,0,0],[1/12,1/3,1/4,0,2/3,2,0,2,0,0,0],\
                [1/12,1/3,1/4,1,2/3,1,0,0,2,0,0],[1/24,0,0,1,2,2,12,0,0,8,0],\
                [1/8,1,3/4,0,0,0,0,0,0,0,3/2]])
        tmp = solve(a,b)
        modulus = tmp
    else:
        print("chosen right bravi type")

    return modulus

def getmecha(modulus):
    #this function get the mechanical properties
    c = modulus
    s = np.linalg.inv(c)
    vogit = np.zeros(4)
    vogit[0] = 1/9*(c[0,0]+c[1,1]+c[2,2])+2/9*(c[0,1]+c[1,2]+c[2,0])
    vogit[1] = 1/15*(c[0,0]+c[1,1]+c[2,2])-1/15*(c[0,1]+c[1,2]+c[2,0])+1/5*(c[3,3]+c[4,4]+c[5,5])
    vogit[2] = 1/(1/(3*vogit[1])+1/(9*vogit[0]))
    vogit[3] = 0.5*(1-3*vogit[1]/(3*vogit[0]+vogit[1]))
    reuss = np.zeros(4)
    reuss[0] = 1/((s[0,0]+s[1,1]+s[2,2])+2*(s[0,1]+s[1,2]+s[2,0]))
    reuss[1] = 15/(4*(s[0,0]+s[1,1]+s[2,2])-4*(s[0,1]+s[1,2]+s[2,0])+3*(s[3,3]+s[4,4]+s[5,5]))
    reuss[2] = 1/(1/(3*reuss[1])+1/(9*reuss[0]))
    reuss[3] = 0.5*(1-3*reuss[1]/(3*reuss[0]+reuss[1]))
    hill = np.zeros(4)
    hill = (vogit+reuss)/2
    hill[2] = 1/(1/(3*hill[1])+1/(9*hill[0]))
    hill[3] = 0.5*(1-3*hill[1]/(3*hill[0]+hill[1]))

    return s,vogit,reuss,hill

def getvolume(axis,bravi_type):
    #this function output the volume of cell
    tmp = np.array([axis[0,1]*axis[1,2]-axis[0,2]*axis[1,1],axis[0,2]*axis[1,0]-axis[0,0]*axis[1,2],\
            axis[0,0]*axis[1,1]-axis[0,1]*axis[1,0]])
    tmp = abs(np.dot(tmp,axis[2]))
    f = open("orig/POSCAR","r")
    scale = float(f.readlines()[1])
    f.close()
    tmp *= scale**3
    #for 2d materials, change the volume to area
    if bravi_type == "sq" or bravi_type == "hexa" or bravi_type == "rec" or bravi_type == "obl":
        tmp /= np.linalg.norm(axis[2])*scale
        tmp *= 10.0  #transfer GPa*A to GPa*nm 
    return tmp

def func(params,x):
    return params*x**2

def error(params,x,y):
    return func(params,x)-y

def func3(params,x):
    a,b,c = params
    return a*x**2+b*x**3+c*x**4

def error3(params,x,y):
    return func3(params,x)-y

def checkstable(modulus,bravi_type):
    #check whether this system is mechanical stable
    c = modulus
    b = False
    if bravi_type == "cubic":
        if c[0,0]>0 and c[3,3]>0 and c[0,0]>abs(c[0,1]) and c[0,0]+2*c[0,1]>0:
            b = True
    elif bravi_type == "hex":
        if c[3,3]>0 and c[0,0]>abs(c[0,1]) and (c[0,0]+2*c[0,1])*c[2,2]>2*c[0,2]**2:
            b = True
    elif bravi_type == "tetra6":
        if c[3,3]>0 and c[0,0]>abs(c[0,1]) and (c[0,0]+2*c[0,1])*c[2,2]>2*c[0,2]**2 and c[5,5]>0:
            b = True
    elif bravi_type == "tetra7":
        if c[0,0]>abs(c[0,1]) and 2*c[0,2]**2<c[2,2]*(c[0,0]+c[0,1]) and c[3,3]>0 and 2*c[0,5]**2<c[5,5]*(c[0,0]-c[0,1]):
            b = True
    elif bravi_type == "trig6" or bravi_type == "trig8":
        if c[0,0]>0 and c[2,2]>0 and c[3,3]>0 and c[5,5]>0 and c[0,0]-c[0,1]>0 and \
                c[0,0]+c[2,2]-2*c[0,2]>0 and 2*(c[0,0]+c[0,1])+c[2,2]+4*c[0,2] > 0:
                    b = True
    elif bravi_type == "ortho":
        if c[0,0]>0 and c[1,1]>0 and c[2,2]>0 and c[3,3]>0 and c[4,4]>0 and c[5,5]>0 and \
                c[0,0]+c[1,1]+c[2,2]+2*(c[0,1]+c[0,2]+c[1,2])>0 and c[0,0]+c[1,1]-2*c[0,1]>0 and \
                c[0,0]+c[2,2]-2*c[0,2]>0 and c[1,1]+c[2,2]-2*c[1,2]>0:
                    b = True
    elif bravi_type == "mono":
        g = c[0,0]*c[1,1]*c[2,2]-c[0,0]*c[1,2]**2-c[1,1]*c[0,2]**2-c[2,2]*c[0,1]**2+2*c[0,1]*c[0,2]*c[1,2]
        if c[0,0]>0 and c[1,1]>0 and c[2,2]>0 and c[3,3]>0 and c[4,4]>0 and c[5,5]>0 and \
                c[0,0]+c[1,1]+c[2,2]+2*(c[0,1]+c[0,2]+c[1,2])>0 and c[2,2]*c[4,4]-c[2,4]**2>0 and \
                c[3,3]*c[5,5]-c[3,5]**2>0 and c[1,1]+c[2,2]-2*c[1,2]>0 and \
                c[1,1]*(c[2,2]*c[4,4]-c[2,4]**2)+2*c[1,2]*c[1,4]*c[2,4]-c[1,2]**2*c[4,4]-c[1,4]**2*c[2,2]>0 and \
                2*(c[0,4]*c[1,4]*(c[2,2]*c[0,1]-c[0,2]*c[1,2])+c[0,4]*c[2,4]*(c[1,1]*c[0,2]-c[0,1]*c[1,2])+\
                c[1,4]*c[2,4]*(c[0,0]*c[1,2]-c[0,1]*c[0,2]))-(c[0,4]**2*(c[1,1]*c[2,2]-c[1,2]**2)+ \
                c[1,4]**2*(c[0,0]*c[2,2]-c[0,2]**2)+c[2,4]**2*(c[0,0]*c[1,1]-c[0,1]**2))+c[4,4]*g > 0:
                    b = True
    elif bravi_type == "sq":
        if c[0,0]>0 and c[2,2]>0 and c[0,0]+c[0,1]>0 and c[0,0]-c[0,1]>0 :
            b = True
    elif bravi_type == "hexa":
        if c[0,0]>0 and c[0,0]+c[0,1]>0 and c[0,0]-c[0,1]>0:
            b = True
    elif bravi_type == "rec":
        if c[0,0]>0 and c[2,2]>0 and c[0,0]*c[1,1]>c[0,1]**2 :
            b = True
    elif bravi_type == "obl":
        if c[0,0]>0 and c[0,0]*c[1,1]>c[0,1]**2 and np.linalg.det(c)>0:
            b = True
    else:
        print("Emmmm,such low symmetry structure it is rather importtant than all the Cij>0")
    
    return b

def caleos(strain_tensor, axis, results, cal_type):
    #this function fitting the EOS
    volume = getvolume(axis, "cubic") #why this function need inputing bravis type?how stupid i am..
    X = np.array([i**3*volume for i in strain_tensor])
    Y = np.array(results[0])
    CX = np.linspace(np.min(X)-1,np.max(X)+1, 1000)
    if cal_type == "Murn":
        p0 = [2,2,2,2]
        para = leastsq(murnerror,p0,args=(X,Y),maxfev=500000)
        a,b,c,d = para[0]
        B1 = 1.0 - b
        B0 = B1*c
        V0 = (a*B1*(B1-1)/B0)**(1/B1)
        B0 *= 160.2
        CY = murn([a,b,c,d],CX)
        label = "Murnaghan EOS"
    elif cal_type == "BM2":
        popt, pcov = curve_fit(BM2,X,Y,p0=[0.9,71,-100])
        B0, V0,E0 = popt[0],popt[1],popt[2]
        B0 *= 160.2
        CY = BM2(CX,B0/160.2,V0,E0)
        label = "second order Birch-Murnaghan EOS"
    elif cal_type == "BM3":
        popt, pcov = curve_fit(BM3,X,Y,p0=[0.9,-0.2,71,-100])
        B0,B1,V0,E0 = popt
        CY = BM3(CX,B0,B1,V0,E0)
        label = "third order Birch-Murnaghan EOS"
        B0 *= 160.2
    elif cal_type == "BM4":
        popt, pcov = curve_fit(BM4,X,Y,p0=[0.9,-0.2,0.2,71,-100])
        B0,B1,B2,V0,E0 = popt
        CY = BM4(CX,B0,B1,B2,V0,E0)
        label = "fourth order Birch-Murnaghan EOS"
        B0 *= 160.2
    elif cal_type == "PT2":
        popt, pcov = curve_fit(PT2,X,Y,p0=[0.9,71,-100])
        B0,V0,E0 = popt
        CY = PT2(CX,B0,V0,E0)
        label = "second order Poirier-Tarantola EOS"
        B0 *= 160.2
    elif cal_type == "PT3":
        popt, pcov = curve_fit(PT3,X,Y,p0=[0.9,-0.1,71,-100])
        B0,B1,V0,E0 = popt
        CY = PT3(CX,B0,B1,V0,E0)
        label = "third order Poirier-Tarantola EOS"
        B0 *= 160.2
    elif cal_type == "PT4":
        popt, pcov = curve_fit(PT4,X,Y,p0=[0.9,-0.1,-0.1,71,-100])
        B0,B1,B2,V0,E0 = popt
        CY = PT4(CX,B0,B1,B2,V0,E0)
        label = "fourth order Poirier-Tarantola EOS"
        B0 *= 160.2
    elif cal_type == "Vinet":
        popt, pcov = curve_fit(Vinet,X,Y,p0=[0.9,-0.1,71,-100])
        B0,B1,V0,E0 = popt
        CY = Vinet(CX,B0,B1,V0,E0)
        label = "Vinet EOS"
        B0 *= 160.2

    return B0, V0, CX, CY ,X, Y,label

def murn(params,x):
    a,b,c,d= params
    return a*x**b+c*x+d
def murnerror(params,x,y):
    return murn(params, x)-y
def BM2(x,B0,V0,E0):
    return E0 + 9/8*B0*V0**(7/3)*((1/x)**(2/3)-1/V0**(2/3))**2
def BM3(x,B0,B1,V0,E0):
    return E0+9/16*V0*B0*((x/V0)**(2/3)-1)**2/(x/V0)**(7/3)*\
            ((x/V0)**(1/3)*(B1-4)-(x/V0)*(B1-6))
def BM4(x,B0,B1,B2,V0,E0):
    f = 1/2*((V0/x)**(2/3)-1)
    H = B0*B2+B1**2
    return E0+3/8*V0*B0*f**2*((9*H-63*B1+143)*f**2+12*(B1-4)*f+12)
def PT2(x,B0,V0,E0):
    f = (np.log(x/V0))*1/3
    return E0+9/2*B0*V0*f**2
def PT3(x,B0,B1,V0,E0):
    f = 1/3*np.log(x/V0)
    return E0+9/2*B0*V0*f**2*((B1+2)*f+1)
def PT4(x,B0,B1,B2,V0,E0):
    f = 1/3*np.log(x/V0)
    H = B2*B0+B1**2
    return E0+9*B0*V0*f**2*(3*(H+3*B1+3)*f**2+4*(B1+2)*f+4)
def Vinet(x,B0,B1,V0,E0):
    ff = (x/V0)**(1/3)
    return E0+4*B0*V0/(B1-1)**2-2*B0*V0/(B1-1)**2*(3*(B1-1)*(ff-1)+2)*\
            np.exp(-3/2*(B1-1)*(ff-1))
