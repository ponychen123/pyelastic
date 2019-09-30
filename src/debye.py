#!/usr/bin/python3
#this module calculate the Debye temperature related properties
#author:ponychen

import numpy as np
from scipy import integrate

#get parameters from input.elastic
f = open("input.elastic","r")
inputfile = f.readlines()
strain = float(inputfile[30].split()[0])
B0,G0 = list(map(float,inputfile[31].split()[:2]))
B1,G1 = list(map(float,inputfile[32].split()[:2]))
ro = float(inputfile[33].split()[0])
m = float(inputfile[34].split()[0])
n = int(inputfile[35].split()[0])
volume = float(inputfile[36].split()[0])
mass = float(inputfile[37].split()[0])
temp = float(inputfile[38].split()[0])
f.close()

#two constant
hp = 6.62607015*10**(-34)  #Plank constant, J*s
kb = 1.380649*10**(-23)   #Boltzmann constant, J/K

#get the longitude(vl) and shear(vs) waves and averaged velocity(va)
#unit m/s
vl = 10000*np.sqrt(10)*np.sqrt((B0+4/3*G0)/(1000*ro))
vs = 10000*np.sqrt(10)*np.sqrt(G0/(1000*ro))
va = (1/3*(1/vl**3+2/vs**3))**(-1/3)

#get the Debye temperature 
deb = hp/kb*(3*m/(4*np.pi))**(1/3)*va*10**10

#roughly separate the acoustic braches from total vibration,get the acoustic 
#Debye temperature(deba)
deba = deb*n**(-1/3)

#Gruneisen parameter(rv) get from sound velocity
tmp = (1-2*(vs/vl)**2)/(2-2*(vs/vl)**2)
rv = 1.5*(1+tmp)/(2-3*tmp)

#Gruneisen parameter(re) get ny long-wave limit
B_V = (B1-B0)/(-strain*volume)
G_V = (G1-G0)/(-strain*volume)
rel = -0.5*volume/(B0+4/3*G0)*(B_V+4/3*G_V)-1/6 #longitude acoustic Gruneisen parameter
res = -0.5*volume/G0*G_V-1/6 #shear acoustic Gruneisen parameter
re = np.sqrt((rel**2+2*res**2)/3) 

#get the lattice thermal conductivity(kl), unit W/mK
kl = 2.43*10**-8/(1-0.514/re+0.228/re**2)*mass*(volume/n)**(1/3)*\
        n**(1/3)*deba**3/re**2/temp*100

#debye integral
def D(y):
    return y**3*np.exp(-y)/(1-np.exp(-y))

#calculating the thermodynamical properties by quasiharmonic formulas
F = []  #Hermholtz free energy , kJ/mol
S = []  #entropy, J/(mol*K)
U = []  #internal energy, kJ/mol
Cv = [] #specific heat capacity, J/(kg*K)

for T in range(1,2000,4):
    F.append((9/8*deb+3*T*np.log(1-np.exp(-deb/T))-T*3/(deb/T)**3*integrate.quad(D,0,deb/T)[0])*8.314463\
            /1000)
    S.append((-3*np.log(1-np.exp(-deb/T))+4*3/(deb/T)**3*integrate.quad(D,0,deb/T)[0]\
            )*8.314463)
    U.append((9/8*deb+3*T*3/(deb/T)**3*integrate.quad(D,0,deb/T)[0])*8.314463/1000)
    Cv.append((12*3/(deb/T)**3*integrate.quad(D,0,deb/T)[0]-9*deb/T/(\
            np.exp(deb/T)-1))*8.314463/mass*1000)

#store all the result to files
f = open("debye.txt","w+")
f.write("this file containing the debye temperture relatied parameters\n")
f.write("sound velocities(m/s)\n")
f.write("  longitude  |     shear    |   averaged    }\n")
f.write("  %9.3f   |   %9.3f   |   %9.3f   |\n" % (vs,vl,va))
f.write("Debye temperature(K): %9.2f\n" % (deb))
f.write("Debye temperature(K) only for acoustic branches: %9.2f\n" % (deba))
f.write("Gruneisen parameter using sound velocites: %9.2f\n" % (rv))
f.write("Gruneisen parameter using bulk and shear modulus (recommend)\n")
f.write("  longitude  |   shear   |  averaged\n")
f.write("   %9.2f   |   %9.2f   |   %9.2f   \n" % (rel,res,re))
f.write("lattice thermal conductivity(W/(m*K) at %9.2fK :  %9.2f\n" % (temp, kl))
f.write("gooooooooooooooooooooooooooooooooooooooooooodbye!")
f.close()

f = open("thermo.txt","w+")
f.write("this file containing the thermodynamical properties\n")
f.write("temperature(K)|Hermholtz free energy(KJ/mol)|entropy(J/(mol*K))|internal energy(kJ/mol)|specific heat capacity(J/(kg*K))\n")
for i in range(len(F)):
    f.write("  %9.2f  %9.2f  %9.2f  %9.2f  %9.2f\n" % (1+4*i,F[i],S[i],U[i],Cv[i]))

f.close()
