#!/usr/bin/python3
#this script read stiffness tensor from modulus.txt and output the necassary
#mechanical properties information for two-dimensional materials
#author:ponychen

import numpy as np
import iio
import analy

#read the bravis type from input.elastic
f = open("input.elastic","r")
inputfile = f.readlines()
bravi_type = inputfile[28].split()[0]
f.close()

#read the stiffness tensor from modulus.txt
f = open("modulus.txt","r")
inputfile = f.readlines()
modulus = []
for i in inputfile:
    modulus.append(list(map(float,i.split())))
modulus = np.array(modulus)
f.close()

#check whether these system is stable
ifstable = analy.checkstable(modulus,bravi_type)
#output the final result
iio.d2output(modulus,ifstable)
