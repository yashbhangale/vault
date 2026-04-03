---
title: DSA loops questions for interviews
tags: [dsa]
date: 2025-01-04
---
********
Haan bhai, **loops ke questions** interview mein kaafi common hote hain, kyunki isse tumhari **logic building** aur **time complexity ka samajh** test karte hain. Chal, kuch **popular loop-based questions** aur unke approaches dekhte hain:

---

### **1. Print Patterns**

#### **Question**:

Print this pattern:

```
*
**
***
****
*****
```

#### **Approach**:

- Use nested loops: Outer loop controls rows, inner loop controls columns.

```java
for (int i = 1; i <= 5; i++) {
    for (int j = 1; j <= i; j++) {
        System.out.print("*");
    }
    System.out.println();
}
```

**Output**:  
`O(n²)` (Outer loop: `O(n)`, Inner loop: `O(n)` for each row).

---

### **2. Reverse a Number**

#### **Question**:

Reverse the digits of a number (e.g., `12345` → `54321`).

#### **Approach**:

- Use a `while` loop to extract digits and reverse them.

```java
int num = 12345, reversed = 0;
while (num != 0) {
    int digit = num % 10;
    reversed = reversed * 10 + digit;
    num /= 10;
}
System.out.println(reversed);
```

**Time Complexity**: `O(d)` (where `d` = number of digits).

---

### **3. Check Prime Number**

#### **Question**:

Write a program to check if a number is prime.

#### **Approach**:

- Use a loop to check divisors up to n\sqrt{n}.

```java
boolean isPrime = true;
int n = 29;
for (int i = 2; i <= Math.sqrt(n); i++) {
    if (n % i == 0) {
        isPrime = false;
        break;
    }
}
System.out.println(isPrime ? "Prime" : "Not Prime");
```

**Time Complexity**: `O(√n)`.

---

### **4. Find the Largest and Smallest in an Array**

#### **Question**:

Find the largest and smallest numbers in an array.

#### **Approach**:

- Use a single loop to compare each element.

```java
int[] arr = {3, 5, 7, 2, 8};
int max = arr[0], min = arr[0];
for (int num : arr) {
    if (num > max) max = num;
    if (num < min) min = num;
}
System.out.println("Max: " + max + ", Min: " + min);
```

**Time Complexity**: `O(n)`.

---

### **5. Count Frequency of Each Element in an Array**

#### **Question**:

Count the frequency of each element in an array.

#### **Approach**:

- Use nested loops or a HashMap for efficient counting.

```java
int[] arr = {1, 2, 2, 3, 3, 3};
Map<Integer, Integer> frequency = new HashMap<>();
for (int num : arr) {
    frequency.put(num, frequency.getOrDefault(num, 0) + 1);
}
System.out.println(frequency);
```

**Time Complexity**: `O(n)` (using HashMap).

---

### **6. Find Sum of Digits of a Number**

#### **Question**:

Find the sum of digits in a number (e.g., `123` → `1 + 2 + 3 = 6`).

#### **Approach**:

- Use a `while` loop to extract digits and sum them.

```java
int num = 123, sum = 0;
while (num != 0) {
    sum += num % 10;
    num /= 10;
}
System.out.println(sum);
```

**Time Complexity**: `O(d)` (where `d` = number of digits).

---

### **7. Find Factorial of a Number**

#### **Question**:

Find the factorial of a number (e.g., `5! = 5 × 4 × 3 × 2 × 1 = 120`).

#### **Approach**:

- Use a `for` loop for multiplication.

```java
int n = 5, fact = 1;
for (int i = 1; i <= n; i++) {
    fact *= i;
}
System.out.println(fact);
```

**Time Complexity**: `O(n)`.

---

### **8. Fibonacci Series**

#### **Question**:

Generate the first `n` Fibonacci numbers.

#### **Approach**:

- Use a `for` loop to calculate Fibonacci iteratively.

```java
int n = 10, a = 0, b = 1;
System.out.print(a + " " + b + " ");
for (int i = 2; i < n; i++) {
    int next = a + b;
    System.out.print(next + " ");
    a = b;
    b = next;
}
```

**Time Complexity**: `O(n)`.

---

### **9. Print All Pairs in an Array**

#### **Question**:

Print all pairs of numbers from an array.

#### **Approach**:

- Use nested loops to generate pairs.

```java
int[] arr = {1, 2, 3};
for (int i = 0; i < arr.length; i++) {
    for (int j = i + 1; j < arr.length; j++) {
        System.out.println(arr[i] + ", " + arr[j]);
    }
}
```

**Time Complexity**: `O(n²)`.

---

### **10. Check for Palindrome String**

#### **Question**:

Check if a string is a palindrome (e.g., `madam`).

#### **Approach**:

- Use a `for` loop to compare characters from both ends.

```java
String str = "madam";
boolean isPalindrome = true;
for (int i = 0; i < str.length() / 2; i++) {
    if (str.charAt(i) != str.charAt(str.length() - 1 - i)) {
        isPalindrome = false;
        break;
    }
}
System.out.println(isPalindrome ? "Palindrome" : "Not Palindrome");
```

**Time Complexity**: `O(n)`.

---

### **11. Count Number of Words in a Sentence**

#### **Question**:

Count the number of words in a sentence.

#### **Approach**:

- Use a loop to split and count words.

```java
String sentence = "This is a test sentence";
String[] words = sentence.split(" ");
System.out.println("Word count: " + words.length);
```

**Time Complexity**: `O(n)`.

---

### **12. Find GCD of Two Numbers**

#### **Question**:

Find the greatest common divisor (GCD) of two numbers.

#### **Approach**:

- Use a `while` loop with the Euclidean algorithm.

```java
int a = 56, b = 98;
while (b != 0) {
    int temp = b;
    b = a % b;
    a = temp;
}
System.out.println("GCD: " + a);
```

**Time Complexity**: `O(log(min(a, b)))`.

---

Bhai, inn questions ko achhi tarah practice kar lo. Interview mein loops ke alag-alag variations pooch sakte hain. Agar kisi question ka doubt ho, toh turant pooch lena! 🚀