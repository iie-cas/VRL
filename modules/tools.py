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

    if 'share.json' not in os.listdir(path[0:-11]):
        with open(path, 'w'):
            pass

    if os.path.getsize(path) >0 :
        with open(path, 'r') as f:
            json_data = json.load(f)

    with open(path, 'w') as f:
        json_data[str(key)] = value
        print json_data
        json.dump(json_data, f, indent=4)

def clear_share():
    path = '../../.tmp/share.json'

    if 'share.json' not in os.listdir(path[0:-11]):
        with open(path, 'w'):
            pass

    with open(path, 'w'):
        pass

def get_share(key):
    path = '../../.tmp/share.json'
    json_data={}

    if 'share.json' not in os.listdir(path[0:-11]):
        with open(path, 'w'):
            pass

    if os.path.getsize(path) >0 :
        with open(path, 'r') as f:
            json_data = json.load(f)

    return json_data[str(key)]
