#! /usr/bin/python
#coding:utf-8
import sys, os, json, subprocess

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
    subprocess.PIPE
    p = subprocess.Popen("cat /proc/sys/kernel/randomize_va_space",stdout=subprocess.PIPE,shell= True)
    ans = p.stdout.read()
    return int(ans[0])

def aslr_on():
    if aslr_status() == 2:
        print 'ASLR is already ON\n'
        return
    print 'ASLR>>ON, may need password.\n'
    p = subprocess.Popen(r"sudo sysctl -w kernel.randomize_va_space=2",\
                                           stdin=subprocess.PIPE,shell= True)
    p.wait()

def aslr_off():
    if aslr_status() == 0:
        print 'ASLR is already OFF\n'
        return
    print 'ASLR>>OFF, may need password.\n'
    p = subprocess.Popen(r"sudo sysctl -w kernel.randomize_va_space=0", \
                                           stdin=subprocess.PIPE,shell= True)
    p.wait()

def aslr_conservative():
    if aslr_status() == 1:
        print 'ASLR is already Conservative\n'
        return
    print 'ASLR>>Conservative, may need password.\n'
    p = subprocess.Popen(r"sudo sysctl -w kernel.randomize_va_space=1", \
                                           stdin=subprocess.PIPE,shell= True)
    p.wait()


def print_line(str):
    try:
        import commands
        _output = commands.getoutput('resize')
        columns = int(_output.split(';')[0].split('=')[-1])
    except:
        print '[Warring]: It seems failed when import "commands".'
        columns = 80
    _length = columns
    _padding = '='
    _str = str.center(_length,_padding)
    print _str
