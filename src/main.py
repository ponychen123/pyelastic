#!/usr/bin/python3
#this is the main program of pyelastic
#author:ponychen
#email:18709821294@outlook.com
#20190831

import transfer
import numpy as np
import iio
import strain
import analy
import subprocess
import standard

#some default parameters
standarding = True # if false, you should make sure that your structure orientation is right
f = open("input.elastic","r")
inputfile = f.readlines()
f.close()
mode = int(inputfile[5].split()[0])  #1 for create calculation input files and 2 for calculate modulus
max_strain = float(inputfile[6].split()[0])  #the max applied strain used, carefully choose
numbers = int(inputfile[7].split()[0])  #the number of sampling points
input_type = inputfile[8].split()[0]  #"qe" "vasp" "elk"or "kkr", as far support these three
bravi_type = inputfile[9].split()[0] #"cubic","hex","trig6","trig8","tetra6","tetra7","ortho","mono","tric","iso"
kkr_atoms = int(inputfile[10].split()[0])  #if you set input_type equal to kkr, the kkr_atoms means the number of total atoms

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

    #standarize the axis 
    if standarding:
        axis = standard.get_standard(axis,bravi_type)

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
    if bravi_type == "cubic":
        types = 3
    elif bravi_type == "hex":
        types = 5
    elif bravi_type == "trig6" or bravi_type == "tetra6":
        types = 6
    elif bravi_type == "tetra7":
        types = 7
    elif bravi_type == "trig8":
        types = 8
    elif bravi_type == "ortho":
        types = 9
    elif bravi_type == "mono":
        types = 13
    elif bravi_type == "tric":
        types = 21
    elif bravi_type == "iso":
        types = 2
    else:
        print("sorry,check your input bravi_type")

    #get the energy vs strain data from result
    results = iio.outread(types,numbers,input_type)

    #get the axis of undistored system
    axis = iio.poscarread()[0]
    #get the parameters of Ax =b
    parameters = analy.getparameter(results,types,numbers,max_strain,axis,bravi_type)
    #get the modulus by parameters
    modulus = analy.getmodulus(parameters,bravi_type)
    #get the average mechanical properties for polycrystalline
    S,vogit,reuss,hill = analy.getmecha(modulus)
    #check whether these system is stable 
    ifstable = analy.checkstable(modulus,bravi_type)
    #output the final result
    iio.finaloutput(modulus,S,vogit,reuss,hill,ifstable)
else:
    print("please set mode = 1 or 2")
