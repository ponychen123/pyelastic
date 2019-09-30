#!/usr/bin/python3
#this script read stiffness tensor from modulus.txt and output the necassary
#mechanical properties information
#author:ponychen

import numpy as np
import iio
import analy

#read the bravis type from input.elastic
f = open("input.elastic","r")
inputfile = f.readlines()
bravi_type = inputfile[26].split()[0]
f.close()

#read the stiffness tensor from modulus.txt
f = open("modulus.txt","r")
inputfile = f.readlines()
modulus = []
for i in inputfile:
    modulus.append(list(map(float,i.split())))
modulus = np.array(modulus)
f.close()

#get the average mechanical properties for polycrystalline
S,vogit,reuss,hill = analy.getmecha(modulus)

#check whether these system is stable
ifstable = analy.checkstable(modulus,bravi_type)
#output the final result
iio.finaloutput(modulus,S,vogit,reuss,hill,ifstable)
