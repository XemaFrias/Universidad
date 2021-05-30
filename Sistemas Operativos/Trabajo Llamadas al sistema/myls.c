#include <stdio.h>              /* Cabecera llamada al sistema printf  */
#include <unistd.h>             /* Cabecera llamada al sistema gtcwd  */
#include <sys/types.h>          /* Cabeceras llamadas al sistema opendir, readdir y closedir  */
#include <dirent.h>
#include <string.h>

#define MAX_PATH 1024
int main(int argc, char *argv[]){

	DIR *dirp;
	struct dirent *extra; /*we need this for the readdir*/
	char *names;/*we will use this for printing the names of the files*/	
	int ending; /*for controlling the sucessful closing*/
	char buf[MAX_PATH];

	if(argv[1]==NULL){
		if(getcwd(buf, MAX_PATH)!=NULL){ /*If we haven't written anything after myls in the terminal, this will look for the path of our actual directory and store it in a buffer*/
			argv[1]=buf;	/*we will assing this path to argv[1] to eliminate extra steps afterwards, allowing this for using always sa,e implementation*/
		}
	}

	if((dirp=opendir(argv[1]))==NULL){ /*if we try to open the path and we can't, we will print an error*/
		perror("Error while opening");
		return(-1);
	}

	while ((extra=readdir(dirp))!=NULL){ /*this will read all the files in the directory by order until dont finding more*/
		names=extra->d_name;/*readdir is based on an structure. This line stores in a string variable the name of the file in the structure*/
		printf("%s\n",names);	/*Prints what is inside the directry*/
	}

	if ((ending=closedir(dirp))<0){/*assure correct ending of our open directory*/
		perror("Fail Closure");
		return(-1);
	}
	return(0);
}	




