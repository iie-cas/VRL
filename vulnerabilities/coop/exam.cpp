#include <stdio.h>
#include<iostream>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <unistd.h>
class Exam {
public:
  int scoreA, scoreB, scoreC;
  char *topic;
  int score;
  char a[10];
public:
/* ... */
  virtual void readString(){
    read(STDIN_FILENO, a, 3);
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
