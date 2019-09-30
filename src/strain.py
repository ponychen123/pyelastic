#!/usr/bin/python3
#this modulue add strain tensor to the system
#author:ponychen
#email:1709821294@outlook.com
#20190831

import numpy as np

def addstrain(max_strain,numbers,bravi_type):
    #this function output the strain tensor
    step = 2*max_strain/(numbers-1) #get the step of applied strain
    sampling = [-max_strain+i*step for i in range(numbers)] #a list storing all the strain step
    if bravi_type == "cubic":
        #c44 c11 c12
        added = np.zeros([3,numbers,3,3])
        added[0] = spc("000111",sampling)
        added[1] = spc("110000",sampling)
        added[2] = spc("111000",sampling)
    elif bravi_type == "hex":
        #c11 c12 c13 c33 c44
        added = np.zeros([5,numbers,3,3])
        added[0] = spc("110000",sampling)
        added[1] = spc("000001",sampling)
        added[2] = spc("001000",sampling)
        added[3] = spc("000110",sampling)
        added[4] = spc("111000",sampling)
    elif bravi_type == "trig6":
        #c11 c12 c13 c33 c44 c14
        added = np.zeros([6,numbers,3,3])
        added[0] = spc("110000",sampling)
        added[1] = spc("000001",sampling)
        added[2] = spc("001000",sampling)
        added[3] = spc("000110",sampling)
        added[4] = spc("111000",sampling)
        added[5] = spc("000011",sampling)
    elif bravi_type == "trig8":
        #c11 c12 c13 c33 c44 c14 c15 c45
        added = np.zeros([8,numbers,3,3])
        added[0] = spc("110000",sampling)
        added[1] = spc("000001",sampling)
        added[2] = spc("001000",sampling)
        added[3] = spc("000110",sampling)
        added[4] = spc("111000",sampling)
        added[5] = spc("000011",sampling)
        added[6] = spc("010001",sampling)
        added[7] = spc("000101",sampling)
    elif bravi_type == "tetra6":
        #c11 c12 c66 c33 c44 c13 
        added = np.zeros([6,numbers,3,3])
        added[0] = spc("110000",sampling)
        added[1] = spc("000001",sampling)
        added[2] = spc("001000",sampling)
        added[3] = spc("000110",sampling)
        added[4] = spc("111000",sampling)
        added[5] = spc("011000",sampling)
    elif bravi_type == "tetra7":
        #c11 c12 c66 c33 c44 c13 c16
        added = np.zeros([7,numbers,3,3])
        added[0] = spc("110000",sampling)
        added[1] = spc("000001",sampling)
        added[2] = spc("001000",sampling)
        added[3] = spc("000110",sampling)
        added[4] = spc("111000",sampling)
        added[5] = spc("011000",sampling)   
        added[6] = spc("100001",sampling)
    elif bravi_type == "ortho":
        #c11 c22 c33 c44 c55 c66 c12 c13 c23
        added = np.zeros([9,numbers,3,3])
        added[0] = spc("100000",sampling)
        added[1] = spc("010000",sampling)
        added[2] = spc("001000",sampling)
        added[3] = spc("000100",sampling)
        added[4] = spc("000010",sampling)
        added[5] = spc("000001",sampling)
        added[6] = spc("110000",sampling)
        added[7] = spc("011000",sampling)
        added[8] = spc("101000",sampling)
    elif bravi_type == "mono":
        #c11 c22 c33 c44 c55 c66 c12 c13 c16 c23 c26 c36 c45 
        added = np.zeros([13,numbers,3,3])
        added[0] = spc("100000",sampling)
        added[1] = spc("010000",sampling)
        added[2] = spc("001000",sampling)
        added[3] = spc("000100",sampling)
        added[4] = spc("000010",sampling)
        added[5] = spc("000001",sampling)
        added[6] = spc("110000",sampling)
        added[7] = spc("011000",sampling)
        added[8] = spc("101000",sampling)
        added[9] = spc("000110",sampling)
        added[10] = spc("100001",sampling)
        added[11] = spc("010001",sampling)
        added[12] = spc("001001",sampling)
    elif bravi_type == "tric":
        #c11 c12 c13 c14 c15 c16 c22 c23 c24 c25 c26 c33 c34 c35 c36 c44 c45 c46 c55 c56 c66
        added = np.zeros([21,numbers,3,3])
        added[0] = spc("100000",sampling)
        added[1] = spc("010000",sampling)
        added[2] = spc("001000",sampling)
        added[3] = spc("000100",sampling)
        added[4] = spc("000010",sampling)
        added[5] = spc("000001",sampling)
        added[6] = spc("110000",sampling)
        added[7] = spc("011000",sampling)
        added[8] = spc("101000",sampling)
        added[9] = spc("000110",sampling)
        added[10] = spc("100001",sampling)
        added[11] = spc("010001",sampling)
        added[12] = spc("100100",sampling)
        added[13] = spc("100010",sampling)
        added[14] = spc("010100",sampling)
        added[15] = spc("010010",sampling)
        added[16] = spc("001100",sampling)
        added[17] = spc("001010",sampling)
        added[18] = spc("000101",sampling)
        added[19] = spc("000011",sampling)
        added[20] = spc("001001",sampling)
    elif bravi_type == "iso":
        #c11 c12
        added = np.zeros([2,numbers,3,3])
        added[0] = spc("100000",sampling)
        added[1] = spc("000100",sampling)
        #following 2d block
    elif bravi_type == "sq":
        #C11 C12 C33
        added = np.zeros([3,numbers,3,3])
        added[0] = spc("100000",sampling)
        added[1] = spc("110000",sampling)
        added[2] = spc("000001",sampling)
    elif bravi_type == "hexa":
        #C11 C12 
        added = np.zeros([2,numbers,3,3])
        added[0] = spc("110000",sampling)
        added[1] = spc("000001",sampling)
    elif bravi_type == "rec":
        #C11 C22 C12 C33
        added = np.zeros([4,numbers,3,3])
        added[0] = spc("100000",sampling)
        added[1] = spc("010000",sampling)
        added[2] = spc("110000",sampling)
        added[3] = spc("000001",sampling)
    elif bravi_type == "obl":
        #C11 C22 C33 C12 C13 C23
        added = np.zeros([6,numbers,3,3])
        added[0] = spc("100000",sampling)
        added[1] = spc("010000",sampling)
        added[2] = spc("000001",sampling)
        added[3] = spc("110000",sampling)
        added[4] = spc("100001",sampling)
        added[5] = spc("010001",sampling)
    elif bravi_type == "cubic3rd":
        #c111 c112 c144 c155 c123 c456 
        added = np.zeros([6,numbers,3,3])
        added[0] = spc("100000",sampling)
        added[1] = spc("110000",sampling)
        added[2] = spc("100200",sampling)
        added[3] = spc("100002",sampling)
        added[4] = spc("000222",sampling)
        added[5] = spc("111000",sampling)
    elif bravi_type == "cubic4rd":
        #c1111 c1112 c1122 c1144 c4444 c1155 c4455 c1266 c1255 c1456 c1123
        added = np.zeros([11,numbers,3,3])
        added[0] = spc("100000",sampling)
        added[1] = spc("110000",sampling)
        added[2] = spc("190000",sampling)
        added[3] = spc("100200",sampling)
        added[4] = spc("100002",sampling)
        added[5] = spc("000222",sampling)
        added[6] = spc("000200",sampling)
        added[7] = spc("110002",sampling)
        added[8] = spc("110200",sampling)
        added[9] = spc("100222",sampling)
        added[10] = spc("111000",sampling)
    else:
        print("chose correct bravi type")

    return added,sampling

def gettensor(added,axis,numbers):
    #this function outpput the distorted axis tensor
    for i in range(len(added)):
        for j in range(numbers):
            added[i,j] = np.dot(axis,added[i,j])

    return added

def spc(strain_type,sampling):
    #this function create specific strain teansor ,strain_type is a string with len=6
    a1 = np.array([[1,0,0],[0,0,0],[0,0,0]])
    a2 = np.array([[0,0,0],[0,1,0],[0,0,0]])
    a3 = np.array([[0,0,0],[0,0,0],[0,0,1]])
    a4 = np.array([[0,0,0],[0,0,0.5],[0,0.5,0]])
    a5 = np.array([[0,0,0.5],[0,0,0],[0.5,0,0]])
    a6 = np.array([[0,0.5,0],[0.5,0,0],[0,0,0]])
    b = list(map(int,strain_type))
    for i in range(6):
        if b[i] == 9:
            b[i] = -1
    a = a1*b[0]+a2*b[1]+a3*b[2]+a4*b[3]+a5*b[4]+a6*b[5]
    tmp = []
    for i in sampling:
        tmp.append(a*i+np.eye(3))

    return tmp

