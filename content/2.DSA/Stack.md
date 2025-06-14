---
title: DSA Stack
date: 2024-12-25
---

Sure, let’s start preparing the **Stack** topic in DSA. Here’s a structured explanation of stacks, including their theory, operations, and applications. We'll also go through implementation details step-by-step.

---

## **What is a Stack?**

A **stack** is a linear data structure that follows the **LIFO** (Last In, First Out) principle:

- The last element inserted into the stack is the first one to be removed.

Think of a stack like a stack of plates:

- You add plates to the top (push operation).
- You remove plates from the top (pop operation).

---

### **Basic Operations on a Stack:**

1. **Push:** Add an element to the top of the stack.
2. **Pop:** Remove the top element from the stack.
3. **Peek/Top:** View the top element without removing it.
4. **IsEmpty:** Check if the stack is empty.
5. **Size:** Get the number of elements in the stack.

---

### **Key Points to Remember:**

1. **LIFO Principle:** Last in, first out.
2. **Fixed vs. Dynamic Size:**
    - Array-based stacks are of fixed size.
    - Linked list-based stacks can grow dynamically.
3. **Overflow/Underflow:**
    - Overflow occurs when the stack is full and you try to push.
    - Underflow occurs when the stack is empty and you try to pop.

---

### **Types of Stacks:**

1. **Static Stack:**
    - Implemented using arrays.
    - Fixed size, might cause overflow.
2. **Dynamic Stack:**
    - Implemented using linked lists.
    - Can grow/shrink dynamically based on needs.

---

### **Stack Representation (Diagram):**

For a stack with elements `{5, 10, 15}`:

```
Top -> 15
        10
         5
```

---

### **Applications of Stack:**

1. **Expression Evaluation:**
    - Infix to postfix conversion.
    - Evaluation of postfix expressions.
2. **Backtracking:**
    - Used in recursive algorithms like maze-solving or DFS.
3. **Function Call Stack:**
    - Keeps track of function calls during recursion.
4. **Browser History:**
    - Navigate back and forth in browser tabs.
5. **Undo/Redo Operations:**
    - In text editors or IDEs.

---

## **How to Implement a Stack?**

### **1. Array-Based Stack:**

#### Code Example:

```java
class Stack {
    private int arr[];
    private int top;
    private int capacity;

    // Constructor to initialize the stack
    public Stack(int size) {
        arr = new int[size];
        capacity = size;
        top = -1;
    }

    // Push operation
    public void push(int x) {
        if (top == capacity - 1) {
            System.out.println("Stack Overflow");
            return;
        }
        arr[++top] = x;
    }

    // Pop operation
    public int pop() {
        if (top == -1) {
            System.out.println("Stack Underflow");
            return -1;
        }
        return arr[top--];
    }

    // Peek operation
    public int peek() {
        if (top == -1) {
            System.out.println("Stack is empty");
            return -1;
        }
        return arr[top];
    }

    // Check if stack is empty
    public boolean isEmpty() {
        return top == -1;
    }
}
```

---

### **2. Linked List-Based Stack:**

#### Code Example:

```java
class Node {
    int data;
    Node next;

    Node(int data) {
        this.data = data;
        next = null;
    }
}

class Stack {
    private Node top;

    // Push operation
    public void push(int x) {
        Node newNode = new Node(x);
        newNode.next = top;
        top = newNode;
    }

    // Pop operation
    public int pop() {
        if (top == null) {
            System.out.println("Stack Underflow");
            return -1;
        }
        int data = top.data;
        top = top.next;
        return data;
    }

    // Peek operation
    public int peek() {
        if (top == null) {
            System.out.println("Stack is empty");
            return -1;
        }
        return top.data;
    }

    // Check if stack is empty
    public boolean isEmpty() {
        return top == null;
    }
}
```

---

## **Stack Problems to Practice:**

### Easy:

1. **Reverse a string using a stack.**
    - Input: `"abcd"`, Output: `"dcba"`.
2. **Check for balanced parentheses in an expression.**
    - Input: `"({[()]})"`, Output: `true`.

### Medium:

1. **Next Greater Element.**
    - Input: `{4, 5, 2, 10}`, Output: `{5, 10, 10, -1}`.
2. **Sort a stack using recursion.**

---

Let me know if you want to dive deeper into any specific topic, code, or problem related to stacks!