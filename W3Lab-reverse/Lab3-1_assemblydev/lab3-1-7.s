mov	rax, 0
mov	rdi, 0
mov	rsi, 0x4000000
mov	rdx, 8
syscall

mov	rbx, rax

mov	rax, 1
mov	rdi, 1
mov	rsi, 0x4000000
mov	rdx, rbx
syscall

mov	rbp, rax
mov	r8, rcx
mov	r9, r11

mov	rax, 0x3c
mov	rdi, 0
syscall

