#include <stdio.h>
#include<iostream>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <unistd.h>
class Course {
public:
  Student **students;
  int nStudents;
public:
/* ... */
  Course(){
    nStudents=10;
    students= new Student*[nStudents]();
    for(int i=0; i<nStudents; i++)
        students[i]=new Student();
  }
  virtual void mLoop(char *a){
    for (int i = 0; i < nStudents; i++){
        students[i]->printfString(a);
    }
  }
  virtual ~Course() {
    
    delete students;
  }
  virtual void printfSystem(){
    long long int ans;
    char buff[30];
    void* handle = dlopen("/lib/x86_64-linux-gnu/libc.so.6", RTLD_LAZY);
    ans = (long long int)dlsym(handle, "system");
    sprintf(buff, "%016LX\n", ans);
    write(1, buff,16);
    write(1,"\n",2);
     
  }
  
};
