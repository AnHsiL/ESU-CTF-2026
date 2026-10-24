mov     r8d, [rsp] ; a
mov     r9d, [rsp+4] ; b
mov     r10d, [rsp+8] ; c
mov     r11d, [rsp+0xc] ; d

mov     eax, r8d
cmp	eax, r9d
cmovl	eax, r9d

mov     ebx, r10d
cmp     ebx, r11d
cmova	ebx, r11d

test	r10d, 1
jz	even

; odd
mov	ecx, r10d
shr	ecx, 3
jmp	done

; even
even:
mov	ecx, r10d
shl	ecx, 2

done:
