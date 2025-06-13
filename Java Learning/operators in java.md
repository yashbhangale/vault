---
title: operators in java
date: 2024-09-22
categories:
  - placement
  - dsa
  - java
draft: false
---
## Operators in Java
classified into different types, such as arithmetic, relational, logical, bitwise, assignment, and more.

### Arithmetic Operators
These operators are used to perform basic mathematical operations:

- `+` (Addition)
- `-` (Subtraction)
- `*` (Multiplication)
- `/` (Division)
- `%` (Modulus - returns the remainder)

```
int a = 10 ;
int b = 10 ;
System.out.println(a+b);
System.out.println(a-b);
System.out.println(a*b);
System.out.println(a/b);
System.out.println(a%b);
```

### Relational (Comparison) Operators
These operators compare two values and return a boolean value (`true` or `false`).

- `==` (Equal to)
- `!=` (Not equal to)
- `>` (Greater than)
- `<` (Less than)
- `>=` (Greater than or equal to)
- `<=` (Less than or equal to)

```
int a = 10;
int b = 20;
System.out.println( a < b );
System.out.println( a == b );
System.out.println( a!= b);
```

### Logical Operator
These operators are used for combining multiple conditions:

- `&&` (Logical AND)
- `||` (Logical OR)
- `!` (Logical NOT)

```
int a = 10;
int b = 5;
System.out.println(a > b && a > 0); // Output: true
System.out.println(a < b || a > 0); // Output: true
System.out.println(!(a == b));      // Output: true
```

### Bitwise Operators

These operators perform operations on bits:

- `&` (Bitwise AND)
- `|` (Bitwise OR)
- `^` (Bitwise XOR)
- `~` (Bitwise NOT)
- `<<` (Left shift)
- `>>` (Right shift)
- `>>>` (Unsigned right shift)

```
int a = 5;  // Binary: 0101
int b = 3;  // Binary: 0011
System.out.println(a & b); // Output: 1  (Binary: 0001)
System.out.println(a | b); // Output: 7  (Binary: 0111)
System.out.println(a ^ b); // Output: 6  (Binary: 0110)
System.out.println(~a);    // Output: -6 (Binary: 1010)
System.out.println(a << 1); // Output: 10 (Binary: 1010)
System.out.println(a >> 1); // Output: 2  (Binary: 0010)
```

#### Assignment Operators

These operators are used to assign values to variables:

- `=` (Assigns value)
- `+=` (Add and assign)
- `-=` (Subtract and assign)
- `*=` (Multiply and assign)
- `/=` (Divide and assign)
- `%=` (Modulus and assign)

```
int a = 10;
a += 5;  // a = a + 5
System.out.println(a);  // Output: 15
```

![](https://www.allaboutcircuits.com/uploads/articles/count-using-different-kinds-of-numeration-systems.jpg)