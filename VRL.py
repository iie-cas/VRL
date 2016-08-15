#! /usr/bin/python
#coding:utf-8
import sys
import os
from modules import *
import vulnerabilities
import exploits
import cmd


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
                        print vul.options
                    if exp:
                        print "Exploit options:"
                        print exp.options
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
            exp.run()
        else:
            print 'Error: No exploit using.'

    def do_qrun(self,vul):
        '''Quick run a vulnerability and it's default exploit with default options
        format: qrun []'''
    def do_EOF(self,line):
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

'''
options={'dIP':"127.0.0.1", 'dPort':"11111", 'exploit':"exploit6", 'payload':""}

def show_exploits(args=[]):      #命令show参数对应的函数定义
    for item in exploits.__all__:
        print "\t",item,": ",eval(item).__doc__
def show_payloads(args=[]):
    for item in payloads.__all__:
        print "\t",item,": ",eval(item).__doc__
def show_options(args=[]):
    for key in sorted(options.keys()):
        print "\t",key,": ",options[key]


shows={'exploits':show_exploits, 'payloads':show_payloads, 'options':show_options} #命令show的参数


def help(args=[]):
    print "\thelp: 帮助信息"
    print "\tquit: 退出"
    print "\treload: 重新加载exploits和payloads模块"
    print "\tshow exploits|payloads|options: 显示相应的信息"
    print "\t     exploits: 显示所有的exploits模块"
    print "\t     payloads: 显示所有的payloads模块"
    print "\t     options: 显示test所需要设置的参数"
    print "\tset dIP|dPort|exploit|payload arg: 设置test所需要设置的参数"
    print "\t    dIP: 设置目标IP"
    print "\t    dPort: 设置目标端口"
    print "\t    exploit: 所选用的exploit模块"
    print "\t    payload: 所选用的payload模块"
    print "\tui: 设置完参数后进行测试"
def show(args=[]):
    if len(args)!=1 or args[0] not in shows:
        print "\tInvalid args!"
        return
    shows[args[0]]()
def setup(args=[]):
    if len(args)!=2 or args[0] not in options:
        print "\tInvalid args!"
        return
    options[args[0]]=args[1]
def load(args=[]):
    for e in exploits.__all__:
        reload(eval(e))
    for p in payloads.__all__:
        reload(eval(p))
def attack(args=[]):
    print "\tNow testing..."
    #eval("from exploits import "+options['exploit']+" as e")
    e = eval(options['exploit'])
    t = e.exploit(options)
    try:
        t.test()
    except BaseException, e:
        print "ERROR:", e
        print "Please reset your options."

commands={'help':help, 'show':show, 'set':setup, 'reload':load, 'ui':attack} #所有命令

while True:
    command = raw_input('ui >> ').split()
    if len(command) == 0:
        print "\tMissing command!"
        print "\tEnter 'help' for help."
        continue
    if command[0] in ['quit', 'q']:
        sys.exit()
    if command[0] not in commands:
        print "\tInvalid command!"
        print "\tEnter 'help' for help."
        continue
    commands[command[0]](command[1:])

        
'''