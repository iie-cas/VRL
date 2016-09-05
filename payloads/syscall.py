#! /usr/bin/python
# coding:utf-8
from pwnlib import asm

class Payload(object):
    def __init__(self):
        self.info = \
            '''abstract : 这段shellcode的作用是执行一个系统调用,默认为exit(0)
            architecture : x64
            length : undefined
            NULL byte: no.'''

    @property
    def data(self):
        code = ''
        #============config===============
        args = [0]    #not more than 6 arguments
        regs = ['rdi','rsi','rdx','rcx','r8','r9']
        rax = 60
        #=======update config=============
        c = raw_input('Do you want change default configurations?(y/n)(n)')
        if c and c[0] == 'y' :
            ar = raw_input("Enter a list of args(ex:[1,2,3]):\n")
            args = eval(ar)
            ra = raw_input("Enter syscall number:\n")
            rax = eval(ra)
        #============config===============
        args = [0]    #not more than 6 arguments
        regs = ['rdi','rsi','rdx','rcx','r8','r9']
        rax = 60
        #============assemble=============
        a_r = zip(args,regs[0:len(args)])
        for (a,r) in a_r:
            code += 'mov '+ r + ', ' + str(a) + '\n'
        code += 'mov rax, ' + str(rax) + '\n'
        code += 'syscall\n'
        return asm.asm(code, arch='amd64', os = 'linux')


if __name__ == '__main__':
    a=Payload()
    print a.data