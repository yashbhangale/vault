---
title: DSA Exception Handling
date: 2025-01-03
---

- **Exception**: An event that disrupts the normal flow of a program (e.g., divide by zero, accessing an invalid array index, etc.).
- **Exception Handling**: Process of handling runtime errors gracefully without crashing the program.

1. **try-catch Block**
	- Code that may throw an exception is written inside the `try` block.
	- Exceptions are caught and handled in the `catch` block.

```java
try {
	//Code that may throw an exception
} catch (ExceptionType e){
	//Handling code
}
```

2. **finally Block**
	- Used for cleanup operations, e.g., closing files or database connections.
	- Always executed, whether an exception is thrown or not.

```java
try {
 // code that may throw exceoption
} catch (ExceptionType e) {
 // Handling code
} finally {
 // cleamup code
}
```

3. throw vs throws 
	- **throw**: Ek specific exception ko manually throw karte hain.
	- **throws**: Method ke declaration mein batate hain ki ye method kaunse exception throw kar sakta hai.

```java
void myMethod() throws IOException { 
	throw new IOException("File not found"); 
}
```

## Types of Exceptions

1.  **Checked Exceptions**
    - Compile-time pe catch karna padta hai, warna code chalega nahi.
    - Example: `IOException`, `SQLException`.

2. **Unchecked Exceptions**
    - Runtime pe hoti hain, jaise `NullPointerException`, `ArithmeticException`.

```java
public class ExceptionExample {
    public static void main(String[] args) {
        try {
            int[] arr = {1, 2, 3};
            System.out.println(arr[5]); // Error: ArrayIndexOutOfBoundsException
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Invalid index accessed!");
        }
    }
}
```

```java
public class FinallyExample {
    public static void main(String[] args) {
        try {
            int data = 10 / 0;
        } catch (ArithmeticException e) {
            System.out.println("Error: " + e.getMessage());
        } finally {
            System.out.println("Cleanup: Closing resources");
        }
    }
}
```

throw and throws Example

```java
import java.io.IOException;

public class ThrowExample {
    static void checkFile() throws IOException {
        throw new IOException("File not found!");
    }

    public static void main(String[] args) {
        try {
            checkFile();
        } catch (IOException e) {
            System.out.println("Caught Exception: " + e.getMessage());
        }
    }
}
```

