mov	r8d, [rsp] ; a
mov     r9d, [rsp+4] ; b
mov     r10d, [rsp+8] ; c

mov	eax, r8d
add	eax, r9d

mov	ebx, r8d
sub	ebx, r9d

mov	ecx, r10d
neg	ecx

imul	edx, r8d, 9
add	edx, 7


