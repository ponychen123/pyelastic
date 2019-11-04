#!/usr/bin/python3
#this script gives the correct lattice axis that pyelasitc need
#ponychen
#2019/11/3

import numpy as np

def get_standard(old_axis,bravi_type):
    #get basic parameters of cell
    la,lb,lc = np.linalg.norm(old_axis,axis=1)
    a = old_axis[0,:]
    b = old_axis[1,:]
    c = old_axis[2,:]
    alpha = np.arccos(np.dot(b,c)/(lb*lc))
    beita = np.arccos(np.dot(a,c)/(la*lc))
    gamma = np.arccos(np.dot(a,b)/(la*lb))

    new_axis = np.zeros([3,3])

    if bravi_type == "cubic" or bravi_type == "tetra6" or \
            bravi_typr == "tetra7" or bravi_type == "ortho":
        new_axis[0,0] = la
        new_axis[1,1] = lb
        new_axis[2,2] = lc
    elif bravi_type == "hex" or bravi_type == "trig6":
        new_axis[0,0] = la
        new_axis[1,0] = -0.5*la
        new_axis[1,1] = 3**0.5/2*la
        new_axis[2,2] = lc
    elif bravi_type == "trig8":
        aa = la*np.sin(alpha/2)
        h = la*np.sqrt(1-4/3*np.sin(alpha/2)**2)
        new_axis[0,0] = aa
        new_axis[0,1] = new_axis[2,1] = -1/3**0.5*aa
        new_axis[:,2] = h
        new_axis[1,1] = 2/3**0.5*aa
        new_axis[2,0] = -aa
    elif bravi_type == "mono":
        #caution: c is the unique axis!!!!
        new_axis[0,0] = la
        new_axis[1,0] = lb*np.cos(gamma)
        new_axis[1,1] = lb*np.sin(gamma)
        new_axis[2,2] = lc
    elif bravi_type == "tric":
        cc = lc/np.sin(gamma)*(np.cos(alpha)-np.cos(beita)*np.cos(gamma))
        omiga = lc/np.sin(gamma)*np.sqrt(1+2*np.cos(alpha)*np.cos(beita)*\
                np.cos(gamma)-np.cos(alpha)**2-np.cos(beita)**2-\
                np.cos(gamma)**2)
        new_axis[0,0] = la
        new_axis[1,0] = lb*np.cos(gamma)
        new_axis[1,1] = lb*np.sin(gamma)
        new_axis[2,0] = lc*np.cos(beita)
        new_axis[2,1] = cc
        new_axis[2,2] = omiga

    return new_axis



