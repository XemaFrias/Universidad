#!/bin/bash
for i in $(seq $1 $2);
do
	if [ $i = 1 ]; then	#As factor does not return any number when factoring 1, it has to be printed "manually"
		echo -e "1"
		continue
	else	#for any other number distinct to 1
	factors=$(factor $i | cut -d : -f 2 | cut -d " " -f 2) #saving al the factors of the corresponding number
		if [ "$i" -eq "$factors" ]	#if the number factorized is saves in the variable factors, then is a prime number 
		then
			echo -e "$i"	#printing a prime number
		fi
	fi
done