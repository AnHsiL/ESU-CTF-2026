mov	rax, 1
mov	rdi, 1
mov	rsi, 0x4000000
mov	rdx, 0xc
syscall

mov	rbx, rax
mov	r8, rcx
mov	r9, r11

mov	rax, 0x3c
mov	rdi, 0
syscall
















