.text
.global main

main:

push {ip, lr}

ldr r1, =n1
ldr r2, =n2
cmp r1, r2
bgt _C12
ldr r0, =str0
bl printf

pop {ip, pc}
_C12:
ldr r0, =str1
bl printf


end:
mov r7, #1
swi 0


.extern printf
.extern scanf


.data
n1: .word 5
n2: .word 3
.balign 4
str0: .asciz "n1 e menor ou igual n2\n"
.balign 4
str1: .asciz "maior que n1\n"
.balign 4
pattern: .asciz "%d"