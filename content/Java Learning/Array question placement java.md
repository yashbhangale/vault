---
title: Array question placement java
date: 2024-09-29
categories:
  - placement
  - java
  - arrray
---
## 1.  Compare Two Arrays in Java

While comparing two arrays we can not use “ == ” operator as it will compare the addresses of the memory block to which both the arrays are pointing. 

A simple way is to run a loop and compare elements one by one. Java provides a direct method _Arrays.equals()_ to compare two arrays. Actually, there is a list of equals() methods in the Arrays class for different primitive types (int, char, ..etc) and one for Object type (which is the base of all classes in Java).

```java
// Java Program to Check If Two Arrays Are Equal
// Using equals() method of Arrays class

// Importing required classes
import java.util.Arrays;

// Main class
class GFG {

	// Main driver method
	public static void main(String[] args)
	{

		// Declaring integer arrays
		int arr1[] = { 1, 2, 3 };
		int arr2[] = { 1, 2, 3 };

		// Checking if above two arrays are equal
		// using equals() method
		if (Arrays.equals(arr1, arr2))

			// Print statement if arrays are equal
			System.out.println("Same");
		else

			// Print statement if arrays are equal
			System.out.println("Not same");
	}
}
```