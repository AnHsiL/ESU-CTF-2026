from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

r = process('./hello')

gdb.attach(r)

r.sendlineafter(b': ', b'Curious')
r.interactive()
