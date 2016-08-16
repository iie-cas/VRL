#! /usr/bin/python
#coding:utf-8
from modules import vulnerability

import os
class Vulnerability(vulnerability.VRL_Vulnerability):
    def __init__(self):
        '''Add information of your vulnerability here'''
        self.name = 'stack_overflow'
        self.info = 'information'
        self.options={'dPort' : '34566'}
        self.exploit = 'stack_overflow'

    def run(self):
        '''Run your vulnerability here, if this script could success, the VRL can run it.
        When the vulnerability run, follow the options.'''
        p = os.popen('gnome-terminal -e \'./ggtest '+ self.options['dPort']+"'",'r')
        print p.read()

'''Bellowing is default, simply ignore it.'''
if __name__ == "__main__":
    vul = Vulnerability()
    print 'Vulnerability: ',vul.name,' \n'
    print 'Checking:\n'
    if vul.check():
        print 'Running:\n'
        vul.run()


