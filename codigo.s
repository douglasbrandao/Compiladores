.data

i: .word 1
f: .word 1
i: .word 1
i: .word 1
i: .word 1
	n: .word 0

.balign 4
	str"Digite qual numero deseja calcular a fatorial": .asciz 0
.balign 4
	str"akaaka": .asciz 1
.balign 4
	str"dentro do se": .asciz 2
	.balign 4
	pattern: .asciz "%d"

.text
.global main

main:

	push {ip, lr}

	ldr r0, =str0
	bl printf

	ldr r0, =pattern
	ldr r1, =n
	bl scanf

	ldr r1, =f
	ldr r1, [r1]
	ldr r2, =i
	ldr r2, [r2]
	mul r1, r1, r2
	ldr r2, =f
	str r1, [r2]

	ldr r1, =i
	ldr r1, [r1]
	mov r2, #1
	add r1, r1, r2
	ldr r2, =i
	str r1, [r2]

	ldr r0, =str1
	bl printf

	ldr r0, =pattern
	ldr r1, =i
	bl scanf

	ldr r0, =str2
	bl printf

	ldr r0, =pattern
	ldr r1, =n
	bl scanf

	pop {ip, pc}


end:
	mov r7, #1
	swi 0


.extern printf
.extern scanf
