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

def print_line(str, padding='='):
    '''Print str expanded to a whole line.'''
    try:
        import commands
        _output = commands.getoutput('resize')
        columns = int(_output.split(';')[0].split('=')[-1])
    except:
        columns = 80
    _length = columns
    _str = str.center(_length,padding)
    print _str

def find_executable_file(path):
    '''Return a list of executable file names in the path.'''
    import ElfHeader
    lst = []
    for _file in os.listdir(path):
        os.chdir(path)
        try:
            with open(_file,'rb') as f:
                fstr = f.read()
                header = ElfHeader.ElfHeader.parse(fstr)
                if header:
                    if header.e_type == 2:
                        lst.append(str(_file))
        except:
            pass
    return lst

def pidof(file_name):
    '''Same as bash, return a list of pid number.'''
    p = subprocess.Popen(r"pidof " + str(file_name), stdout=subprocess.PIPE, shell= True)
    lst = p.stdout.read().split()
    lst = [int(i) for i in lst]
    return lst

def gdb(file_name='',pid=0, path='', sudo=True):
    '''Open a gdb.'''
    _cmd = ''
    if sudo: _cmd += 'sudo '
    _cmd += 'gdb '
    if file_name: _cmd += file_name + ' ' + str(pid)
    if path:
        os.chdir(path)
        sys.path.append(path)
        os.system(new_terminal_exit(_cmd))
        sys.path.remove(path)
    else:
        os.system(new_terminal_exit(_cmd))

colorcodes =    {'bold':{True:'\x1b[1m',False:'\x1b[22m'},
                 'cyan':{True:'\x1b[36m',False:'\x1b[39m'},
                 'blue':{True:'\x1b[34m',False:'\x1b[39m'},
                 'red':{True:'\x1b[31m',False:'\x1b[39m'},
                 'magenta':{True:'\x1b[35m',False:'\x1b[39m'},
                 'green':{True:'\x1b[32m',False:'\x1b[39m'},
                 'yellow':{True:'\x1b[33m',False:'\x1b[39m'},
                 'white':{True:'\x1b[37m',False:'\x1b[39m'},
                 'black':{True:'\x1b[30m',False:'\x1b[39m'},
                 'underline':{True:'\x1b[4m',False:'\x1b[24m'}}
def colorize(val, color):
    '''Given a string (``val``), returns that string wrapped in UNIX-style
       special characters that turn on (and then off) text color and style.
       ``color`` should be one of the supported strings (or styles):
       red/blue/green/cyan/magenta, bold, underline'''
    if color:
        return colorcodes[color][True] + val + colorcodes[color][False]
    return val

