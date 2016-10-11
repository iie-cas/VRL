#! /usr/bin/python
#coding:utf-8
import sys, os
sys.path.append(os.path.abspath("../.."))
from modules import vulnerability
from modules.script_tools import *

class Vulnerability(vulnerability.VRL_Vulnerability):
    def __init__(self):
        '''Add information of your vulnerability here'''
        self.name = 'stack_overflow'
        self.info = '''Vulnerability Name : stack_overflow
Vulnerability abstract : A simple server with stack overflow vulnerability
Author : guoyingjie'''

        self.options={
                'aslr': 'off',
                'allow_stack_exec' : 'True',
                'static' : 'False',
                'architecture' : 'i386',#'amd64',
                'port' : '34567'}
        self.exploit = ['code_injection', 'borrow_code_chunks', 'rop', 'jop', 'rop_shellcode']

    def run(self):
        aslr_off()
        '''Run your vulnerability here, if this script could success, the VRL can run it.
        When the vulnerability run, follow the options.'''
        if self.options['architecture'] == 'amd64':
            if self.options['static'] == 'False':
                if eval(self.options['allow_stack_exec']):
                    p = os.popen(new_terminal('./code_injection '+self.options['port']),'r')
                else:
                    p = os.popen(new_terminal('./code_reuse '+self.options['port']),'r')
            else:
                if eval(self.options['allow_stack_exec']):
                    p = os.popen(new_terminal('./ggteststatic '+self.options['port']),'r')
                else:
                    p = os.popen(new_terminal('./ggteststatic_stacknoexe '+self.options['port']),'r')
        elif self.options['architecture'] == 'i386':
            if self.options['static'] == 'False':
                p = os.popen(new_terminal('./code_reuse32 '+self.options['port']),'r')
            else:
                print 'Not supported: i386 & static.'
        else:
            print 'Unrecognized architecture, stop.'
            return
'''Bellowing is default, simply ignore it.'''
if __name__ == "__main__":
    if '__init__.py' not in os.listdir(os.curdir):
        os.mknod('__init__.py')
    vul = Vulnerability()
    print 'Vulnerability: ',vul.name,' \n'
    print 'Checking:\n'
    if vul.frame_check():
        print 'Running:\n'
        vul.run()


