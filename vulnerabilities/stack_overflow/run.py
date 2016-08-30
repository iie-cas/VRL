#! /usr/bin/python
#coding:utf-8
import sys, os
sys.path.append("../..")
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
                'port' : '34567'}
        self.exploit = ['exploits/code_injection', 'exploits/borrow_code_chunks', 'exploits/rop', 'exploits/jop']

    def run(self):
        aslr_off()
        '''Run your vulnerability here, if this script could success, the VRL can run it.
        When the vulnerability run, follow the options.'''
        if eval(self.options['allow_stack_exec']):
            p = os.popen(new_terminal('./code_injection '+self.options['port']),'r')
        else:
            p = os.popen(new_terminal('./code_reuse '+self.options['port']),'r')

'''Bellowing is default, simply ignore it.'''
if __name__ == "__main__":
    if '__init__.py' not in os.listdir(os.curdir):
        os.mknod('__init__.py')
    vul = Vulnerability()
    print 'Vulnerability: ',vul.name,' \n'
    print 'Checking:\n'
    if vul.check():
        print 'Running:\n'
        vul.run()


