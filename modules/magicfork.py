#! /usr/bin/python
# coding:utf-8

__author__ = 'Readm'

import __builtin__
import subprocess
import sys
from os import fork


def magicfork(terminal='gnome'):
    _fork = fork()
    if _fork != 0:
        return _fork
    else:
        if terminal in ['gnome', 'gnome-terminal']:
            bash_exec = "gnome-terminal -e \"bash -c 'mkfifo tmp; tty>tmp; exec sleep 99999999'\";  cat tmp; rm tmp"
        elif terminal == 'xterm':
            bash_exec = "xterm -e 'tty >&3; exec sleep 99999999' 3>&1"
        else:
            raise NameError('Unrecognized terminal name.')

        _r_i = __builtin__.raw_input
        _i = __builtin__.input

        p = subprocess.Popen(bash_exec, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        tty_path = p.stdout.readline().strip()
        tty = open(tty_path, 'r+')
        sys.stdout = tty
        sys.stderr = tty
        sys.stdin = tty

        def raw_input(prompt):
            sys.stdout.write(prompt)
            return _r_i('')

        __builtin__.raw_input = raw_input

        def input(prompt):
            sys.stdout.write(prompt)
            return _i('')

        __builtin__.input = input

        return 0
