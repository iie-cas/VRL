#! /usr/bin/python
#coding:utf-8

#import sys
import os
try:
    import cmd2 as cmd
except ImportError:
    import cmd

#from modules import *
#import vulnerabilities
#import exploits


class ui(cmd.Cmd):
    prompt = '(VRL)'
    intro = 'Welcome to VRL'

    def do_reload(self,line):
        '''Reload all exploits,vulnerabilities,payloads,etc.
        When VRL started, loading is done.
        So you only need to use this when you add something new and do not want to restart VRL.'''
        global exploit_list, vulnerability_list, payload_list
        exploit_list=[]
        vulnerability_list=[]
        payload_list=[]
        for type in ['exploits','vulnerabilities']:
            subpath=os.path.join(os.curdir,type)
            for name in os.listdir(subpath):
                if os.path.isdir(os.path.join(subpath,name)):
                    if 'run.py' in os.listdir(os.path.join(subpath,name)):
                        if type=='exploits': exploit_list.append(str(name))
                        if type=='vulnerabilities': vulnerability_list.append(str(name))
        for i in os.listdir(os.path.join(os.curdir,'payloads')):
            [a,b]=os.path.splitext(str(i))
            if b == '.py':
                if a != '__init__':
                    payload_list.append(a)

    def do_guide(self,line):
        '''Show a simple guide.'''
        print '''
        Simple guide:
        help command or ?[command] for help.
        show command for list vulnerabilities and exploits.
        use command for load vulnerabilities and exploits.
        run command for run vulnerabilities and exploits.
        For more commands, use help command to list all, or read the document.
        Following command is related to the VRL:
        reload | guide | show
        usevul | useexp
        run | runvul |runexp
        stop | stopvul |stopexp
        set | setvul | setexp
        '''

    def do_show(self,type):
        '''Show all exploits|vulnerabilities|payload|options
        format: list exploit|vulnerabilities|payload|options (e|v|p|o for short.)'''
        if type:
            path={'e':exploit_list, 'v':vulnerability_list,'p':payload_list}
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

    def do_usepay(self,name):
        '''Use a payload
        format: usepay payload_name'''
        global pay
        #check
        if not exp:
            print 'Error: You should use an exploit before use a payload.'
            return
        else:
            if not hasattr(exp,'payload'):
                print 'Error: Current exploit does not support change payload.'
                return
        #load payload
        try:
            _temp = __import__('payloads.'+name,globals(),locals(),fromlist=['Payload'])
            Payload =  _temp.Payload
            pay = Payload()
            print 'Payload Loaded.'
            if hasattr(exp,'payload_info'):
                print 'Payload requirements of the exploit:\n',exp.payload_info

            c = raw_input("Payload info:\n"+pay.info+"\nAre you sure to use the payload?(y/n):(y)")
            if not c or c[0] != 'n':
                exp.payload = pay.data
        except Exception,e:
            print e



    def do_use(self,name):
        '''Load the vulnerability and exploit with same name.
        format: use name
        Notice: use exp/e ... equals useexp ...
                use vul/v ... equals usevul ...'''
        [arg,name_] = name.split()[0:2]
        if arg in ['exp','e','vul','v', 'p','pay']:
            if arg in ['exp','e']:
                self.do_useexp(name_)
            elif arg in ['p','pay','payload']:
                self.do_usepay(name_)
            else:
                self.do_usevul(name_)
            return

        self.do_usevul(name)
        self.do_useexp(name)

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

    def do_stop(self,line):
        '''Stop both vulnerability and exploit.
        Notice: stop exp/e equals stopexp
                stop vul/v equals stopvul'''
        if line in ['exp','e','vul','v']:
            if line in ['exp','e']:
                self.do_stopexp('')
            else:
                self.do_stopvul('')
            return
        self.do_stopexp(line)
        self.do_stopvul(line)

    def do_run(self,name):
        '''Quick run a vulnerability and it's default exploit with default options
        format: run []
        Metion: run exp/e equals runexp
                run vul/v equals runvul'''
        if name in ['exp','vul','e','v']:
            if name in ['exp','e']:
                self.do_runexp('')
            else:
                self.do_runvul('')
            return
        print 'Quick running...'
        if not vul and not exp:
            if not name:
                print "No vulnerability or exploit using, enter a name to quick run."
                return
            self.do_usevul(name)
        self.do_runvul('')
        self.do_runexp('')

    def do_set(self,args):
        '''This command will automatically find the option of vulnerability or exploit.
        format: set key value
        Notice: When the vulnerability and exploit share same keys, they will change together.
                 if you want to only change one of them, use 'setvul'/'setexp' command.'''
        [key,value] = args.split(' ')[0:2]
        suc = False         # found or not
        if vul:
            for (k,_) in vul.options.items():
                if k == key:
                    vul.options[k] = value
                    print "Vulnerability options updated."
                    suc = True
        if exp:
            for (k,_) in exp.options.items():
                if k == key:
                    exp.options[k] = value
                    print "Exploit options updated."
                    suc = True
        if not suc:
            print "Error: no such key found."

    def do_setvul(self,args):
        '''See help set.'''
        [key,value] = args.split(' ')[0:2]
        suc = False         # found or not
        if vul:
            for (k,_) in vul.options.items():
                if k == key:
                    vul.options[k] = value
                    print "Vulnerability options updated."
                    suc = True
        if not suc:
            print "Error: no such key found."

    def do_setexp(self,args):
        '''See help set.'''
        [key,value] = args.split(' ')[0:2]
        suc = False         # found or not
        if exp:
            for (k,_) in exp.options.items():
                if k == key:
                    exp.options[k] = value
                    print "Exploit options updated."
                    suc = True
        if not suc:
            print "Error: no such key found."

    def do_q(self,line):
        '''Quit VRL.'''
        return True


#list of exp & vul & payload
exploit_list=[]
vulnerability_list=[]
payload_list= []
#exp & vul & payload using
exp=[]
vul=[]
pay=''

VRLui=ui()

#delete unused command (make command list clear)
for attr in ['do_exit','do_list','do_r','do_cmdenvironment','do_history','do_hi','do_save',
             'do_pause','do_ed','do_edit','do_EOF','do_eof','do_li','do_l','do_quit']:
    if hasattr(cmd.Cmd,attr): delattr(cmd.Cmd,attr)

VRLui.do_reload('')
VRLui.cmdloop()

