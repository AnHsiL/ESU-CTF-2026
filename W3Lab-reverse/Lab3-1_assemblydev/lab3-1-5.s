sub	rsp, 0x20

mov	[rsp], rax
mov	[rsp+8], rbx

mov	rax, [rsp]
add	rax, [rsp+8]

add	rsp, 0x20
