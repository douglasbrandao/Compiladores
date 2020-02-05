.data

	.balign 4
	n1: .word 0

	.balign 4
	pattern: .asciz "%d"

.text
.global main

main:

	push {ip, lr}

	ldr r0, =pattern
	ldr r1, =n1
	bl scanf

	pop {ip, pc}


end:
	mov r7, #1
	swi 0


.extern printf
.extern scanf
