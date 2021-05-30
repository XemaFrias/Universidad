#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <dirent.h>
#include <unistd.h>

#define MAX_PATH 1024
int main(int argc, char *argv[]){

	int fd;	/*For opening files*/
	int n;	/*Obtaining the size of the file*/
	DIR *dirp;
	struct dirent *extra; /*we need this for the readdir*/
	char *names;/*we will use this for printing the names of the files*/	
	char buf[MAX_PATH];	/*The buffer*/

	if(argv[1] != NULL){
		printf("Please, don't enter any paramenter\n");
		return (-1);
	}

	if(getcwd(buf, MAX_PATH)==NULL){	/*Gets the directory we are in*/
		perror("Obtaining path error");	/*If there is an error when obtaining the directory, it's printed on the console*/
		return(-1);
	}
	if((dirp=opendir(buf))<0){ /*Opens the directory*/
		perror("Error while opening");	/*If there is an error when opening, it's printed on the console*/
		return(-1);
	}

	while ((extra=readdir(dirp))!=NULL){ /*Reads each element in the directory */
		if(extra->d_type == DT_REG){/*Checks if tis a regular file*/
			names=extra->d_type;/*Saves the name of the read file for using it later*/
			if ((fd=open(names,O_RDONLY,0666))<0) { /*Opens the file with the name we saved before*/
	    		perror("Error opening file");	/*Prints an error if the file couldn't be open*/
    			return(-1);
  			}
  			if((n=lseek(fd,0,SEEK_END)) < 0) {	/*Moves the offset to the end of the file and returns that number*/	
     			perror("Seek error");	/*If there is an error when seeking, it's printed on the console*/
		    	return(-1);
  			}
  			if (close(fd)<0){    /*Closes the opened file*/
   				perror("Close file error");	/*If there is an error when closing, it's printed on the console*/
    			return(-1);
  			}
  			printf("%s\t%d\n", names, n);	/*Prints the information in the requested format*/
		}
	}

	if (closedir(dirp)<0){	/*Closes the opened directory*/
		perror("Close dir error");	/*If there is an error when closing, it's printed on the console*/
		return(-1);
	}
	return(0);
}
