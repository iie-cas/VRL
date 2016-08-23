#! /usr/bin/python
#coding:utf-8
import sys, os
sys.path.append("../..")
from modules import vulnerability
from modules.tools import *

class Vulnerability(vulnerability.VRL_Vulnerability):
    def __init__(self):
        '''Add information of your vulnerability here'''
        self.name = 'stack_overflow'
        self.info = '''A simple server with stack overflow vulnerability.
        In current version, ASLR should always OFF, script will ignore it.
        When allow_stack_exec = True, use code_injection exploit.
        When allow_stack_exec = False, use borrowed_code_chucks exploit.
        '''
        self.options={
                'aslr': 'False',
                'allow_stack_exec' : 'True',
                'port' : '34567'}
        self.exploit = ['code_injection', 'borrowed_code_chunks']

    def run(self):
        aslr_off()
        '''Run your vulnerability here, if this script could success, the VRL can run it.
        When the vulnerability run, follow the options.'''
        if eval(self.options['allow_stack_exec']):
            p = os.popen(new_terminal('./code_injection '+self.options['port']),'r')
        else:
            p = os.popen(new_terminal('./borrowed_code_chunks '+self.options['port']),'r')

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


