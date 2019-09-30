![image](https://github.com/ponychen123/software/blob/master/pyelastic/images/156835383594723.png)

# pyelasitc is python based computer program for calculating the stiffness tensor and related mechanical and thermodynamical properties 

## author:ponychen

## email:18709821294@outlook.com

## key features:
+ generating series of input files for the calculation of second-order stiffness tensor （energy vs strain method)，as far supporting VASP, QE and Akai ab-inito programs
+ applying the Vogit, Reuss and Hill averaging procedure in order to obtain an evaluation of the bulk, shear, Young's moduli as well as
the Possion ratio of poly-crystalline samples, and so on
+ plot 2D and 3D anisotropic representation of elastic properties in single crystal
+ determining the sound velocities, Debye temperature, Gruneison parameter and lattice thermal conductivity using elastic properties
+ roughly calculating the pressure-temperature dependent thermodynamic properties of quasiharmonic approximation (Debye-Slater model)
+ calculating third and fourth oder elastic constants, as far only support cubic system

## acknowledgement
+ inspired by [VASPKIT](http://vaspkit.com/)
+ inspired by [ELAM](https://www.sciencedirect.com/science/article/pii/S0010465510003401)
+ inspired by [gibbs2](https://www.sciencedirect.com/science/article/pii/S0010465511001652)
+ inspired by [paper](https://journals_aps.gg363.site/prb/abstract/10.1103/PhysRevB.95.155206) of Tiantian Jia
+ greate thanks to the guidance from 李二狗(狗哥) and Vei Wang

## required environment
[python3](https://www.python.org/) [numpy](http://www.numpy.org/) [scipy](https://www.scipy.org/scipylib/index.html) [mayavi](http://docs.enthought.com/mayavi/mayavi/) [PyQt](https://sourceforge.net/projects/pyqt/files/PyQt5/) [matplotlib](https://matplotlib.org/)

## update history
2019/09/30: ponychen add support for TOEC and FOEC calculation for cubic system

2019/09/21：ponychen add support for elk format

2019/09/13: ponychen finished the first version (v0.1) of pyelastic

## instruction
### install
no need to complile this program ( python based ), but you should give execute permission to all the executable files in src foder. Meanwhile, give execyte permission to pyelastic.sh in the main folder
### code structure
all the necessacery modules and programs are under src folder, the main program pyelastic.sh in the main folder is written in bash shell. orig folder containing the undistorted structure file and relative input files，input.elastic in the main folder storing the parameters
### uasge
+ firstly specify the second and fourth columns of input.elastic. in column 2, choose your dimension of system (2D or 3D, you should alian your Z aixs to the direction of vacuum layer if you choose 2D). in column 4, choose calculation type (vrh, read, plot, debye, 3rd or 4rd). vrh means calculating mechanical properties by energy vs strain method, read means calculating mechanical properties by reading stiffness tensor from modulus.txt, plot means plot anisotropic single crystal properties by reading stiffness tensor from modulus.txt.  debye means calculating Debye temperature related thermo properties. 3rd means TOEC caluculation and 4rd means FOEC calculation. after confirm columns 2 and 4， you just need go to relative block and change default parameters as you like
+ case 3D and vrh: trig6 bravi type containing 32, 3m, -32/m. trig8 bravi type containing 3, -3. tetra6 bravi_type containing 422, 4mm, -42m, 4/mmm. tera7 bravi type containing 4, -4, 4/m. iso means isotrobic. this function is a two step process. Firstly you should set mode to 1, and this code will generating series of typeXXX folders containing distorted structures. you should do scf or relaxation (but keep cell fixed) in all sub folders ( you can copy all the folders to your clusters）. After this, set mode to 2 and code will read from all the typeXXX folders and output finalresult.txt and modulus.txt (containing stiffness tensor for other use)
+ debye calculation type only support 3D system
+ if your input type is vasp, orig folder need containing POSCAR (undistorted), POTCAR, KPOINTS and INCAR. if your input type is kkr, orig folder need containing in.inp (you should not change this name). if your input type is qe, orig folder need containing in.pw, you should specify your absolute path of pseudopotential file. if your input type is elk, orig folder need containing elk.in
+ for case read and plot, code need modulus.txt, for 3D system, this is a 6x6 matrix. for 2D system, this is a 3x3 matrix. wanning: you should use vogit indices
+ for 3rd and 4rd calculation, a large strain is needed to iclude the anhormonic 
