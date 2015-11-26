#coding:UTF-8
import exploits
from exploits import *
import payloads
from payloads import *
import sys

options={'dIP':"127.0.0.1", 'dPort':"12345", 'exploit':"exploit4", 'payload':"payload1"}

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
    print "\ttest: 设置完参数后进行测试"
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

commands={'help':help, 'show':show, 'set':setup, 'reload':load, 'test':attack} #所有命令

while True:
    command = raw_input('test >> ').split()
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

        
