#!/usr/bin/python3
#this module calculate solid equation of states
#author:ponychen
#email:18709821294@outlook.com
#20191118

import transfer
import numpy as np
import iio
import strain
import analy
import subprocess
import standard

#some default parameters
with open("input.elastic","r") as f:
    inputfile = f.readlines()
mode = int(inputfile[54].split()[0])  #1 for create calculation input files and 2 for calculate modulus
max_strain = float(inputfile[57].split()[0])  #the max applied strain used, carefully choose
numbers = int(inputfile[56].split()[0])  #the number of sampling points
input_type = inputfile[58].split()[0]  #"qe" "vasp" "elk"or "kkr", as far support these three
cal_type = inputfile[55].split()[0]

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
    strain_tensor, sampling = strain.addeosstrain(max_strain,numbers)
    
    #appliying the strain tensor to axis tensor
    axis_tensor = strain.geteostensor(strain_tensor,axis,numbers)

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
    types = 1

    #get the energy vs strain data from result
    results = iio.outread(types,numbers,input_type)

    #get the axis of undistored system
    axis = iio.poscarread()[0]
    #get the sampling
    strain_tensor, sampling = strain.addeosstrain(max_strain,numbers)
    #get the B0 B1
    B0, V0,CX,CY,X,Y,label = analy.caleos(strain_tensor,axis,results,cal_type)
    print("Bulk moduli : %9.2f GPa balance volume : %9.2f angstroms^3"\
            % (B0,V0))
    #output the EOS data
    iio.eosout(CX,CY,X,Y,label)
else:
    print("please set mode = 1 or 2")
