#!/bin/bash
#this script used to trasfer the KKR format to POSCAR for the use of watching
#usage: kkr2pos.sh filename atom_numbers
#caution: only aux format are support
#author:ponychen
#email:18709821294@outlook.com
#20190829

#get the begoin and end lines of axis coodnation
cellbegin=`grep -in "aux" $1 | awk ' BEGIN{FS=":"} {print $1+1}'`
cellend=$(($cellbegin+2))

#get the axis coordition and tranfer them to uniform Cartesian with unit Angstrom
eval $(awk -v begin=$cellbegin -v end=$cellend '
    NR>=begin && NR<=end {x0[NR]=$1;y0[NR]=$2;z0[NR]=$3}
	NR==end+1 {alen=$1*0.5292}
END{for(i=begin;i<=end;i++){
printf("cell[%d]=\"  %9.6f\t%9.6f\t%9.6f\"\n",i,x0[i]*alen,y0[i]*alen,z0[i]*alen)}}' $1)

#get the atom coordinations 
grep -v "^$" $1 | tail -n $2 - | tr -d "a-zA-Z" | awk '{print $1,$2,$3}' > tmp

#export to POSCAR
echo "generate by kkr2pos.sh" > POSCAR
echo "1.000000" >> POSCAR
for ((i=$cellbegin;i<=$cellend;i=i+1))
do
	echo "    ${cell[$i]}" >> POSCAR
done
echo "Au" >> POSCAR
echo $2 >> POSCAR
echo "Direct" >> POSCAR
cat tmp >> POSCAR
rm tmp
