#! /usr/bin/python
#coding:utf-8
import sys
import os
import cmd


from modules import *
import vulnerabilities
import exploits


class ui(cmd.Cmd):
    prompt = '(VRL)'
    intro = 'Welcome to VRL'
    global exp,vul,exploit_list,vulnerability_list

    def do_reload(self,line):
        '''Reload all exploits,vulnerabilities,payloads,etc.
        When VRL started, loading is done.
        So you only need to use this when you add something new and do not want to restart VRL.'''
        global exploit_list
        global vulnerability_list
        exploit_list=[]
        vulnerability_list=[]
        for type in ['exploits','vulnerabilities']:
            subpath=os.path.join(os.curdir,type)
            for name in os.listdir(subpath):
                if os.path.isdir(os.path.join(subpath,name)):
                    if 'run.py' in os.listdir(os.path.join(subpath,name)):
                        if type=='exploits': exploit_list.append(str(name))
                        if type=='vulnerabilities': vulnerability_list.append(str(name))

    def do_show(self,type):
        '''Show all exploits|vulnerabilities|payload
        format: list exploit|vulnerabilities|payload (e|v|p for short.)'''
        if type:
            path={'e':exploit_list, 'v':vulnerability_list}#,'p':payload}
            if type[0] in path.keys():
                for i in path[type[0]]:
                    print i
            elif type[0] == 'o':     #for options
                if vul or exp:
                    if vul:
                        print "Vulnerability options:"
                        for (key,value) in vul.options.items():
                            print key,':',value
                    if exp:
                        print "Exploit options:"
                        for (key,value) in exp.options.items():
                            print key,':',value
                else:
                    print 'Error: No vulnerability or exploit using.'
            else:
                print "Error: Invade argument."
        else:
            print "Wrong format!"

    def do_usevul(self,name):
        '''Use a vulnerability
        format: usevul vulnerability_name'''
        global vul
        try:
            _temp=__import__('vulnerabilities.'+name+'.run',globals(),locals(),fromlist=['Vulnerability'])
            Vulnerability = _temp.Vulnerability
            vul=Vulnerability()
            print 'Vulnerability Loaded'
            if hasattr(vul,'exploit') and not exp:
                c = raw_input("This vulnerability has a default exploit, use the exploit?(y/n):(y)")
                if not c or c[0] != 'n':
                    self.do_useexp(vul.exploit)
        except Exception,e:
            print e

    def do_useexp(self,name):
        '''Use an exploit
        format: useexp exploit_name'''
        global exp
        try:
            _temp=__import__('exploits.'+name+'.run',globals(),locals(),fromlist=['Exploit'])
            Exploit= _temp.Exploit
            exp=Exploit()
            print 'Exploit Loaded'
            if hasattr(exp,'vulnerability') and not vul:
                c = raw_input("This exploit has a default vulnerability, use the exploit?(y/n):(y)")
                if not c or c[0] != 'n':
                    self.do_usevul(exp.vulnerability)
        except Exception,e:
            print e

    def do_runvul(self,line):
        '''Run the vulnerability using'''
        if vul:
            vul.run()
        else:
            print 'Error: No vulnerability using.'

    def do_runexp(self,line):
        '''Run the exploit using'''
        if exp:
            exp.stop()
        else:
            print 'Error: No exploit using.'

    def do_stopvul(self,line):
        '''Stop the vulnerability using'''
        if vul:
            if hasattr(vul,'stop'):
                vul.stop()
            else:
                print 'Error: This vulnerability cannot stop.'
        else:
            print 'Error: No vulnerability using.'

    def do_stopexp(self,line):
        '''Stop the exploit using'''
        if exp:
            if hasattr(exp,'stop'):
                exp.stop()
            else:
                print 'Error: This exploit cannot stop.'
        else:
            print 'Error: No exploit using.'

    def do_qrun(self,name):
        '''Quick run a vulnerability and it's default exploit with default options
        format: qrun []'''
        if not vul and not exp:
            if not name:
                print "No vulnerability or exploit using, enter a name to quick run."
                return
            self.do_usevul(name)
        self.do_runvul('')
        self.do_runexp('')

    def do_q(self,line):
        '''Quit VRL.'''
        self.do_EOF(line)

    def do_EOF(self,line):
        '''Quit VRL'''
        return True

#list of exp & vul
exploit_list=[]
vulnerability_list=[]
#exp & vul using
exp=[]
vul=[]

VRLui=ui()
VRLui.do_reload('')
VRLui.cmdloop()

