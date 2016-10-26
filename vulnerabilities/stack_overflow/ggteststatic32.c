//gcc -fno-stack-protector -z execstack -g -o code_injection ggtest.c aslr off
//gcc -fno-stack-protector -g -o code_reuse ggtest.c -ldl aslr on
//gcc -fno-stack-protector -g -o code_reuse_jop ggtest.c -ldl  aslr off
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <dlfcn.h>
#include<sys/socket.h>
#include<string.h>
#include<sys/types.h>
#include<arpa/inet.h>

#define MAXSIZE 1024



/*vulnerability function*/
long int testVul(int connfd)
{
        char str[10];
        recv(connfd, str, MAXSIZE, 0);


        //code reuse jop, rop, dep
      if(str[0]=='p'){//generate gadget, non-execution
        __asm__("pop %ecx");
        __asm__("pop %eax");
	__asm__("pop %ebx");
	__asm__("add $0x08,%ebx");
        __asm__("jmp *(%ebx)");
        __asm__("pop %eax");
        __asm__("jmp %ecx");
      }
      if (str[0]=='c'){//non-execution
       system("/bin/sh");
      }
      if(str[0]=='b'){//the second receive,return rbp
         __asm__("mov %ebp, %eax");
	 __asm__("leave");
	 __asm__("ret");}
	
}


int main(int argc,char *argv[])
{
	int listenfd, connfd;
	struct sockaddr_in servaddr;
	long int add;
	char buff[MAXSIZE];
	listenfd = socket(AF_INET, SOCK_STREAM, 0);
	if(listenfd==-1)
	{
		printf("Error socket\n");
		exit(1);
	}
	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port=htons(atoi(argv[1]));  
	if(bind(listenfd, (struct sockaddr*)&servaddr, sizeof(servaddr))==-1)
	{
		printf("Error bind\n");
		exit(1);
	}
	if(listen(listenfd, 1)==-1)
	{
		printf("Error listen\n");
		exit(1);
	}
	unsigned int len;
	if(getsockname(listenfd, (struct sockaddr*)&servaddr, &len))
	{
		printf("Error getsockname\n");
		exit(1);
	}
	int listenPort = ntohs(servaddr.sin_port);
	while(1)
	{
		printf("waiting for connect...(port %d)\n", listenPort);
		connfd = accept(listenfd, (struct sockaddr*)NULL, 0);
		if(connfd==-1)
		{
			printf("Error accept\n");
			exit(1);
		}
		printf("wating for data...\n");
        int m;
		
		while(1){
                        add = testVul(connfd); //call vulnerability function, get useful value
			sprintf(buff, "%08lX\n", add);//convert to hexadecimal
			m=send(connfd, buff, 8, 0);//send to exploit program
                } 
		close(connfd);
	}
	close(listenfd);
	return 0;
}
