#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<stdbool.h>

typedef struct vul{
	int d1, d2;
	void(*fp)();
}vul;

void test(){
	printf("hello!\n");
}

void hack(){
	system("/bin/sh");
}

void useAfterFree(char *str){
	vul *p = (vul *)malloc(sizeof(vul));
	p->fp = test;
	free(p);
	char *p2 = (char*)malloc(12);
	strcpy(p2, str);
	p -> fp();
}

int main(){
	char s[100];
	gets(s);
	useAfterFree(s);
	return 0;
}
