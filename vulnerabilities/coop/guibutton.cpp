#include <stdio.h>
#include<iostream>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <unistd.h>
class GuiButton {
public:
  char *a;
  int (*callbackClick)(char *a);
public:
  
  virtual void printfString(char a[]){
    printf("%s\n",a);
  }

  
  void registerCbClick(int(*cb)(char *a)) {
    callbackClick = cb;
  }
  virtual void clicked(char *a1) {
    callbackClick(a);

  }
};
