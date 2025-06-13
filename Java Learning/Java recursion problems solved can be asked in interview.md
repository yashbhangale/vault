---
title: Java recursion problems solved can be asked in interview
date: 2024-09-28
categories:
  - java
  - placement
---
## 1. Tower of Hanoi 

![](https://i.imgur.com/8SAx5Qz.png)

![](https://i.imgur.com/VQar2NA.png)

> [!Rules:]
> 1. Only one disk transferred in 1 step
> 2. smaller disks are always kept on top of larger disks 

```java
public class Recursion { // Define a public class named 'Recursion'.
  
  // A static method to solve the Tower of Hanoi problem
  public static void TowerOfHanoi(int n, String src, String helper, String dest) {
    
    // Base condition: If there's only one disk, move it directly from source to destination.
    if (n == 1) {
      // Print out the move of the single disk from source to destination
      System.out.println("transfer disk " + n + " from " + src + " to " + dest);
      return; // End the current recursive call when only one disk is left
    }

    // Recursive call: Move (n-1) disks from source to helper using destination as an auxiliary
    TowerOfHanoi(n - 1, src, dest, helper);

    // Move the nth disk (largest) from source to destination
    System.out.println("transfer disk " + n + " from " + src + " to " + dest);

    // Recursive call: Move (n-1) disks from helper to destination using source as an auxiliary
    TowerOfHanoi(n - 1, helper, src, dest);
  }
  
  // Main method: the entry point of the program
  public static void main(String[] args) {
    int n = 3; // Number of disks
    // Call the TowerOfHanoi method to solve for 3 disks, with source as "Source", helper as "Helper", and destination as "Destination".
    TowerOfHanoi(n, " Source ", " Helper ", " Destination ");
  }
}
```

>  Time complexity is = $O(2^n)$

---
## 2. Reverse a string using Recurssion

abcd
dcba


![](https://i.imgur.com/Lf9KaEO.png)


```java
public class Recursion{
  public  static void ReverseString(int index, String str) {
    //base condition
    if(index == 0 ){
      System.out.print(str.charAt(index));
      return;
    }
    
    System.out.print(str.charAt(index));
    ReverseString( index -1,str);
  }
  
  public static void main (String[] args) {
    String str = "abcdefg";
    ReverseString( str.length()-1 , str);
  }
}
```

> Time complexity O(n)

---
## 3. find the last occurrence of the element in the string.

>> reference video with time stamp =[[https://youtu.be/u-[HgzgYe8KA]()?list=PLfqMhTWNBTe3LtFWcvwpqTkUSlB32kJop&t=1929]]

![](https://i.imgur.com/riquZZU.png)

```java
public class Recursion {
  public static int first = -1;
  public static int last = -1;
  
  public static void findOccurrence(int index, String str, char element) {
    // Base condition: If index reaches the length of the string, print first and last occurrence
    if (index == str.length()) {
      System.out.println("First occurrence: " + first);
      System.out.println("Last occurrence: " + last);
      return;
    }

    // Check if the current character matches the element
    char currChar = str.charAt(index);
    if (currChar == element) {
      if (first == -1) {
        // Set the first occurrence if it's the first time encountering the element
        first = index;
      } else {
        // Update the last occurrence
        last = index;
      }
    }

    // Recursive call with index incremented to move forward
    findOccurrence(index + 1, str, element);
  }

  public static void main(String[] args) {
    String str = "abcdefga";  // Input string
    findOccurrence(0, str, 'a');  // Start the search at index 0
  }
}


```

> time complexity: O(n)

---
## 4. check if an array is sorted (strictly sorted)


![](https://i.imgur.com/kUDx16x.png)


```java
public class Recursion2 {
  public static boolean isSorted(int arr[], int idx) {
    // Print the current index and the elements being compared
    System.out.println("Checking if arr[" + idx + "] < arr[" + (idx + 1) + "]");

    // Base case: if we're at the last index, the array is sorted
    if (idx == arr.length - 1) {
      System.out.println("Reached the last element, array is sorted.");
      return true;
    }

    // Recursive case: if the current element is less than the next, keep checking
    if (arr[idx] < arr[idx + 1]) {
      System.out.println("arr[" + idx + "] = " + arr[idx] + " is less than arr[" + (idx + 1) + "] = " + arr[idx + 1] + ", checking further.");
      return isSorted(arr, idx + 1);
    } else {
      System.out.println("arr[" + idx + "] = " + arr[idx] + " is NOT less than arr[" + (idx + 1) + "] = " + arr[idx + 1] + ", array is not sorted.");
      return false;
    }
  }

  public static void main(String args[]) {
    int arr[] = {1, 3, 5};  // You can modify this array to test different cases
    System.out.println("Is the array sorted? " + isSorted(arr, 0));
  }
}
```

>  time complexity = O(n)

![](https://i.imgur.com/YsRLkfz.png)

---
## 5.  Move all 'X' to the end of string ("acbcxxd")

Given a string like `"axbcxxd"`, we want to move all the `'x'` characters to the end. The result for this example would be `"abcxdxx"`

- If the current character is **not 'x'**, keep it where it is.
- If the current character **is 'x'**, move it to the end.

Recursion involves solving a problem by breaking it into smaller sub-problems. Here's how we can think about this:

1. If the string is empty, return an empty string (base case).
2. For a string that is not empty:
    - If the first character is **not 'x'**, keep it at the front and call the function recursively on the rest of the string.
    - If the first character **is 'x'**, move it to the end and call the function recursively on the rest of the string.

```java
public class MoveXToEnd {

  // Recursive function to move all 'x' to the end of the string
  public static String moveXToEnd(String str) {
    // Base case: if the string is empty, return the empty string
    if (str.length() == 0) {
      return "";
    }

    // Get the first character of the string
    char firstChar = str.charAt(0);

    // Recursively call moveXToEnd on the rest of the string
    String restOfString = moveXToEnd(str.substring(1));

    // If the first character is 'x', append it to the result of the recursion
    if (firstChar == 'x') {
      return restOfString + firstChar; // Move 'x' to the end
    } else {
      return firstChar + restOfString; // Keep the first character in front
    }
  }

  // Main method to test the function
  public static void main(String[] args) {
    String input = "axbcxxd";
    String result = moveXToEnd(input);
    System.out.println("Result: " + result);
  }
}

```

>  time complexity O(n)

## 6.Remove Duplicates of strings 
 

![](https://i.imgur.com/98boTPH.jpeg)


```java
public class Recursion2 {
  public static boolean[] map = new boolean[26];
  
  public static void removeDuplicates(String str, int idx, String newString){
    if(idx == str.length()) {
      System.out.println(newString);
      return;
    }
    char currChar= str.charAt(idx);
    if(map[currChar - 'a']) {
       removeDuplicates(str, idx+1, newString);
       
    } else {
      newString += currChar;
      map[currChar - 'a'] = true;
      removeDuplicates (str,idx+1, newString);
    }
  }
  
  public static void main (String args[]) {
    String str = "abbcddddaaa";
    removeDuplicates(str,0,"");
  }
}
```

---
## 7. print all the sub-sequences of a string "abc"

![](https://i.imgur.com/caZ2lxN.png)
![](https://i.imgur.com/eNwoPlV.png)
 


```java
public class Recursion2 {
  public static void subsequence(String str, int idx, String newString){
    
    if(idx == str.length())  {
      System.err.println(newString);
      return;
    }  
    char currcharr = str.charAt(idx);
    
    subsequence(str, idx+1, newString + currcharr);
    
    subsequence(str,idx+1,newString);
  
  }
  
  public static void main (String args[]) {
    String str = "abc";
    subsequence(str,0,"");
  }
}
```

>  time complexity = 2^n

---
## 8. Print keypad combnation

![](https://i.imgur.com/V5RJ7U9.jpeg)



```java
import java.util.HashSet;

public class Recursion2 {
  public static String[] keypad =  {".","abc","def","ghi","jkl","mno","pqrs","tu","vwx","yz"};
  
  public static void printComb(String str, int idx, String combination) {
    if(idx == str.length()) {
      System.out.println(combination);
      return;
    }
    char currChar = str.charAt(idx);
    String mapping = keypad[currChar - '0'];
    
    for(int i =0; i<mapping.length(); i++){
      printComb(str, idx+1,combination+mapping.charAt(i));
    }
  }
  
  public static void main (String args[]){
    String str = "41";
    printComb(str,0,"");
  }
  
}
```