#include <stdio.h>
#include<iostream>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <unistd.h>
class Student {
public:
  char a[10];
public:
Student(){};
virtual void readString(){
    read(STDIN_FILENO, a, 512);
  };
virtual void printfString(char a[]){printf("%s\n",a);};
};
