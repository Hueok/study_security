# Based on x86-64

#### Basic structure : opcode operand1 operand2 ... ex) `mov eax 3`  
#### kind of operand : Immediate value, Register, Memory(Size Directive TYPE PTR can added before it)  

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

### Arithmetic
#### add dst, src : dst += src
#### sub dst, src : dst -= src
#### inc op : op += 1
#### dec op : op -= 1

### Logical
#### and, or, xor, neg ( bit calculation base)

### Comparison
#### cmp op1, op2 : compare op1 and op2 by subtraction but no substition. just set flag so that cpu read
#### test op1, op2 : compare op1 and op2 by taking `And` bit calculation but no substition. just set flag so taht cpu read

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
