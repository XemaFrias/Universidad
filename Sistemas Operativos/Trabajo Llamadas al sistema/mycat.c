#include <stdio.h>              /* Libraries to call functions open(), perror(), read(), write() and close()*/
#include <sys/types.h>          
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>             
#include <stdlib.h>

#define N 1024
int main(int argc, char *argv[]){

	int fd,n;
  char buf[N];
  
  if(argv[1] == NULL){
    return -1;
  }
  if ((fd=open(argv[1],O_RDONLY,0666))<0) { /*Using argv[1] to open the file introduced as an argument through the console*/
	  perror("Error opening file");	/*Prints an error if the file couldn't be open*/
   	return -1;
  }

  while((n=read(fd,buf,N))>0){	/*Reads the file, copyes N bytes into the buffer and assings to n the size in it*/
    if (write(STDOUT_FILENO,buf,n)< 0) {	/*Writes on the console the content of the buffer until the position n, because is the size of the file*/
      perror("write error"); /*Prints an error if the content of the buffer couldn't be written*/
      exit(1);
    }
  }
  if(close(fd) < 0){
    perror("Error closing file");
    exit(1);
  };	/*Closes the file*/
  return 0;
}
