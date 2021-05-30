	#!/bin/bash
	my_num=$#				#Store the number of arguments passed into a variable
	if [ "$my_num" -ne 2 ];then		#If that variable is not equal to 2 we print the usage message
		echo "Usage: ./exercise2_b.sh FILE NUMBER"
	else
		tr -c [:alnum:] [\\n\*] < $1 | sort | uniq -c | sort -nr | head -$2	
	fi			