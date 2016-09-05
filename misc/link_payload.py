#! /usr/bin/python
# coding:utf-8

import json
import os
import sys

sys.path.append("../..")

'''Interactive payloads link tool'''

try:
    import cmd2 as cmd
except ImportError:
    import cmd


class link_payload(cmd.Cmd):
    prompt = 'Link_Payload > '
    intro = \
        '''
    This is an easy tool for payload linking(or save a customized payload).
    Use 'add payload' to add a new payload to your new payload.
    Use 'save' to link them all.
    'q' for quit!'''
    data = str("")
    info = "Linked payload, from:\n"
    payload_list = []
    for i in os.listdir(os.path.join(os.curdir, 'payloads')):
        [a, b] = os.path.splitext(str(i))
        if b in ['.py', '.json']:
            if a != '__init__':
                payload_list.append(a)

    def do_add(self, name):
        '''Add a payload
        format: add payload_name'''
        # load payload
        # try .json first
        if name + '.json' in str(os.listdir('payloads')):
            try:
                with open('payloads/' + name + '.json', 'r') as f:
                    json_data = json.load(f)

                    class _tmp_pay(object):
                        info = ''
                        data = str('')

                    pay = _tmp_pay()
                    pay.info = json_data['info']
                    pay.data = eval("str('" + json_data['data'] + "')")
                    print ">Payload info:"
                    print pay.info
                    c = raw_input("Are you sure to add the payload?(y/n):(y)")
                    if not c or c[0] != 'n':
                        self.info += name + ' '
                        self.data += pay.data
                    print "New payload added."
            except Exception, e:
                print '[Error]: ', e
            finally:
                return

        # try .py
        try:
            _temp = __import__('payloads.' + name, globals(), locals(), fromlist=['Payload'])
            Payload = _temp.Payload
            pay = Payload()
            print 'Payload Loaded.'
            c = raw_input(">Payload info:\n" + pay.info + "\nAre you sure to add the payload?(y/n):(y)")
            if not c or c[0] != 'n':
                self.info += name + ' '
                self.data += pay.data
            print "New payload added."
        except Exception, e:
            print '[Error]: ', e

    def do_save(self, line):
        name = raw_input("Enter a new name:")
        if not name:
            print '[Error]: Empty name.'
            return
        else:
            if name in [a.split('.')[0] for a in os.listdir('payloads')]:
                c = ''
                while not c:
                    c = raw_input("Payload name exist, overwrite?(y/n)")
                if c[0] != 'y': return
            with open('payloads/' + name + '.json', 'w') as f:
                # convert str to '\xAA' mode
                new_data = ''
                for i in self.data:
                    new_data += '\\x%02x' % ord(i)
                json_data = {
                    "info": self.info,
                    'data': new_data
                }
                json.dump(json_data, f, indent=4)
                print 'New payload saved.'
                return True

    def complete_save(self, text, line, begidx, endidx):
        return [i for i in self.payload_list if i.startswith(text)]


def run():
    _link = link_payload()
    _link.cmdloop()
