#!/bin/bash
directory="/etc/group"	#file we want to look into
for arg in $@
do
	check=false	#controls whether the name has been found or not. In this line resets
	while IFS=: read -r f1 f2 f3	#divides the line into fields, which are delimited by ":"
	do
		if [ $arg = $f3 ]; then
			echo -e "$f1"	#if the name is found, then prints the requested information
			check=true	#set the variable to true because the name has been found
			break	#if the name is found, the program stops looking for it an passes to the next name
		fi
	done < "$directory"
	if [ $check = false ]; then
		echo -e "-ERROR- $arg: no such GID"	#if the name wasn't founf, this is printed
	fi
done