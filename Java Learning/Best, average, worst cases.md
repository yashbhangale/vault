---
title: Best average and worstcases time complexity
date: 2025-01-10
---



---

### **1. Best Case**
- **Definition**: Jab algorithm apne kaam ko sabse efficient tareeke se kare, i.e., ==minimum time lage.==
- **Example**: 
  - ==**Linear Search**: Agar element list ke pehle hi index pe mil jaye==.
    ```java
    int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) return i; // Found at first position
        }
        return -1;
    }
    ```
    - **Best Case Complexity**: `O(1)` (First element match ho gaya).

---

### **2. Average Case**
- **Definition**: Jab algorithm ka performance **typical input** ke liye analyze kare.
- **Example**:
  - **Linear Search**: Jab target element random position pe ho.
    - Agar list ke har position pe element hone ke equal chances hain, toh on average tumhe array ka aadha iterate karna padega.
    - **Average Case Complexity**: `O(n/2)` ≈ `O(n)`.

---

### **3. Worst Case**
- **Definition**: Jab algorithm apne kaam ko sabse inefficient tareeke se kare, i.e., maximum time lage.
- **Example**: 
  - **Linear Search**: Jab element list ke last index pe ho ya na ho.
    ```java
    int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) return i; // Last element match or no match
        }
        return -1;
    }
    ```
    - **Worst Case Complexity**: `O(n)` (Pura array traverse karna padega).

---

### **Case-wise Complexity for Different Algorithms**

| **Algorithm**        | **Best Case** | **Average Case** | **Worst Case**    |
|-----------------------|---------------|-------------------|-------------------|
| **Linear Search**     | `O(1)`       | `O(n)`           | `O(n)`           |
| **Binary Search**     | `O(1)`       | `O(log n)`       | `O(log n)`       |
| **Bubble Sort**       | `O(n)`       | `O(n²)`          | `O(n²)`          |
| **Quick Sort**        | `O(n log n)` | `O(n log n)`     | `O(n²)`          |
| **Merge Sort**        | `O(n log n)` | `O(n log n)`     | `O(n log n)`     |
| **Hash Table Search** | `O(1)`       | `O(1)`           | `O(n)`           |

---

### **Example: Binary Search**

- **Best Case**: Jab element middle pe hi mil jaye.
  - Complexity: `O(1)`.
- **Average Case**: Jab element mid ke around somewhere ho.
  - Complexity: `O(log n)`.
- **Worst Case**: Jab element exist na kare ya end tak dhoondhna pade.
  - Complexity: `O(log n)`.

```java
int binarySearch(int[] arr, int target) {
    int low = 0, high = arr.length - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) return mid; // Best Case
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1; // Worst Case (not found)
}
```

---

### **Key Insights**

1. **Best Case**:
   - Ideal situation.
   - Rarely defines real-world performance.
2. **Average Case**:
   - Most realistic measure of an algorithm’s efficiency.
3. **Worst Case**:
   - Safest measure.
   - Defines the upper bound on runtime.
