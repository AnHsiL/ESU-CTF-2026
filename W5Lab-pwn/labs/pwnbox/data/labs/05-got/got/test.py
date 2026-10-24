from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

elf = ELF('./got', checksec=False)
got = elf.got['puts']
plt = elf.plt['puts']

log.info('puts@got = %#x', got)
log.info('puts@plt = %#x', plt)

# 斷點下在 puts@plt，兩次呼叫都會停；每次停下來自動印一次 puts@got。
# 第一次停：GOT 還指回 .plt 的 stub（lazy binding 還沒發生）
# 第二次停：GOT 已經是 libc 裡 puts 的位址，不再經過 loader
gdbscript = f'''
set pagination off
define hook-stop
  printf "puts@got -> "
  x/gx {hex(got)}
end
b *{hex(plt)}
'''

r = process('./got')
gdb.attach(r, gdbscript)
r.interactive()
