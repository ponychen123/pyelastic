#!/usr/bin/python3
#this module calculate the fourth order elastic constants
#author:ponychen
#email:18709821294@outlook.com
#20190929

import transfer
import numpy as np
import iio
import strain
import analy
import subprocess

#some default parameters
f = open("input.elastic","r")
inputfile = f.readlines()
f.close()
mode = int(inputfile[47].split()[0])  #1 for create calculation input files and 2 for calculate modulus
max_strain = float(inputfile[48].split()[0])  #the max applied strain used, carefully choose
numbers = int(inputfile[49].split()[0])  #the number of sampling points
input_type = inputfile[50].split()[0]  #"qe" "vasp" "elk"or "kkr", as far support these three
bravi_type = inputfile[51].split()[0] #"cubic4rd"
kkr_atoms = int(inputfile[52].split()[0])  #if you set input_type equal to kkr, the kkr_atoms means the number of total atoms

#reading the file, only support for fractional format, this is important
if mode == 1:
    if input_type == "vasp":
        axis, data = iio.poscarread() #data are the whole POSCAR
    elif input_type == "kkr":
        subprocess.call("./src/kkr2pos.sh "+"orig/in.inp "+str(kkr_atoms),shell=True) #you should specify the name to in.inp
        subprocess.call("mv POSCAR ./orig/POSCAR", shell=True)
        axis, data = iio.poscarread()
    elif input_type == "qe":
        subprocess.call("./src/qe2vasp.sh "+"orig/in.qe", shell=True)
        subprocess.call("mv POSCAR ./orig/POSCAR", shell=True)
        axis, data = iio.poscarread()
    elif input_type == "elk":
        transfer.elk2pos()
        axis, data = iio.poscarread()
    else:
        print("please specift correct input type.")
    #create series of applied strain matrix
    #sampling is the list storing all the strain
    strain_tensor, sampling = strain.addstrain(max_strain,numbers,bravi_type)
    
    #appliying the strain tensor to axis tensor
    axis_tensor = strain.gettensor(strain_tensor,axis,numbers)

    #output the files and you should doing the calculation
    if input_type == "vasp":
        iio.poscarout(axis_tensor,sampling,data)
    elif input_type == "kkr":
        iio.kkrout(axis_tensor,sampling)
    elif input_type == "qe":
        iio.qeout(axis_tensor,sampling)
    elif input_type == "elk":
        iio.elkout(axis_tensor,sampling)
    else:
        print("input right input_type")

elif mode == 2:
    if bravi_type == "cubic4rd":
        types = 11
    else:
        print("sorry,check your input bravi_type")

    #get the energy vs strain data from result
    results = iio.outread(types,numbers,input_type)

    #get the axis of undistored system
    axis = iio.poscarread()[0]
    #get the parameters of Ax =b
    parameters = analy.getparameter4(results,types,numbers,max_strain,axis,bravi_type)
    #get the modulus by parameters
    modulus = analy.getmodulus(parameters,bravi_type)
    #output the final result
    iio.finalout4rd(modulus)
else:
    print("please set mode = 1 or 2")
