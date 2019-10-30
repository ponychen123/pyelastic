#!/bin/bash
#this script read stiffness tensor from OUTCAR of VASP using strss vs strain
#method
#ponychen
#20191030

column=`grep -in "TOTAL ELASTIC" OUTCAR|awk 'BEGIN{FS=":"} {print $1+3}'`

awk -v col=$column '
        NR>=col && NR<=col+5 {c1[NR-col+1]=$2/10;c2[NR-col+1]=$3/10;c3[NR-col+1]=$4/10;\
			c4[NR-col+1]=$5/10;c5[NR-col+1]=$6/10;c6[NR-col+1]=$7/10;}
		END{s1[1]=c1[1];s1[2]=c1[2];s1[3]=c1[3];s1[4]=c1[5];s1[5]=c1[6];s1[6]=c1[4];
		s2[1]=c2[1];s2[2]=c2[2];s2[3]=c2[3];s2[4]=c2[5];s2[5]=c2[6];s2[6]=c2[4];
		s3[1]=c3[1];s3[2]=c3[2];s3[3]=c3[3];s3[4]=c3[5];s3[5]=c3[6];s3[6]=c3[4];
		s4[1]=c5[1];s4[2]=c5[2];s4[3]=c5[3];s4[4]=c5[5];s4[5]=c5[6];s4[6]=c5[4];
		s5[1]=c6[1];s5[2]=c6[2];s5[3]=c6[3];s5[4]=c6[5];s5[5]=c6[6];s5[6]=c6[4];
		s6[1]=c4[1];s6[2]=c4[2];s6[3]=c4[3];s6[4]=c4[5];s6[5]=c4[6];s6[6]=c4[4];
		printf(" %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f\n",s1[1],s1[2],s1[3],s1[4],s1[5],s1[6]);
		printf(" %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f\n",s2[1],s2[2],s2[3],s2[4],s2[5],s2[6]);
		printf(" %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f\n",s3[1],s3[2],s3[3],s3[4],s3[5],s3[6]);
		printf(" %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f\n",s4[1],s4[2],s4[3],s4[4],s4[5],s4[6]);
		printf(" %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f\n",s5[1],s5[2],s5[3],s5[4],s5[5],s5[6]);
		printf(" %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f\n",s6[1],s6[2],s6[3],s6[4],s6[5],s6[6]);
	}' OUTCAR > modulus.txt 

