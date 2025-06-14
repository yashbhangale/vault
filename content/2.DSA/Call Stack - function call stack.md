---
title: 2.DSA Call Stack - function call stack
date: 2025-01-14
---

![[Pasted image 20250114060144.png]]


It is a LIFO (Last In, First Out) structure used to keep track of method calls during the execution of a program

- The **call stack** is a runtime stack maintained by the Java Virtual Machine (JVM).
- It stores information about method invocations (calls) for the currently executing thread.
- Each method call creates a **stack frame**, which holds:
    - Local variables.
    - Parameters passed to the method.
    - Return address (where the method should return after execution).
    - Temporary data like intermediate results.

![[Pasted image 20250114060921.png]]

### Call stack in recursion

![[Pasted image 20250114061031.png]]

---
### **6. Real-World Applications**

- **Backtracking Algorithms**: E.g., solving mazes, Sudoku, N-Queens problem.
- **DFS (Depth First Search)**: For traversing trees and graphs.
- **Function Execution**: Handles function calls and returns in programming.

---
### **Key Points**

- The call stack operates on LIFO.
- Each method call creates a stack frame that is pushed and popped during execution.
- Deep recursion can lead to `StackOverflowError`.
- Proper base cases in recursion ensure efficient stack usage