# Based on x86-64

#### Basic structure : opcode operand1 operand2 ... ex) `mov eax 3`  
#### kind of operand : Immediate value, Register, Memory(Size Directive TYPE PTR can added before it)  
- - -
### Data Transfer
#### mov dst, src : replace value of src to dst
```assembly
mov rdi, rsi ; replace value of rsi to rdi.
mov QWORD PTR[rdi], rsi ; replace value of rsi to memory address rdi point to  
```

#### lea dst, src : store Effective Address(EA) of src to dst
```assembly
lea rsi, [rbx+8*rcx] ; store address of [rbx+8*rcx] to rsi
```
- - -
### Arithmetic
#### add dst, src : dst += src
#### sub dst, src : dst -= src
#### inc op : op += 1
#### dec op : op -= 1
- - -
### Logical
#### and, or, xor, neg ( bit calculation base)
- - -
### Comparison
#### cmp op1, op2 : compare op1 and op2 by subtraction but no substition. just set flag so that cpu read
#### test op1, op2 : compare op1 and op2 by taking `And` bit calculation but no substition. just set flag so taht cpu read
- - -
### Branch : change execution flow by moving `rip`
#### jmp addr : move rip to addr
```assembly
1: xor rax, rax
2: jmp 1
```
#### je addr : jump if equal
```assembly
1: mov rax, 0xcafebabe
2: mov rbx, 0xcafebabe
3: cmp rax, rbx ; rax == rbx
4: je 1 ; jump to 1
```
#### jg addr : jump if greater
```assembly
1: mov rax, 0x31337
2: mov rbx, 0x13337
3: cmp rax, rbx ; rax > rbx
4: jg 1  ; jump to 1
```
- - -
### Stack
#### push val : rsp-=8; [rsp]=val;
```assembly
;[Stack]
0x7fffffffc400 | 0x0  <= rsp
0x7fffffffc408 | 0x0
;[Code]
push 0x31337
```
```assembly
; AFTER
;[Stack]
0x7fffffffc3f8 | 0x31337 <= rsp 
0x7fffffffc400 | 0x0
0x7fffffffc408 | 0x0
```
#### pop reg : reg=[rsp]; rsp+=8;
```assembly
;[Stack]
0x7fffffffc3f8 | 0x31337 <= rsp 
0x7fffffffc400 | 0x0
0x7fffffffc408 | 0x0
;[Code]
pop rax
```
```assembly
; AFTER
;[Register]
rax = 0x31337
;[Stack]
0x7fffffffc400 | 0x0 <= rsp 
0x7fffffffc408 | 0x0
```
- - -
### Procedure
#### call addr : push return_address; jmp addr;
```assembly
;[Register]
rip = 0x400000
rsp = 0x7fffffffc400 
;[Stack]
0x7fffffffc3f8 | 0x0
0x7fffffffc400 | 0x0 <= rsp
;[Code]
0x400000 | call 0x401000  <= rip
0x400005 | mov esi, eax
...
0x401000 | push rbp
```
```assembly
;[Register] ;AFTER
rip = 0x401000
rsp = 0x7fffffffc3f8
;[Stack] 
0x7fffffffc3f8 | 0x400005  <= rsp
0x7fffffffc400 | 0x0
;[Code]
0x400000 | call 0x401000
0x400005 | mov esi, eax
...
0x401000 | push rbp  <= rip
```
#### leave(clear stack frame) : mov rsp, rbp; pop rbp
```assembly
;[Register]
rsp = 0x7fffffffc400
rbp = 0x7fffffffc480
;[Stack]
0x7fffffffc400 | 0x0 <= rsp
...
0x7fffffffc480 | 0x7fffffffc500 <= rbp
0x7fffffffc488 | 0x31337 
;[Code]
leave
```
```assembly
;[Register] ;AFTER
rsp = 0x7fffffffc488
rbp = 0x7fffffffc500
;[Stack]
0x7fffffffc400 | 0x0
...
0x7fffffffc480 | 0x7fffffffc500
0x7fffffffc488 | 0x31337 <= rsp
...
0x7fffffffc500 | 0x7fffffffc550 <= rbp
```
#### ret(return address) : pop rip
```assembly
;[Register]
rip = 0x401021
rsp = 0x7fffffffc3f8
;[Stack]
0x7fffffffc3f8 | 0x400005    <= rsp
0x7fffffffc400 | 0x123456789abcdef
;[Code]
0x400000 | call 0x401000
0x400005 | mov esi, eax
...
0x401000 | push rbp
0x401001 | mov rbp, rsp
0x401004 | sub rsp, 0x30
0x401008 | mov BYTE PTR [RSP], 0x3
...
0x401020 | leave
0x401021 | ret <= rip
```
```assembly
;[Register]
rip = 0x400005
rsp = 0x7fffffffc400
;[Stack]
0x7fffffffc3f8 | 0x400005
0x7fffffffc400 | 0x123456789abcdef    <= rsp
;[Code]
0x400000 | call 0x401000
0x400005 | mov esi, eax   <= rip
...
0x401000 | push rbp
0x401001 | mov rbp, rsp
0x401004 | sub rsp, 0x30
0x401008 | mov BYTE PTR [RSP], 0x3
...
0x401020 | leave
0x401021 | ret
```  

#### ___Allocation and Free of stack frame___
1. Call function. At this time, nexp instruction address will be pushed in stack. : `call func`
2. push rbp to stack to store original stack frame. : `push rbp`
3. move rbp to rsp to create new stack frame. : `mov rbp rsp`
4. subtract 0x30 from rsp to expand stack frame space. : `sub rsp 0x30`
5. allocate local variable to allocated stack frame. : `mov BYTE PTR[rsp] 0x30`
6. use any calculation on this stack frame. :  `...`
7. take stored rbp to go back to the original stack frame. : `leave`
8. take stored return address to go back to the original execution flow. : `ret`
