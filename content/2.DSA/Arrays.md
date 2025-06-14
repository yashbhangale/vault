---
title: DSA Arrays
date: 2025-01-10
---


why we need arrays

- array is collection of datatypes 
- Arrays are a type of static data structure because their size is predefined and unchangeable.
- Array indices start from 0.
- Arrays ==store elements of the same data type==, e.g., all integers, all strings, etc.

**Advantages in Java:**

- Simple to use for storing fixed-size collections of data.
- Provides a direct way to manage memory.

syntax
datatype[] variable_name = ==new== datatype[size];


here ==new== is a keyword used to create an object


ed : int[] numbers = new int[5];

int[] rnos = new int[5];
or
int[] rnos2 = {12,23,21,34,43};

![alt text](Pastedimage20241119120436.png)

![alt text](Pastedimage20241119120619.png)

here new is a keyword used to create an object

![alt text](Pastedimage20241119120751.png)

![alt text](Pastedimage20241119120813.png)

> In java their is no concept of pointers 

array objects are in heap

> all objects in java is stored in heap

heap object are not continous (memory are one by one allocated)

array objects  in java may not be continuous (it depends on jvm)


![alt text](Pastedimage20241119122520.png)


### passing through function

![alt text](Pastedimage20241119122826.png)
 
strings are immutable and arrays are mutable in java (here mutable means we can change object) 

### Multidimensional array

 ![alt text](Pastedimage20241119123237.png)

multidimensional arrays are array of arrays 


![alt text](Pastedimage20241119133407.png)

arr[] -----> [4,5,6]

![alt text](Pastedimage20241119133500.png)



individual size of an array can vary as well , bcoz  each array itself is a different object 


![alt text](Pastedimage20241119133949.png) 

input of multidimensional array

![alt text](Pastedimage20241119140517.png)


input and output of multidimensional array

```java
import java.util.Scanner;

public class MultiDimensionalArray {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Input dimensions of the array
        System.out.print("Enter number of rows: ");
        int rows = scanner.nextInt();
        System.out.print("Enter number of columns: ");
        int cols = scanner.nextInt();

        // Declare a 2D array
        int[][] array = new int[rows][cols];

        // Input elements into the array
        System.out.println("Enter the elements of the array:");
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                System.out.print("Element [" + i + "][" + j + "]: ");
                array[i][j] = scanner.nextInt();
            }
        }

        // Output the 2D array
        System.out.println("\nThe entered 2D array is:");
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                System.out.print(array[i][j] + " ");
            }
            System.out.println(); // Move to the next line for each row
        }

        scanner.close();
    }
}

```



![alt text](Pastedimage20241119142537.png)

### Array list

when we don't know how much size of the array we want

// syntax

```
ArrayList<Integer> list = new ArrayList<>();
```


An ArrayList in Java is a part of the `java.util` package and provides a resizable array implementation. Unlike arrays, the size of an ArrayList can grow or shrink dynamically.

- Automatically resizes when elements are added or removed.
- No need to define a fixed size at initialization.

![alt text](Pastedimage20241119143637.png)


internal working of arraylist

![alt text](Pastedimage20241119143937.png)


![alt text](Pastedimage20241119144049.png)



Q1 swap 2 index in an array

![alt text](Pastedimage20241119151147.png)


Q2. find max value of array

Q3. reverse of array


null