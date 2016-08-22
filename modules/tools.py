#! /usr/bin/python
#coding:utf-8
import sys, os, json

'''Tools for VRL script'''

def new_terminal(command):
    '''Return a new command, execute old command in a new terminal, when old command stop, leave in the terminal.'''
    cmd_bash = command + '; exec bash'
    e_command = "'bash -c \""+cmd_bash+"\"'"
    return "gnome-terminal -e "+e_command

def new_terminal_exit(command):
    '''Return a new command, execute old command in a new terminal, when old command stop, exit the terminal.'''
    return "gnome-terminal -e '"+command+"'"

#Share data between vul and exp script.
#Only use it in run.py.
def share(key, value):

    path = '../../.tmp/share.json'
    json_data = {}

    _check_share_path()

    if os.path.getsize(path) >0 :
        with open(path, 'r') as f:
            json_data = json.load(f)

    with open(path, 'w') as f:
        json_data[str(key)] = value
        print json_data
        json.dump(json_data, f, indent=4)

def clear_share():
    path = '../../.tmp/share.json'

    _check_share_path()

    with open(path, 'w'):
        pass

def get_share(key):
    path = '../../.tmp/share.json'
    json_data={}

    _check_share_path()

    if os.path.getsize(path) >0 :
        with open(path, 'r') as f:
            json_data = json.load(f)

    return json_data[str(key)]

def _check_share_path():
    path = '../../.tmp/share.json'
    if not os.path.exists(path[0:-11]):
        os.mkdir(path[0:-11])
    if 'share.json' not in os.listdir(path[0:-11]):
        with open(path, 'w'):
            pass

def aslr_status():
    p = os.popen(r"cat /proc/sys/kernel/randomize_va_space")
    ans = p.read()
    return int(ans[0])

def aslr_on():
    if aslr_status() == 2:
        print 'ASLR is already ON\n'
        return
    print 'ASLR>>ON, need password.\n'
    os.popen(new_terminal_exit(r"sudo sysctl -w kernel.randomize_va_space=2"))

def aslr_off():
    if aslr_status() == 0:
        print 'ASLR is already OFF\n'
        return
    print 'ASLR>>OFF, need password.\n'
    os.popen(new_terminal_exit(r"sudo sysctl -w kernel.randomize_va_space=0"))

def aslr_conservative():
    if aslr_status() == 1:
        print 'ASLR is already Conservative\n'
        return
    print 'ASLR>>Conservative, need password.\n'
    os.popen(new_terminal_exit(r"sudo sysctl -w kernel.randomize_va_space=1"))
