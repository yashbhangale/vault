---
title: DSA Linear Search Algorithm
date: 2025-01-10
---


https://youtu.be/_HRA37X8N_Q?list=PL9gnSGHSqcnr_DxHsP7AW9ftq0AtAyYqJ


A simple algorithm that checks each element in the array until the target element is found or the end of the array is reached.

![alt text](Pastedimage20241121133906.png)

> start searching from the first element till the element which we are finding 

we use for loop in linear searching

time complexity :

- Best Case: O(1)    // constant
- Worst Case: O(n)  // here n is the size of the array

![alt text](Pastedimage20241121134313.png)

![alt text](Pastedimage20241121134405.png)
 linear time complexity (above image)


![alt text](Pastedimage20241121134446.png)
best case time complexity (above image)


O(n) (upper bound time complexity) means it will never go worst then linear, it is always better than linear


space complexity means are you taking extra space (extra space taken)



```java
public class Search { // Class name should start with an uppercase letter for convention

    public static void main(String[] args) {
        // Define an array of integers to search from
        int[] nums = {1, 2, 3, 4, 2, 1, 3, 5, 6};

        // The target value we want to find in the array
        int target = 5;

        // Call the linearSearch method to search for the target in the array
        int ans = linearSearch(nums, target);

        // Print the result: If found, it will print the index; otherwise, -1
        System.out.println(ans);
    }

    /**
     * Perform a linear search in the array.
     * @param arr The array to search in
     * @param target The value to search for
     * @return The index of the target if found, otherwise -1
     */
    static int linearSearch(int[] arr, int target) {
        // If the array is empty, return -1 as there is nothing to search
        if (arr.length == 0) {
            return -1;
        }

        // Iterate through each element in the array
        for (int index = 0; index < arr.length; index++) {
            // Get the current element at the index
            int element = arr[index];

            // Check if the current element matches the target
            if (element == target) {
                return index; // Return the index of the target if found
            }
        }

        // If the loop completes and the target is not found, return -1
        return -1;
    }
}

```


![alt text](Pastedimage20241121140431.png)
![alt text](Pastedimage20241121140448.png)



## Q. Is a char present in the string 

![alt text](Pastedimage20241122234332.png)

## Q. Search in Range


![alt text](Pastedimage20241121141646.png)


![alt text](Pastedimage20241121142520.png)

## Q. find minimum element in the ARRAY

![alt text](Pastedimage20241121142733.png)

![alt text](Pastedimage20241121142851.png)

![alt text](Pastedimage20241121142913.png)


## Q. Searching in 2d arrays
![alt text](Pastedimage20241124002356.png)

## Q. Search and print maximum value in 2D array


![alt text](Pastedimage20241124003045.png)

 ![alt text](Pastedimage20241121153028.png)

![alt text](Pastedimage20241125185619.png)

https://youtu.be/vwa9vgYz5ZE?t=35

![alt text](Pastedimage20241125190847.png)


![alt text](Pastedimage20241121153519.png)


![alt text](Pastedimage20241121154417.png)



![alt text](Pastedimage20241125193442.png)
