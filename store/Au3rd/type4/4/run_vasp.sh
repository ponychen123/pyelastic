#!/bin/bash
#SBATCH -p paratera 
#SBATCH -N 1
#SBATCH -n 24
source /PARA/app/scripts/cn-module.sh
module load intel-compilers/2018
module load MPI/Intel/MPICH/3.2-icc2018-dyn
VASP_PATH=/PARA/pp513/Application/vasp
export PATH=${VASP_PATH}:$PATH
export LD_LIBRARY_PATH=/opt/intel/composer_xe_2013_sp1.2.144/mlk/lib/intel64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/PARA/pp513/library/:$LD_LIBRARY_PATH

yhrun  vasp_std
