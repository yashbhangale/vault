---
title: bit manipulation in java
categories:
  - placement
  - dsa
  - java
date: 2024-09-22
---
Bit manipulation is a powerful tool in programming that involves directly operating on bits (0s and 1s) of data.
often used to optimize code for speed and memory usage in performance-critical applications.
Java provides a set of bitwise operators that allow manipulation of individual bits.

### Bit Manipulation in Java

Bit manipulation is a powerful tool in programming that involves directly operating on bits (0s and 1s) of data. It is often used to optimize code for speed and memory usage in performance-critical applications. Java provides a set of bitwise operators that allow manipulation of individual bits.

### Common Bitwise Operators in Java

1. **Bitwise AND (`&`)**: 
   Compares each bit of two numbers and returns `1` if both bits are `1`, otherwise returns `0`.

   Example:
   ```java
   int a = 5;  // 0101 in binary
   int b = 3;  // 0011 in binary
   int result = a & b;  // 0001 in binary (1 in decimal)
   System.out.println(result);  // Output: 1
   ```

2. **Bitwise OR (`|`)**: 
   Compares each bit of two numbers and returns `1` if at least one of the bits is `1`, otherwise returns `0`.

   Example:
   ```java
   int a = 5;  // 0101 in binary
   int b = 3;  // 0011 in binary
   int result = a | b;  // 0111 in binary (7 in decimal)
   System.out.println(result);  // Output: 7
   ```

3. **Bitwise XOR (`^`)**: 
   Compares each bit of two numbers and returns `1` if the bits are different, and `0` if they are the same.

   Example:
   ```java
   int a = 5;  // 0101 in binary
   int b = 3;  // 0011 in binary
   int result = a ^ b;  // 0110 in binary (6 in decimal)
   System.out.println(result);  // Output: 6
   ```

4. **Bitwise NOT (`~`)**: 
   Inverts all the bits of a number (1 becomes 0, and 0 becomes 1).

   Example:
   ```java
   int a = 5;  // 0101 in binary
   int result = ~a;  // 1010 in binary (-6 in decimal due to two's complement representation)
   System.out.println(result);  // Output: -6
   ```

5. **Left Shift (`<<`)**: 
   Shifts the bits of the number to the left by the specified number of positions. This effectively multiplies the number by `2^n` (where `n` is the number of positions shifted).

   Example:
   ```java
   int a = 5;  // 0101 in binary
   int result = a << 1;  // 1010 in binary (10 in decimal)
   System.out.println(result);  // Output: 10
   ```

6. **Right Shift (`>>`)**: 
   Shifts the bits of the number to the right by the specified number of positions. This effectively divides the number by `2^n` (where `n` is the number of positions shifted), but keeps the sign bit intact (preserving the sign for negative numbers).

   Example:
   ```java
   int a = 10;  // 1010 in binary
   int result = a >> 1;  // 0101 in binary (5 in decimal)
   System.out.println(result);  // Output: 5
   ```

7. **Unsigned Right Shift (`>>>`)**: 
   Shifts the bits of the number to the right, but does not preserve the sign bit. It inserts `0` in the leftmost bits. It treats the number as an unsigned value.

   Example:
   ```java
   int a = -10;  // 11111111111111111111111111110110 in binary
   int result = a >>> 1;  // 01111111111111111111111111111011 in binary (2147483643 in decimal)
   System.out.println(result);  // Output: 2147483643
   ```

### Common Bit Manipulation Techniques

1. **Checking if a number is odd or even**:
   You can use the bitwise AND operator to check if the least significant bit (LSB) is 1 (odd) or 0 (even).
   
   Example:
   ```java
   int a = 5;
   boolean isOdd = (a & 1) == 1;  // If LSB is 1, the number is odd
   System.out.println(isOdd);  // Output: true (since 5 is odd)
   ```

2. **Swapping two numbers without a temporary variable**:
   You can swap two numbers using XOR.
   
   Example:
   ```java
   int a = 5, b = 3;
   a = a ^ b;  // a becomes 6 (0110)
   b = a ^ b;  // b becomes 5 (0101)
   a = a ^ b;  // a becomes 3 (0011)
   System.out.println("a: " + a + ", b: " + b);  // Output: a: 3, b: 5
   ```

3. **Flipping all the bits of a number**:
   Use the bitwise NOT (`~`) operator to flip all the bits.
   
   Example:
   ```java
   int a = 5;  // 0101 in binary
   int flipped = ~a;  // 1010 in binary (-6 in decimal)
   System.out.println(flipped);  // Output: -6
   ```

4. **Counting the number of set bits (1-bits)**:
   You can count the number of 1s in the binary representation of a number using a loop or Java's `Integer.bitCount()` method.
   
   Example:
   ```java
   int a = 5;  // Binary: 0101
   int count = Integer.bitCount(a);  // Number of 1s
   System.out.println(count);  // Output: 2
   ```

5. **Checking if the `n`-th bit is set**:
   You can check if the `n`-th bit (starting from 0) is set to `1` using the bitwise AND operator.

   Example:
   ```java
   int a = 5;  // Binary: 0101
   int n = 2;
   boolean isSet = (a & (1 << n)) != 0;  // Check if the 2nd bit is set
   System.out.println(isSet);  // Output: true (since the 2nd bit is 1)
   ```

6. **Setting the `n`-th bit**:
   You can set the `n`-th bit to `1` using the bitwise OR operator.

   Example:
   ```java
   int a = 5;  // Binary: 0101
   int n = 1;
   a = a | (1 << n);  // Set the 1st bit
   System.out.println(a);  // Output: 7 (Binary: 0111)
   ```

7. **Clearing the `n`-th bit**:
   You can clear the `n`-th bit (set it to `0`) using the bitwise AND with a mask that has the `n`-th bit as `0` and all other bits as `1`.

   Example:
   ```java
   int a = 5;  // Binary: 0101
   int n = 2;
   a = a & ~(1 << n);  // Clear the 2nd bit
   System.out.println(a);  // Output: 1 (Binary: 0001)
   ```

8. **Toggle the `n`-th bit**:
   You can toggle the `n`-th bit (flip it) using the bitwise XOR operator.

   Example:
   ```java
   int a = 5;  // Binary: 0101
   int n = 1;
   a = a ^ (1 << n);  // Toggle the 1st bit
   System.out.println(a);  // Output: 7 (Binary: 0111)
   ```

### Conclusion
Bit manipulation in Java is a highly efficient way to perform operations at the bit level. By mastering bitwise operators and common techniques like setting, clearing, and toggling bits, you can write optimized and high-performance code. This is particularly useful in areas like cryptography, compression, graphics programming, and low-level systems programming.