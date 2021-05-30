#!/bin/bash
var1=""
var2=""
heu1="pickD"
heu2="busD"
heu3="lowB"

while getopts ":f:u:h" opt; do
  case ${opt} in
    f )
			if [ -f $OPTARG ]
			then
				var1=$OPTARG
				echo "$OPTARG will be the input file"
			else
				echo "$OPTARG is not a file"
				exit 1
			fi
      ;;
		u )
			if [ "$OPTARG" == "$heu1" ]
			then
				echo "Pick Distance heuristic selected..."
				var2=$OPTARG
			elif [ "$OPTARG" == "$heu2" ]
			then
				echo "Bus Deliver heuristic selected..."
				var2=$OPTARG
			elif [ "$OPTARG" == "$heu3" ]
			then
				echo "Lower Boundaries heuristic selected..."
				var2=$OPTARG
			else
				echo "Heuristic does not exist"
				exit 1
			fi
			;;
		h )
      echo "Usage of the script:         ./BusRouting -f filePath -u heuristicName"
			echo ""
			echo "Only supports execution when route.py and BusRouting are in the same directory and this one is the working directory"
			echo "Providing a file path or a file name is mandatory"
			echo "There are some test cases inside the directory ejemplos/"
			echo ""
			echo "Heuristics that can be chosen are the following:"
			echo "  -u pickD"
			echo "  -u busD"
			echo "  -u lowB"
			echo "If no heuristic has to be used:"
			echo "  -u no"
			echo "Read .pdf in p2-383387-383533/ to find out more about the heuristic"
			exit 1
      ;;
    \? )
      echo "Invalid option: $OPTARG" 1>&2
			echo "Use ./BusRouting -h to display help"
			exit 1
      ;;
    : )
      echo "Invalid option: $OPTARG requires an argument" 1>&2
			echo "Use ./BusRouting -h to display help"
			exit 1
      ;;
  esac
done

if [ "$var1" == "" ]
then
	echo "No input file was given"
	echo "Use ./BusRouting -h to display help"
	exit 1
fi
if [ -z $var2 ]
then
	echo "No heuristic was selected"
fi
echo ""
echo "Running search..."
python3 route.py $var1 $var2
