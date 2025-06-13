---
title: Mathematics for Dsa
date: 2025-02-22
---

## 1. HCF & GCD of a number

```java
import java.util.Scanner;

public class Solution {
	public static void main(String[] args) {
		Scanner scanner = new Scanner(System.in);
		System.out.print("");
		int a = scanner.nextInt();
		System.out.print("");
		int b = scanner.nextInt();
		
		while (a != b) {
			if(a==0)
			{
				System.out.print(b);
				break;
			}
			if(b == 0)
			{
				System.out.println(a);
			}
			if ( a > b ) {
				a = a - b;
			} else {
				b = b - a; 
			}
		}
		System.out.printla(a);
		scanner.close();
	}
}
```

---

## 2. Write a program to find the factorial of a number.

```java
import java.util.Scanner;

public class FactorialIterative {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Input number
        System.out.print("Enter a number: ");
        int num = scanner.nextInt();

        // Calculate factorial
        long factorial = 1;
        for (int i = 1; i <= num; i++) {
            factorial *= i; // Multiply each number
        }

        // Display result
        System.out.println("The factorial of " + num + " is: " + factorial);

        scanner.close();
    }
}
```

---

