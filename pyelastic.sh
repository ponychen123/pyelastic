#!/bin/bash
#the main program of pyelastic, writen with bash shell
#author:ponychen
#email:18709821294@outlook.com

sys_type=`sed -n '2p' input.elastic|awk '{print $1}'`
cal_type=`sed -n '4p' input.elastic|awk '{print $1}'`

if [ "$sys_type" == "3D" ] && [ "$cal_type" == "vrh" ];then
	python3 src/main.py
fi

if [ "$sys_type" == "3D" ] && [ "$cal_type" == "plot" ];then
	python3 src/plotaniso.py
fi

if [ "$sys_type" == "2D" ] && [ "$cal_type" == "vrh" ];then
    python3 src/2dmain.py
fi

if [ "$sys_type" == "2D" ] && [ "$cal_type" == "plot" ];then
	python3 src/2dplotaniso.py
fi

if [ "$sys_type" == "3D" ] && [ "$cal_type" == "read" ];then
	python3 src/3dmodulusread.py
fi

if [ "$sys_type" == "2D" ] && [ "$cal_type" == "read" ];then
	python3 src/2dmodulusread.py
fi

if [ "$sys_type" == "3D" ] && [ "$cal_type" == "debye" ];then
	python3 src/debye.py
fi

if [ "$sys_type" == "3D" ] && [ "$cal_type" == "3rd" ];then
	python3 src/3rd.py
fi

if [ "$sys_type" == "3D" ] && [ "$cal_type" == "4rd" ];then
	python3 src/4rd.py
fi

if [ "$sys_type" == "3D" ] && [ "$cal_type" == "eos" ];then
	python3 src/eos.py
fi
