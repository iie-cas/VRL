// http://drops.wooyun.org/binary/7958
// gcc -g -m32 -o heap heap.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char *a[2010];
int i=2000;
void Malloc(void);
void Free(void);
void Edit(void);
void Print(void);

int main(void)
{
	char c;
	setbuf(stdout,NULL);
	while (1)
	{
		printf("What is your choice?(m/f/e/p)\n");
		scanf("%c",&c);
		getchar();
		if(c == 'm')
		{
			Malloc();
		}
		else if(c == 'f')
		{
			Free();
		}
		else if(c == 'e')
		{
			Edit();
		}
		else if(c == 'p')
		{
			Print();
		}
		else
		{
			break;
		}
	}
	printf("end\n");
}

void Malloc(void)
{
	int q;
	printf("malloc a heap\n");

	printf("enter the size of chunk\n");		
	scanf("%d",&q);
	getchar();

	a[i] = (char *)malloc(q);
	printf("enter your code\n");
	gets(a[i]);
	i++;
	printf("OK!\n");
}

void Free(void)
{
	int j;
	//printf("now i free a heap\n");
	printf("which heap do you want to free?\n");
	
	scanf("%d",&j);
	getchar();

	free(a[j+2000]);
	printf("Ok!\n");
}

void Edit(void)
{
	int j;
	printf("which heap do you want to edit?\n");
	scanf("%d",&j);
	getchar();
	gets(a[j+2000]);
	printf("Ok!\n");
}
void Print(void)
{
	int j;
	printf("which heap do you want to show?\n");
	scanf("%d",&j);
	getchar();
	printf("%s\n",a[j+2000]);
	printf("end\n");
}
