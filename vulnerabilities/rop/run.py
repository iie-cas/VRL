#! /usr/bin/python
#coding:utf-8
import sys
sys.path.append("../..")
from modules import vulnerability
from modules.tools import *

import os
class Vulnerability(vulnerability.VRL_Vulnerability):
    def __init__(self):
        '''Add information of your vulnerability here'''
        self.name = 'rop'
        self.info = 'A simple server with rop vulnerability.'
        self.options={'dPort' : '34568'}
        self.exploit = 'rop'

    def run(self):
        '''Run your vulnerability here, if this script could success, the VRL can run it.
        When the vulnerability run, follow the options.'''
        p = os.popen(new_terminal('./ggtest '+self.options['dPort']),'r')
        #p = os.popen('gnome-terminal -e \'./ggtest '+ self.options['dPort']+"'",'r')
        print p.read()

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


