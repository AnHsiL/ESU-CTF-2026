#Reverse 
## 題目

**assemblydev**
Write assembly to earn the flag

`nc chals1 13020`

## 解題
共 7 小題，把演算法用 ASM 寫完後，透過
```bash
base64 -w 0 [檔案名稱]
```
轉成 base64 提交

##### 1
```bash
# Modify register values
RAX += 0x87
RBX -= 0x63
RCX, RDX = RDX, RCX

# Modify memory values
MEM[RSP+0x0:RSP+0x4] += 0xdeadbeef
MEM[RSP+0x4:RSP+0x8] -= 0xfaceb00c
MEM[RSP+0x8:RSP+0xc], MEM[RSP+0xc:RSP+0x10] =     MEM[RSP+0xc:RSP+0x10], MEM[RSP+0x8:RSP+0xc]

Give me the base64 of your assembly source!
```
答
```armasm
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
```
base64
```
YWRkIHJheCwgMHg4NwpzdWIgcmJ4LCAweDYzCnhjaGcgcmN4LCByZHgKCm1vdiByOGQsIDB4ZGVhZGJlZWYKYWRkIFtyc3BdLCByOGQKbW92IHI4ZCwgMHhmYWNlYjAwYwpzdWIgW3JzcCs0XSwgcjhkCgptb3YgcjhkLCBbcnNwKzhdCm1vdiByOWQsIFtyc3ArMHhjXQptb3YgW3JzcCsweGNdLCByOGQKbW92IFtyc3ArOF0sIHI5ZAo=
```

##### 2
```
let a = MEM[RSP+0x0:RSP+0x4]
let b = MEM[RSP+0x4:RSP+0x8]
let c = MEM[RSP+0x8:RSP+0xc]

EAX = a + b
EBX = a - b
ECX = -c
EDX = 9*a + 7
```
答
```armasm
mov     r8d, [rsp] ; a
mov     r9d, [rsp+4] ; b
mov     r10d, [rsp+8] ; c

mov     eax, r8d
add     eax, r9d

mov     ebx, r8d
sub     ebx, r9d

mov     ecx, r10d
neg     ecx

imul	edx, r8d, 9
add     edx, 7
```
base64
```
bW92CXI4ZCwgW3JzcF0gOyBhCm1vdiAgICAgcjlkLCBbcnNwKzRdIDsgYgptb3YgICAgIHIxMGQsIFtyc3ArOF0gOyBjCgptb3YJZWF4LCByOGQKYWRkCWVheCwgcjlkCgptb3YJZWJ4LCByOGQKc3ViCWVieCwgcjlkCgptb3YJZWN4LCByMTBkCm5lZwllY3gKCmltdWwJZWR4LCByOGQsIDkKYWRkCWVkeCwgNwoKCg==
```

##### 3
```
let a = MEM[RSP+0x0:RSP+0x4]
let b = MEM[RSP+0x4:RSP+0x8]
let c = MEM[RSP+0x8:RSP+0xc]
let d = MEM[RSP+0xc:RSP+0x10]

# a and b are signed 4-byte integers
EAX = max(a, b)

# c and d are unsigned 4-byte integers
EBX = min(c, d)

if c is odd:
    ECX = c // 8
else:
    ECX = c * 4
```
答
```armasm
mov     r8d, [rsp] ; a
mov     r9d, [rsp+4] ; b
mov     r10d, [rsp+8] ; c
mov     r11d, [rsp+0xc] ; d

mov     eax, r8d
cmp     eax, r9d
cmovl	eax, r9d

mov     ebx, r10d
cmp     ebx, r11d
cmova	ebx, r11d

test	r10d, 1
jz	    even

; odd
mov     ecx, r10d
shr     ecx, 3
jmp     done

; even
even:
mov     ecx, r10d
shl     ecx, 2

done:
```
base64
```
bW92ICAgICByOGQsIFtyc3BdIDsgYQptb3YgICAgIHI5ZCwgW3JzcCs0XSA7IGIKbW92ICAgICByMTBkLCBbcnNwKzhdIDsgYwptb3YgICAgIHIxMWQsIFtyc3ArMHhjXSA7IGQKCm1vdiAgICAgZWF4LCByOGQKY21wCWVheCwgcjlkCmNtb3ZsCWVheCwgcjlkCgptb3YgICAgIGVieCwgcjEwZApjbXAgICAgIGVieCwgcjExZApjbW92YQllYngsIHIxMWQKCnRlc3QJcjEwZCwgMQpqeglldmVuCgo7IG9kZAptb3YJZWN4LCByMTBkCnNocgllY3gsIDMKam1wCWRvbmUKCjsgZXZlbgpldmVuOgptb3YJZWN4LCByMTBkCnNobAllY3gsIDIKCmRvbmU6Cg==
```
##### 4
```
Use PUSH and POP to place RAX, RBX, and RCX on the stack in that order.
Pop all three values back to demonstrate LIFO order:

RDX = original RCX
RSI = original RBX
RDI = original RAX

Restore RSP to its initial value before the code finishes.
```
答
```armasm
push    rax
push    rbx
push    rcx

pop     rdx
pop     rsi
pop     rdi
```
base64
```
cHVzaAlyYXgKcHVzaAlyYngKcHVzaAlyY3gKCnBvcAlyZHgKcG9wCXJzaQpwb3AJcmRpCg==
```
##### 5
```
Create a 0x20-byte stack-local area.

1. Save the original RAX at [RSP+0x0].
2. Save the original RBX at [RSP+0x8].
3. Set RAX to the sum of those two qwords by reading the local copies.
4. Release the local area and restore RSP to its initial value.
```
答
```armasm
sub     rsp, 0x20

mov     [rsp], rax
mov     [rsp+8], rbx

mov     rax, [rsp]
add     rax, [rsp+8]

add     rsp, 0x20
```
base64
```
c3ViCXJzcCwgMHgyMAoKbW92CVtyc3BdLCByYXgKbW92CVtyc3ArOF0sIHJieAoKbW92CXJheCwgW3JzcF0KYWRkCXJheCwgW3JzcCs4XQoKYWRkCXJzcCwgMHgyMAo=
```
##### 6
```
The checker placed 12 bytes at 0x4000000.

1. Use Linux x86-64 write(1, 0x4000000, 0xc).
2. Copy the write return value from RAX to RBX.
3. Immediately copy the post-SYSCALL RCX to R8 and R11 to R9.
4. Use exit(0) with syscall number 0x3c.

Recall: RAX is the syscall number; arguments are RDI, RSI, RDX, R10, R8,
and R9. SYSCALL clobbers RCX and R11.
```
答
```armasm
mov     rax, 1
mov     rdi, 1
mov     rsi, 0x4000000
mov     rdx, 0xc
syscall

mov     rbx, rax
mov     r8, rcx
mov     r9, r11

mov     rax, 0x3c
mov     rdi, 0
syscall
```
base64
```
bW92CXJheCwgMQptb3YJcmRpLCAxCm1vdglyc2ksIDB4NDAwMDAwMAptb3YJcmR4LCAweGMKc3lzY2FsbAoKbW92CXJieCwgcmF4Cm1vdglyOCwgcmN4Cm1vdglyOSwgcjExCgptb3YJcmF4LCAweDNjCm1vdglyZGksIDAKc3lzY2FsbAoKCgoKCgoKCgoKCgoKCgoK
```
##### 7
```
The checker has 8 bytes of simulated stdin.

1. Use read(0, 0x4000000, 8).
2. Copy the read return value from RAX to RBX.
3. Use write(1, 0x4000000, RAX_from_read) to echo the bytes.
4. Copy the write return value from RAX to RBP.
5. Immediately copy the post-write RCX to R8 and R11 to R9.
6. Use exit(0) with syscall number 0x3c.

No syscall reaches the host. The checker only models read, write, and exit.
```
答
```armasm
mov     rax, 0
mov     rdi, 0
mov     rsi, 0x4000000
mov     rdx, 8
syscall

mov     rbx, rax

mov     rax, 1
mov     rdi, 1
mov     rsi, 0x4000000
mov     rdx, rbx
syscall

mov     rbp, rax
mov     r8, rcx
mov     r9, r11

mov     rax, 0x3c
mov     rdi, 0
syscall
```
base64
```
bW92CXJheCwgMAptb3YJcmRpLCAwCm1vdglyc2ksIDB4NDAwMDAwMAptb3YJcmR4LCA4CnN5c2NhbGwKCm1vdglyYngsIHJheAoKbW92CXJheCwgMQptb3YJcmRpLCAxCm1vdglyc2ksIDB4NDAwMDAwMAptb3YJcmR4LCByYngKc3lzY2FsbAoKbW92CXJicCwgcmF4Cm1vdglyOCwgcmN4Cm1vdglyOSwgcjExCgptb3YJcmF4LCAweDNjCm1vdglyZGksIDAKc3lzY2FsbAoK
```

##### flag
- flag = `FLAG{trUe_As53mb1y_wr1t3r}`