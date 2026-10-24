add rax, 0x87
sub rbx, 0x63
xchg rcx, rdx

mov r8d, 0xdeadbeef
add [rsp], r8d
mov r8d, 0xfaceb00c
sub [rsp+4], r8d

mov r8d, [rsp+8]
mov r9d, [rsp+0xc]
mov [rsp+0xc], r8d
mov [rsp+8], r9d
