
#include "guibutton.cpp"
#include "exam.cpp"
#include "student.cpp"
#include "course.cpp"



int main(){
    GuiButton butt;
    Student student, *studentPtr;
    Course course;
    Exam exam, *examPtr;
    studentPtr=&student;
    examPtr=&exam;
    examPtr->readString();
    studentPtr->readString();
    examPtr->printfString(student.a);
    studentPtr->printfString(exam.a);
    return 0;
}














