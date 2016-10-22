
#include <stdio.h>
#include<iostream>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <unistd.h>
using namespace std;
class GuiButton {
public:
  void(*callbackClick)();
public:
  
  virtual void printfString(char a[]){
    printf("%s\n",a);
  }

  
  void registerCbClick(void(*cb)()) {
    callbackClick = cb;
  }
  virtual void clicked(int posX) {
    callbackClick();
  }
};
class Exam {
public:
  int scoreA, scoreB, scoreC;
  char *topic;
  int score;
  char a[10];
public:
/* ... */
  virtual void readString(){
    read(STDIN_FILENO, a, 512);
  };
  virtual void printfString(char a[]){
    printf("%s\n",a);
  };
  virtual void sumScore(long int &allscore) {
    allscore = scoreA + scoreB + scoreC;
  }
 
  virtual int getWeightedScore() {
    return (scoreA*5+scoreB*3+scoreC*2)/3;
  }
};

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
  virtual void mLoop(char a[]){
    for (int i = 0; i < nStudents; i++){
        students[i]->printfString(a);
    }
  }
  virtual ~Course() {
    
    delete students;
  }
  virtual void printfSystem(){
    void* handle = dlopen("libc.so.6", RTLD_LAZY);
    printf("%p\n",dlsym(handle,"Close"));
    fflush(stdout);   
  }
  
};




int main(){
    GuiButton butt;
    Student student;
    Course course;
    Exam exam;
    exam.readString();
    student.readString();
    exam.printfString(student.a);

    return 1;
}














