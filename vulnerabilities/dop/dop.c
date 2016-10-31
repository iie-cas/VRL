 #include <stdio.h>
 #include <unistd.h>
#include <dlfcn.h>
 typedef struct _mystruct {
     void (*foo)();
 } mystruct;

 void m1(){
     printf("hello from m1\n");
     fflush(stdout);
 }
 void m2(){
     printf("hello from m2\n");
     fflush(stdout);
 }
 
 void set_string(char a[]){
      char b[2];
      b[0]=a[0];

 }

void systemaddr()
{
  void* handle = dlopen("/lib/x86_64-linux-gnu/libc.so.6", RTLD_LAZY);
  printf("%p\n",dlsym(handle,"system"));
  fflush(stdout);
}

 mystruct ms1;
 mystruct ms2;
 mystruct ms3;
 mystruct *pms1 = &ms1, *pms2 = &ms2, *pms3 = &ms3;



 int main(int argc, char * argv[]) {
     int old_value, new_value;
     char buf;
     int *p = &old_value, *q = &new_value;
     pms1->foo=m1;
     pms2->foo=m2;
     pms3->foo=systemaddr;
     int limit = 2;
     int choose=0;
     while(limit--) {
         choose=limit+1;
         read(STDIN_FILENO, &buf,512); // memory error
         if(choose==1)
             pms1->foo();
         else if(choose==2)
             pms2->foo();
         else
             set_string(&buf);
          // assignment gadgets
         *p = *q;

     }
      
     pms2->foo();
 }




















