#/usr/bin/python3
#this modulue read and output the files
#author:ponychen
#email:18709821294@outlook.com
#20190831

import numpy as np
import os
import subprocess

def poscarread():
    #this function reading the no-strain POSCAR and get the axis matrix
    fileopen = open("orig/POSCAR","r")
    data = fileopen.readlines()
    axistmp = []
    for i in range(2,5):
        tmp = []
        tmp = list(map(float,data[i].split()))
        axistmp.append(tmp)
    axis = np.array(axistmp)
    fileopen.close()
    return axis,data

def poscarout(axis_tensor,sampling,data):
    #this function output all the POSCARs to their folder
    for i in range(len(axis_tensor)):
        name1 = "type"+str(i+1)
        os.system("mkdir "+name1)
        for j in range(len(sampling)):
            name2 = "type"+str(i+1)+"/"+str(j)
            os.system("mkdir "+name2)
            os.system("cp orig/INCAR orig/POTCAR orig/KPOINTS ./"+name2)
            f = open(name2+"/POSCAR","w+")
            for k in range(3):
                line = map(str, axis_tensor[i,j,k])
                line = " ".join(line)
                line += "\n"
                data[k+2] = line
            f.writelines(data)
            f.close()

def kkrout(axis_tensor,sampling):
    #this function output all the input file in.inp to their folder
    f = open("orig/in.inp","r")
    data = f.readlines()
    f.close()
    ai = int(subprocess.getoutput("grep -in 'aux' orig/in.inp | awk 'BEGIN{FS=\":\"}{print $1}'"))
    leng = float(data[ai+3])*0.5292
    for i in range(len(axis_tensor)):
        name1 = "type"+str(i+1)
        os.system("mkdir "+name1)
        for j in range(len(sampling)):
            name2 = "type"+str(i+1)+"/"+str(j)
            os.system("mkdir "+name2)
            os.system("cp orig/in.inp ./"+name2)
            f = open(name2+"/in.inp","w+")
            for k in range(3):
                line = map(str, axis_tensor[i,j,k]/leng)
                line = " ".join(line)
                line += "\n"
                data[k+ai] = line
            f.writelines(data)
            f.close()

def elkout(axis_tensor,sampling):
    #this function output all the input file elk.in to their folder
    f = open("orig/elk.in","r")
    data = f.readlines()
    f.close()
    ai = int(subprocess.getoutput("grep -in ^avec orig/elk.in | awk 'BEGIN{FS=\":\"}{print $1}'"))
    for i in range(len(axis_tensor)):
        name1 = "type"+str(i+1)
        os.system("mkdir "+name1)
        for j in range(len(sampling)):
            name2 = "type"+str(i+1)+"/"+str(j)
            os.system("mkdir "+name2)
            os.system("cp orig/elk.in ./"+name2)
            f = open(name2+"/elk.in","w+")
            for k in range(3):
                line = map(str, axis_tensor[i,j,k]/0.5292)
                line = " ".join(line)
                line += "\n"
                data[k+ai] = line
            f.writelines(data)
            f.close()

def qeout(axis_tensor,sampling):
    #this function output all the input file in.pw to their folder
    f = open("orig/in.pw","r")
    data = f.readlines()
    f.close()
    ai = int(subprocess.getoutput("grep -in 'CELL_PARA' orig/in.pw | awk 'BEGIN{FS=\":\"}{print $1}'"))
    data[ai-1] = "CELL_PARAMETERS angstrom\n"
    for i in range(len(axis_tensor)):
        name1 = "type"+str(i+1)
        os.system("mkdir "+name1)
        for j in range(len(sampling)):
            name2 = "type"+str(i+1)+"/"+str(j)
            os.system("mkdir "+name2)
            os.system("cp orig/INCAR orig/POTCAR orig/KPOINTS ./"+name2)
            f = open(name2+"/POSCAR","w+")
            for k in range(3):
                line = map(str, axis_tensor[i,j,k])
                line = " ".join(line)
                line += "\n"
                data[k+ai] = line
            f.writelines(data)
            f.close()

def outread(types,numbers,input_type):
    #read the result from Vasp calculation 
    result = np.zeros([types,numbers])
    for i in range(types):
        for j in range(numbers):
            if input_type == "vasp":
                name = "grep E0 ./type"+str(i+1)+"/"+str(j)+"/OSZICAR | tail -1 |awk '{print $5}'"
                result[i,j] = float(subprocess.getoutput(name))
            elif input_type == "kkr":
                name = "grep -v \"^&\" ./type"+str(i+1)+"/"+str(j)+"/pot.info | tail -1 | awk '{print $2}'"
                result[i,j] = float(subprocess.getoutput(name))*13.606  #change Ry to eV
            elif input_type == "qe":
                name = "grep ! ./type"+str(i+1)+"/"+str(j)+"/out.pw | tail -1 | awk '{print $5}'"
                result[i,j] = float(subprocess.getoutput(name))*13.606 #change Ry to eV
            elif input_type == "elk":
                name = "grep '^ total energy' ./type"+str(i+1)+"/"+str(j)+"/INFO.OUT | tail -1 | awk '{print $4}' "
                result[i,j] = float(subprocess.getoutput(name))*27.21138505 #change Ha to eV
            else:
                print("chosen right input_type")
    return result

def finaloutput(c,s,vogit,reuss,hill,ifstable):
    #this function output all the result to the file finalresult.txt
    f = open("finalresult.txt","w+")
    ff = open("modulus.txt","w+")
    c = c.tolist()
    s = s.tolist()
    f.write("the final mechanical result calculated by ponychen\n")
    f.write("Stiffness tensor C_ij (GPa)\n")
    for i in c:
        f.write("%9.2f  %9.2f  %9.2f  %9.2f  %9.2f  %9.2f\n" % (i[0],i[1],i[2],i[3],i[4],i[5]))
        ff.write("%9.2f  %9.2f  %9.2f  %9.2f  %9.2f  %9.2f\n" % (i[0],i[1],i[2],i[3],i[4],i[5]))
    ff.close()
    f.write("compliance tensor S_ij (GPa-1)\n")
    for i in s:
        f.write("%9.6f  %9.6f  %9.6f  %9.6f  %9.6f  %9.6f\n" % (i[0],i[1],i[2],i[3],i[4],i[5]))
    hc = [2*((vogit[1]/vogit[0])**2*vogit[1])**0.585-3,2*((reuss[1]/reuss[0])**2*reuss[1])**0.585-3,2*((hill[1]/hill[0])**2*hill[1])**0.585-3]
    ht = [0.92*(vogit[1]/vogit[0])**1.137*vogit[1]**0.708,0.92*(reuss[1]/reuss[0])**1.137*reuss[1]**0.708,0.92*(hill[1]/hill[0])**1.137*hill[1]**0.708]
    f.write("some mechanical properties for polycrystalline\n")
    f.write("  schem  |  Bulk K(GPa)  |  Shear G(GPa)  |  Young's E(GPa)  |  Possion's V  |  Vickers hardness (Chen)  |  Vickers hardness (Tian) \n")
    f.write("-----------------------------------------------------------------------------\n")
    f.write("  vogit  |  %9.2f  |  %9.2f  |  %9.2f  |  %9.2f  |  %9.2f  |  %9.2f\n" % (vogit[0],vogit[1],vogit[2],vogit[3],hc[0],ht[0]))
    f.write("  reuss  |  %9.2f  |  %9.2f  |  %9.2f  |  %9.2f  |  %9.2f  |  %9.2f\n" % (reuss[0],reuss[1],reuss[2],reuss[3],hc[1],ht[1]))
    f.write("  hill   |  %9.2f  |  %9.2f  |  %9.2f  |  %9.2f  |  %9.2f  |  %9.2f\n" % (hill[0],hill[1],hill[2],hill[3],hc[2],ht[2]))
    isov = (3*hill[0]-2*hill[1])/(6*hill[0]+2*hill[1]) #isotropic Poisson's ratio
    f.write("-----------------------------------------------------------------------------\n")
    f.write("Isotropic Poisson's ratio:    %9.2f\n" % (isov))
    pr = hill[1]/hill[0] #Pugh ratio
    f.write("Pugh ratio:    %9.2f\n" % (pr))
    cp = c[0][1] - c[3][3] #Cauthy pressure
    f.write("Cauthy pressure(GPa):    %9.2f\n" % (cp))
    ac = (vogit[1]-reuss[1])/(vogit[1]+reuss[1]) #Chung-Buessem anisotropy index
    f.write("Chung-Buessem anisotropy index:    %9.2f\n" % (ac))
    au = 5*vogit[1]/reuss[1]+vogit[0]/reuss[0]-6 #Universal elestic anisotropy index
    f.write("Universal elestic anisotropy index:    %9.2f\n" % (au))
    if ifstable:
        f.write("your system are mechanical stable!\n")
    else:
        f.write("your system seems not stable or just check by your self!\n")
    f.write("\nGoooooooooooooooooooooooooooooooooooooooooooooodbye!")
    f.close()

def d2output(c,ifstable):
    #this function output all the result to 2dresult.txt
    f = open("2dresult.txt","w+")
    ff = open("modulus.txt","w+")
    s = np.linalg.inv(c)
    Ex = (c[0,0]*c[1,1]-c[0,1]**2)/c[1,1]
    Ey = (c[0,0]*c[1,1]-c[0,1]**2)/c[1,1]
    Gxy = c[2,2]
    Vxy = c[1,0]/c[1,1]
    Vyx = c[0,1]/c[0,0]
    c = c.tolist()
    s = s.tolist()
    f.write("the final mechanical result calculated by ponychen\n")
    f.write("stiffness tensor C_ij (GPa*nm)\n")
    for i in c:
        f.write("%9.2f %9.2f %9.2f\n" % (i[0],i[1],i[2]))
        ff.write("%9.2f %9.2f %9.2f\n" % (i[0],i[1],i[2]))
    ff.close()
    f.write("compliance tensor S_ij (GPa*nm)^-1\n")
    for i in s:
        f.write("%9.6f %9.6f %9.6f\n" % (i[0],i[1],i[2]))
    f.write("in-plane planar Young's moduli (GPa*nm) along x and y \n")
    f.write("%9.2f    %9.2f\n" % (Ex,Ey))
    f.write("in-plane planar Poisson's ratio along xy and yx\n")
    f.write("%9.2f    %9.2f\n" % (Vxy,Vyx))
    f.write("in-plane planar Shear moduli (GPa*nm)\n")
    f.write("%9.2f\n" % (Gxy))
    if ifstable:
        f.write("Your system are mechanical stable!\n")
    else:
        f.write("Your system seems not stable or just check by yourself!\n")
    f.write("\nGoooooooooooooooooooooooooooooooooooooooooooooooooooooobye!")
    f.close()

def finalout3rd(modulus):
    #output the third order elastic constants 
    f = open("3rd.txt","w+")
    f.write("third order elastic constants calculated by ponycehn\n")
    f.write("c111  c112  c144  c155  c456  c123  unit GPa\n")
    f.write("%9.2f  %9.2f  %9.2f  %9.2f  %9.2f  %9.2f" % (modulus[0],modulus[1],\
            modulus[2],modulus[3],modulus[4],modulus[5]))
    f.close()

def finalout4rd(modulus):
    #output the fourth order elastic constants
    c = modulus
    f = open("4rd.txt","w+")
    f.write("fourth order elastic constants calculated by ponychen\n")
    f.write("c1111  c1112  c1122  c1144  c4444  c1155  c4455  c1266  c1255  c1456  c1123 unit GPa\n")
    f.write("%9.2f %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f" % (\
            c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[10]))
    f.close()

def eosout(CX,CY,X,Y,label):
    #output the curve date of EOS
    with open("oldeos.txt","w+") as f:
        for i in range(len(X)):
            f.write("%9.2f %9.2f \n" % (X[i],Y[i]))
    with open("neweos.txt","w+") as f:
        f.write(label+"\n")
        for i in range(len(CX)):
            f.write("%9.6f %9.6f \n" % (CX[i], CY[i]))

