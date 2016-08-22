//gcc -fno-stack-protector -g -o ggtest ggtest.c -ldl
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <dlfcn.h>
#include<sys/socket.h>
#include<string.h>
#include<sys/types.h>
#include<arpa/inet.h>

#define MAXSIZE 1024

long long int systemaddr()
{
  char buf[128];
  long long int ans;
  void* handle = dlopen("libc.so.6", RTLD_LAZY);
  ans = (long long int)dlsym(handle, "system");
  return ans;
  //sprintf(buff,"%016LX\n\0",dlsym(handle,"system"));
  //m=send(connfd, buff, MAXSIZE, 0);
}

long long int testVul(char *buff)
{
	char str[10];
	strcpy(str, buff);
	if (buff[0] == 'b'){
	__asm__("movq %rbp, %rax");
	__asm__("leave");
	__asm__("ret");}
	else {
	    if (buff [0] == 's'){
	        long long int ans;
	        ans=systemaddr();
	        return ans;}
	    else {return 0;}
	}
	//return;
}
/*
void vulnerable_function(int connfd) {
  char buf[128];
  int n;
  if((n=recv(connfd, buf, MAXSIZE, 0))<=0){
      printf("Error recive\n");
      exit(1);
  }
}*/

int main(int argc,char *argv[])
{
	int listenfd, connfd;
	struct sockaddr_in servaddr;
	long long int add;
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
        int n,m;
		while((n=recv(connfd, buff, MAXSIZE, 0))>0)
		{
			buff[n] = '\0';
			add = testVul(buff);
			sprintf(buff, "%016LX\n", add);
			m=send(connfd, buff, MAXSIZE, 0);
		}

		close(connfd);
	}
	close(listenfd);
	return 0;
}
