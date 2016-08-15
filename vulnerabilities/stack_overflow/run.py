#! /usr/bin/python
#coding:utf-8
import os
from modules import vulnerability

class Vulnerability(vulnerability.VRL_Vulnerability):
    def __init__(self):
        '''Add information of your vulnerability here'''
        self.name = 'stack_overflow'
        self.info = 'information'
        self.options={'dIP' : '127.0.0.1',
                      'dPort' : '12345'}
        self.exploit = 'stack_overflow'

    def run(self):
        '''Run your vulnerability here, if this script could success, the VRL can run it.
        When the vulnerability run, follow the options.'''
        print 'run your vulnerability here'

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


