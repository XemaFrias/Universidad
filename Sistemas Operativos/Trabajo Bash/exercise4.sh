# !/bin/bash
for inputfile in "$1"/* ; do    #Look for all the files inside the directory introduced by the user
	if [[ $inputfile == *".JPG" ]] || [[ $inputfile == *".jpg" ]] || [[ $inputfile == *".JPEG" ]] || [[ $inputfile == *".jpeg" ]];then
		size_image="$(du "$inputfile" |cut -f1)"				#Extract the size of the image
		echo "$size_image"
		if [ "$size_image" -gt 1024 ];	then				#If image_size bigger than 1Mb	
    	convert "$inputfile" -resize 720x "$inputfile"		#resize the width maintaining the height proportion and the name
    	echo "Images changed:"
    	echo "$inputfile"
		fi
	fi	
done	