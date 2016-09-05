#! /usr/bin/python
# coding:utf-8

import sys
import os
import json

try:
    import cmd2 as cmd
except ImportError:
    import cmd

from modules.script_tools import *

def update_prompt(f):
    def fn(*args, **kw):
        sys.stdout.flush()
        global exp, vul, pay
        ans = f(*args, **kw)
        _pro = colorize('VRL ','magenta')
        if vul:
            _pro += colorize('V ','green')
        else :
            _pro += colorize('V ','black')
        if exp:
            _pro += colorize('E ','green')
        else :
            _pro += colorize('E ','black')
        if exp:
            if hasattr(exp, 'default_payload'):
                if vul:
                    _pro += colorize('P','green')
                else:
                    _pro += colorize('P','black')
            else :
                _pro += colorize('P','blue')
        else:
            _pro += colorize('P','black')
        VRLui.prompt = colorize(_pro+'>','bold')
        sys.stdout.flush()
        return ans
    return fn

class ui(cmd.Cmd):
    intro = 'Welcome to VRL'

    @update_prompt
    def do_reload(self, line):
        '''Reload all exploits,vulnerabilities,payloads,etc.
When VRL started, loading is done.
So you only need to use this when you add something new and do not want to restart VRL.'''
        global exploit_list, vulnerability_list, payload_list, misc_list
        exploit_list = []
        vulnerability_list = []
        payload_list = []
        for type in ['exploits', 'vulnerabilities']:
            subpath = os.path.join(os.curdir, type)
            for name in os.listdir(subpath):
                if os.path.isdir(os.path.join(subpath, name)):
                    if 'run.py' in os.listdir(os.path.join(subpath, name)):
                        if type == 'exploits': exploit_list.append(str(name))
                        if type == 'vulnerabilities': vulnerability_list.append(str(name))
        for type in ['payloads', 'misc']:
            for i in os.listdir(os.path.join(os.curdir, type)):
                [a, b] = os.path.splitext(str(i))
                if b in ['.py', '.json']:
                    if a != '__init__':
                        if type == 'misc':
                            misc_list.append(a)
                        else:
                            payload_list.append(a)

    def do_guide(self, line):
        '''Show a simple guide.'''
        print '''
        Simple guide:
        help command or ?[command] for help.
        show command for list vulnerabilities and exploits.
        use command for load vulnerabilities and exploits.
        run command for run vulnerabilities and exploits.
        For more commands, use help command to list all, or read the document.
        '''

    def do_show(self, type):
        """
Show all exploits|vulnerabilities|payload|options|tools
Format: show exploit|vulnerabilities|payload|options|tools
        show e|v|p|o|t for short."""
        if type:
            path = {'exploits': exploit_list, 'vulnerabilities': vulnerability_list, \
                    'payloads': payload_list, 'tools': misc_list}
            _cmd = path.keys()
            _cmd.append('options')
            for i in _cmd:
                if i.startswith(type): type = i
            if type in path.keys():
                print_line('')
                for i in path[type]:
                    print i
                print_line('')
            elif type == 'options':  # for options
                if vul or exp:
                    if vul:
                        print_line('Vulnerability options:')
                        for (key, value) in vul.options.items():
                            print key, ':', value
                    if exp:
                        print_line('Exploit options:')
                        for (key, value) in exp.options.items():
                            print key, ':', value
                    print_line('')
                else:
                    print 'No vulnerability or exploit using. So no options to show.'
            else:
                print "[Error]: Invalid argument."
        else:
            print "[Error]: Wrong Format!"
            self.do_help('show')

    def complete_show(self, text, line, begidx, endidx):
        args = ['options', 'payloads', 'exploits', 'vulnerabilities', 'tools']
        return [i for i in args if i.startswith(text)]

    @update_prompt
    def do_usevul(self, name):
        '''Use a vulnerability
Format: usevul vulnerability_name'''
        global vul, vul_path
        try:
            _temp = __import__('vulnerabilities.' + name + '.run', globals(), locals(), fromlist=['Vulnerability'])
            Vulnerability = _temp.Vulnerability
            vul = Vulnerability()
            print 'Vulnerability Loaded.'
            vul_path = os.path.join(sys.path[0], 'vulnerabilities', name)
            self.do_infovul('')
            if hasattr(vul, 'exploit') and vul.exploit:
                print_line('Supported Exploits:')
                if type(vul.exploit) == str:
                    print vul.exploit
                elif type(vul.exploit) == list:
                    for i in vul.exploit:
                        print i
                print_line('')
            if exp:
                print '>Exploit exist, auto_sync options(exp->vul).'
                for _key in vul.options.keys():
                    if _key in exp.options.keys():
                        vul.options[_key] = exp.options[_key]
        except Exception, e:
            print colorize('[Error]: ','red'), e

    def complete_usevul(self, text, line, begidx, endidx):
        return [i for i in vulnerability_list if i.startswith(text)]

    @update_prompt
    def do_useexp(self, name):
        '''Use an exploit
Format: useexp exploit_name'''
        global exp, exp_path, pay
        try:
            _temp = __import__('exploits.' + name + '.run', globals(), locals(), fromlist=['Exploit'])
            Exploit = _temp.Exploit
            exp = Exploit()
            print 'Exploit Loaded.'
            self.do_infoexp('')
            exp_path = os.path.join(sys.path[0], 'exploits', name)
            if hasattr(exp, 'vulnerability') and exp.vulnerability:
                print_line('Supported Vulnerabilities:')
                if type(exp.vulnerability) == str:
                    print exp.vulnerability
                elif type(exp.vulnerability) == list:
                    for i in exp.vulnerability:
                        print i
                print_line('')

            # auto options fixing
            if vul:
                print '>Vulnerability exist, auto_sync options(exp->vul).'
                for _key in vul.options.keys():
                    if _key in exp.options.keys():
                        vul.options[_key] = exp.options[_key]

            # load default payload
            if hasattr(exp, 'default_payload'):
                if (exp.default_payload):
                    exp.payload=''
                    print ">Exploit has a default payload, loading..."

                    # try .json
                    if exp.default_payload + '.json' in str(os.listdir('./payloads')):
                        try:
                            with open('./payloads/' + exp.default_payload + '.json', 'r') as f:
                                json_data = json.load(f)
                                class _tmp_pay(object):
                                    info = ''
                                    data = ''
                                pay = _tmp_pay()
                                pay.data = eval("str('" + json_data['data'] + "')")  # This is unsafe, and ugly.
                                exp.payload = pay.data
                                print ">Default payload: '" + exp.default_payload+ "' loaded."
                        except Exception, e:
                            print colorize('[Error]:','red'), e
                            return 0

                    # try .py
                    else:
                        try:
                            _temp = __import__('payloads.' + exp.default_payload, globals(), locals(),
                                               fromlist=['Payload'])
                            Payload = _temp.Payload
                            pay = Payload()
                            exp.payload = pay.data
                            print ">Default payload: '" + exp.default_payload+ "' loaded."
                        except Exception, e:
                            print '[Error]: ', e
            # print supported payloads
                if hasattr(exp, 'supported_payload'):
                    if type(exp.supported_payload) == str:
                        print exp.supported_payload
                    elif type(exp.supported_payload) == list:
                        for i in exp.supported_payload:
                            print i
                print_line('')
        except Exception, e:
            print colorize('[Error]: ','red'), e

    def complete_useexp(self, text, line, begidx, endidx):
        return [i for i in exploit_list if i.startswith(text)]

    @update_prompt
    def do_usepay(self, name):
        '''Use a payload
Format: usepay payload_name'''
        global pay
        # check
        if not exp:
            print colorize('[Error]: ','red'), 'You should use an exploit before use a payload.'
            return
        else:
            if not hasattr(exp, 'default_payload'):
                print colorize('[Error]: ','red'), 'Current exploit does not support change payload.'
                return
        # load payload
        # try .json first
        if name + '.json' in str(os.listdir('./payloads')):
            try:
                with open('./payloads/' + name + '.json', 'r') as f:
                    json_data = json.load(f)

                    class _tmp_pay(object):
                        info = ''
                        data = ''

                    pay = _tmp_pay()
                    pay.info = json_data['info']
                    pay.data = eval("str('" + json_data['data'] + "')")  # This is unsafe, and ugly.
                    print ">Payload info:"
                    print pay.info  # who can tell me a better way? by author
                    c = raw_input("Are you sure to use the payload?(y/n):(y)")
                    if not c or c[0] != 'n':
                        exp.payload = pay.data
                    print "New payload loaded."
            except Exception, e:
                print colorize('[Error]: ','red'), e
            finally:
                return

        # try .py
        try:
            _temp = __import__('payloads.' + name, globals(), locals(), fromlist=['Payload'])
            Payload = _temp.Payload
            pay = Payload()
            print 'Payload Loaded.'
            if hasattr(exp, 'payload_requirement'):
                print '>Payload requirements of the exploit:\n', exp.payload_requirement

            c = raw_input(">Payload info:\n" + pay.info + "\nAre you sure to use the payload?(y/n):(y)")
            if not c or c[0] != 'n':
                exp.payload = pay.data
            print "New payload loaded."
        except Exception, e:
            print colorize('[Error]: ','red'), e

    def complete_usepay(self, text, line, begidx, endidx):
        return [i for i in payload_list if i.startswith(text)]

    @update_prompt
    def do_use(self, name):
        '''Try to use the vulnerability and exploit with the same name.
Format: use name
Notice: use exp/e ... equals useexp ...
        use vul/v ... equals usevul ...'''
        if len(name.split()) == 2:
            [arg, name_] = name.split()[0:2]
            if arg in ['exp', 'e', 'vul', 'v', 'p', 'pay']:
                if arg in ['exp', 'e']:
                    self.do_useexp(name_)
                elif arg in ['p', 'pay', 'payload']:
                    self.do_usepay(name_)
                else:
                    self.do_usevul(name_)
                return
        print 'Try to load vulnerability: ', name
        self.do_usevul(name)
        if not exp:
            print 'Try to load exploit: ', name
            self.do_useexp(name)

    def complete_use(self, text, line, begidx, endidx):
        if begidx == 4:
            list = self.complete_useexp(text, line, begidx, endidx)
            list.extend(self.complete_usevul(text, line, begidx, endidx))
            list.extend(['exp', 'vul', 'pay'])
            return [i for i in list if i.startswith(text)]
        else:
            if line[4] == 'e':
                return self.complete_useexp(text, line, begidx, endidx)
            elif line[4] == 'v':
                return self.complete_usevul(text, line, begidx, endidx)
            elif line[4] == 'p':
                return self.complete_usepay(text, line, begidx, endidx)

            else:
                return []

    def _check_before_running(self):
        '''Check the options.'''
        if hasattr(self, 'ignore_check_before_running'): return True
        if exp and vul:
            for _key in vul.options.keys():
                if _key in exp.options.keys():
                    if vul.options[_key] != exp.options[_key]:
                        _input = raw_input(colorize('[Warring]: ','yellow')+\
                                           'Options of vulnerability and exploit do not match,\nContinue? y/n:(n)')
                        if _input and _input[0] == 'y':
                            print "Continue, we won't warn you again."
                            self.ignore_check_before_running = True
                        else:
                            return False
        return True

    def do_run(self, name):
        '''Run vulnerability then the exploit.
Format: run
Mention: run exp/e equals runexp
         run vul/v equals runvul'''
        if name in ['exp', 'vul', 'e', 'v']:
            if name in ['exp', 'e']:
                self.do_runexp('')
            else:
                self.do_runvul('')
            return
        print 'Quick running...'
        if not vul and not exp:
            if not name:
                print colorize('[Error]: ','red'), 'No vulnerability or exploit using. Use one before running.'
                return
        print "Try to run the vulnerability."
        self.do_runvul('')
        print "Try to run the exploit."
        self.do_runexp('')

    def complete_run(self, text, line, begidx, endidx):
        return self._complete_e_or_v(text, line, begidx, endidx)

    def do_runvul(self, line):
        '''Run the vulnerability using'''
        if not self._check_before_running(): return
        if vul:
            print 'Vulnerability Running...'
            os.chdir(vul_path)
            sys.path.append(vul_path)
            vul.run()
            sys.path.remove(vul_path)
            os.chdir(root_path)
            print 'Script Finished.'
        else:
            print 'No vulnerability using. Nothing to do.'

    def do_runexp(self, line):
        '''Run the exploit using'''
        if not self._check_before_running(): return
        if exp:
            print 'Exploit Running...'
            os.chdir(vul_path)
            sys.path.append(exp_path)
            exp.run()
            sys.path.remove(exp_path)
            os.chdir(root_path)
            print 'Script Finished.'
        else:
            print 'No exploit using. Nothing to do.'

    def do_stopvul(self, line):
        '''Stop the vulnerability using'''
        if vul:
            if hasattr(vul, 'stop'):
                vul.stop()
            else:
                print colorize('[Error]: ','red'), 'This vulnerability cannot stop.'
        else:
            print colorize('[Error]: ','red'), 'No vulnerability using.'

    def do_stopexp(self, line):
        '''Stop the exploit using'''
        if exp:
            if hasattr(exp, 'stop'):
                exp.stop()
            else:
                print colorize('[Error]: ','red'), 'This exploit cannot stop.'
        else:
            print colorize('[Error]: ','red'), 'No exploit using.'

    def do_stop(self, line):
        '''Stop both vulnerability and exploit.
Notice: stop exp/e equals stopexp
        stop vul/v equals stopvul'''
        if line in ['exp', 'e', 'vul', 'v']:
            if line in ['exp', 'e']:
                self.do_stopexp('')
            else:
                self.do_stopvul('')
            return
        self.do_stopexp(line)
        self.do_stopvul(line)

    def complete_stop(self, text, line, begidx, endidx):
        return self._complete_e_or_v(text, line, begidx, endidx)

    def do_makevul(self, line):
        '''Recompile the vulnerability using'''
        if vul:
            if hasattr(vul, 'make'):
                vul.make()
            else:
                print colorize('[Error]: ','red'), 'This vulnerability cannot make.'
        else:
            print colorize('[Error]: ','red'), 'No vulnerability using.'

    def do_makeexp(self, line):
        '''Recompile the exploit using'''
        if exp:
            if hasattr(exp, 'make'):
                exp.make()
            else:
                print colorize('[Error]: ','red'), 'This exploit cannot make.'
        else:
            print colorize('[Error]: ','red'), 'No exploit using.'

    def do_make(self, line):
        '''Recompile both vulnerability and exploit.
Notice: make exp/e equals makeexp
        make vul/v equals makevul'''
        if line in ['exp', 'e', 'vul', 'v']:
            if line in ['exp', 'e']:
                self.do_makeexp('')
            else:
                self.do_makevul('')
            return
        self.do_makeexp(line)
        self.do_makevul(line)

    def complete_make(self, text, line, begidx, endidx):
        return self._complete_e_or_v(text, line, begidx, endidx)

    def do_infovul(self, line):
        '''Show the inFormation of current Vulnerability.'''
        if vul:
            if hasattr(vul, 'info'):
                print_line('Vulnerability inFormation:')
                print vul.info
            else:
                print colorize('[Error]: ','red'), 'This vulnerability has no info.'
        else:
            print colorize('[Error]: ','red'), 'No vulnerability using.'

    def do_infoexp(self, line):
        '''Show the inFormation of current Exploit.'''
        if exp:
            if hasattr(exp, 'info'):
                print_line('Exploit inFormation:')
                print exp.info
            else:
                print colorize('[Error]: ','red'), 'This exploit has no info.'
        else:
            print colorize('[Error]: ','red'), 'No exploit using.'

    def do_info(self, line):
        '''Show inFormation of both vulnerability and exploit.
Notice: info exp/e equals infoexp
        info vul/v equals infovul'''
        if line in ['exp', 'e', 'vul', 'v']:
            if line in ['exp', 'e']:
                self.do_infoexp('')
            else:
                self.do_infovul('')
            return
        self.do_infoexp(line)
        self.do_infovul(line)

    def complete_info(self, text, line, begidx, endidx):
        return self._complete_e_or_v(text, line, begidx, endidx)

    def do_set(self, args):
        '''This command will automatically find the option of vulnerability or exploit.
Format: set key value
Notice: When the vulnerability and exploit share same keys, they will change together.
        if you want to only change one of them, use 'setvul'/'setexp' command.'''
        [key, value] = args.split(' ')[0:2]
        if key in ['e', 'exp']:
            self.do_setexp(args[len(key) + 1:])
            return
        if key in ['v', 'vul']:
            self.do_setvul(args[len(key) + 1:])
            return
        suc = False  # found or not
        if vul:
            for (k, _) in vul.options.items():
                if k == key:
                    vul.options[k] = value
                    print "Vulnerability options updated."
                    suc = True
        if exp:
            for (k, _) in exp.options.items():
                if k == key:
                    exp.options[k] = value
                    print "Exploit options updated."
                    suc = True
        if not suc:
            print colorize('[Error]: ','red'), 'No such key found.'

    def complete_set(self, text, line, begidx, endidx):
        if begidx == 4:
            list = self.complete_setexp(text, line, begidx, endidx)
            list.extend(self.complete_setvul(text, line, begidx, endidx))
            list.extend(['exp', 'vul'])
            return [i for i in list if i.startswith(text)]
        else:
            if line[4] == 'e':
                return self.complete_setexp(text, line, begidx, endidx)
            elif line[4] == 'v':
                return self.complete_setvul(text, line, begidx, endidx)
            else:
                return []

    def do_setvul(self, args):
        '''See help set.'''
        [key, value] = args.split(' ')[0:2]
        suc = False  # found or not
        if vul:
            for (k, _) in vul.options.items():
                if k == key:
                    vul.options[k] = value
                    print "Vulnerability options updated."
                    suc = True
        if not suc:
            print colorize('[Error]: ','red'), 'No such key found.'

    def complete_setvul(self, text, line, begidx, endidx):
        if not vul: return []
        if not text: return vul.options.keys()
        return [i for i in vul.options.keys() if i.startswith(text)]

    def do_setexp(self, args):
        '''See help set.'''
        [key, value] = args.split(' ')[0:2]
        suc = False  # found or not
        if exp:
            for (k, _) in exp.options.items():
                if k == key:
                    exp.options[k] = value
                    print "Exploit options updated."
                    suc = True
        if not suc:
            print colorize('[Error]: ','red'), 'No such key found.'

    def complete_setexp(self, text, line, begidx, endidx):
        if not exp: return []
        if not text: return exp.options.keys()
        return [i for i in exp.options.keys() if i.startswith(text)]

    def do_tool(self, name):
        '''Call a tool.
Format: tool name'''
        try:
            _temp = __import__('misc.' + name, globals(), locals(), fromlist=['run'])
            tool = _temp.run
            os.chdir(root_path)
            tool()
        except Exception, e:
            print '[Error]:', e

    def complete_tool(self, text, line, begidx, endidx):
        return [i for i in misc_list if i.startswith(text)]

    def do_gdb(self, args):
        '''Open an gdb in a new terminal.(With '!gdb', the terminal will fall into it.)'''
        gdb()

    def do_attach(self, line):
        '''Use gdb to attach the program automatically(ELF only).
Format: attach          attach the vulnerability.
        attach  e|exp|v|vul     attach the exploit/vulnerability.'''
        file_pids = []
        _path = vul_path
        if line and line[0] == 'e': _path = exp_path

        for i in find_executable_file(_path):
            _pid = pidof(i)
            if _pid:
                for j in _pid:
                    file_pids.extend([(i, j)])

        if not file_pids:
            print colorize('[Error]: ','red'), 'Process not found.'
        else:
            max_pid = max(file_pids, key=lambda x: x[1])
            if len(file_pids) > 1:
                print colorize('[Warring]: ','yellow')+'More than one process found, attach max pid: %d' % max_pid[1]
            gdb(file_name=max_pid[0], pid=max_pid[1], path=_path)
        os.chdir(root_path)

    def do_aslr(self, line):
        '''Check status/Turn on/Turn off ASLR of system.
Format: aslr status/check/on/off/conservative'''
        if line in ['status', 'check', 'on', 'off', 'conservative']:
            if line[1] in ['h', 't']:
                state = aslr_status()
                if state == 2:
                    print "ASLR: ON\n"
                elif state == 0:
                    print "ASLR: OFF\n"
                elif state == 1:
                    print "ASLR: Conservative ON\n"
                else:
                    print "Invalid Value."
            elif line[1] == 'n':
                aslr_on()
            elif line[1] == 'f':
                aslr_off()
            elif line[1] == 'o':
                aslr_conservative()

        else:
            print colorize('[Error]: ','red'), 'Wrong Format.'
            self.do_help('aslr')

    def complete_aslr(self, text, line, begidx, endidx):
        return [i for i in ['status', 'check', 'on', 'off', 'conservative'] if i.startswith(text)]

    def do_q(self, line):
        '''Quit VRL.'''
        return True

    def _complete_e_or_v(self, text, line, begidx, endidx):
        if text:
            return [i for i in ['exp', 'vul'] if i.startswith(text)]
        else:
            return ['exp', 'vul']



# list of exp & vul & payload
exploit_list = []
vulnerability_list = []
payload_list = []
misc_list = []

# exp & vul & payload using
exp = []        # will be replaced by an Exploit instance.
vul = []        # will be replaced by a Vulnerability instance.
pay = ''        # only be replaced by payload data.

# path
root_path = sys.path[0]         # not change
exp_path = sys.path[0]          # change to exploit path
vul_path = sys.path[0]          # change to vulnerability path

VRLui = ui()

# delete unused command (make command list clear)
for attr in ['do_list', 'do_r', 'do_cmdenvironment', 'do_history', 'do_hi', 'do_save',
             'do_pause', 'do_ed', 'do_edit', 'do_EOF', 'do_eof', 'do_li', 'do_l', 'do_quit']:
    if hasattr(cmd.Cmd, attr): delattr(cmd.Cmd, attr)

VRLui.do_reload('')
VRLui.cmdloop()
