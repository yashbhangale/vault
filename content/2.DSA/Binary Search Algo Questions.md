---
title: DSA Binary Search Algo Questions
date: 2025-01-10
---



> [!NOTE]
> we use binary search in sorted arrays.
> if we get problem statement with sorted array try binary search first.

### Q.1 ceiling of a given number 

ceiling of no is smallest ele in arr greater ot == target
arr = [2,3,4,5,9,14,16,18], target = 14
if target = 14 then ceiling = 14
ceiling(arr,target=15) = 16 

![alt text](Pastedimage20241202175529.png)


![alt text](Pastedimage20241203070828.png)

---
### Q.2 Floor of a number

![alt text](WhatsAppImage2024-12-03at06.47.31_98d7e648.jpg)

### Code 

![alt text](Pastedimage20241203070809.png)

---
### Q.3 Find Smallest letter greater than target [ leetcode : 744 ]


1. Exact same approach for cieling of the number
2. ignore the target = what are looking for.
3. wrapping of later eg: arr = ['c','d','f','j'] , target = 'j' output = c we will use modulo (%) 
4. condition violeted : start = end + 1 ==> length of array = N   

![alt text](Pastedimage20241204144936.png)

---
### 4. Find First and Last Position of Element in Sorted Array

**Example 1:**
**Input:** nums = [5,7,7,8,8,10], target = 8
**Output:** [3,4]

**Example 2:**
**Input:** nums = [5,7,7,8,8,10], target = 6
**Output:** [-1,-1]

**Example 3:**
**Input:** nums = [], target = 0
**Output:** [-1,-1]

![alt text](Pastedimage20241204114845.png)

---

### 5. Find position of an element in a sorted array of infiniate numbers. (amazon interview question)

> try not to use array.length in infinite array 

https://youtu.be/W9QJ8HaRvJQ?list=PL9gnSGHSqcnr_DxHsP7AW9ftq0AtAyYqJ&t=6656

traverse through chunks
![alt text](Pastedimage20241215122615.png)

![alt text](Pastedimage20241215121554.png)


Doubling the size of chuck 

![alt text](Pastedimage20241215123745.png)

![alt text](Pastedimage20241215124827.png)

---
### 6. leetcode 852 peak index in a mountain Array

also known as biotonic arrray = {1,2,3,4,3,2,1}

![alt text](Pastedimage20241215174002.png)


find peak in mountain array
try to solve this question with linear search
#### but here i am using binary search to solve this

it is the sorted array it is sorted in 3 halfs (first asending 2nd decenting)

![alt text](Pastedimage20241216190242.png)

---
## 7. leetcode 1095 find in mountain array
### Search in mountain

![alt text](Pastedimage20241216190713.png)

code for this will try later

---
## 8. Search in a Rotated Sorted Array (LeetCode 33)

distinct value (no dublicates)

2 approaches 

#### case 1:
![alt text](Pastedimage20241216191656.png)

![alt text](Pastedimage20241216191704.png)

![alt text](Pastedimage20241216191913.png)

> remember pivot is the largest number 


1. find pivot 
2. search in first half (simple binary search) [o,pivot]
3. otherwise, search in second half [pivot + 1, end ]

![alt text](Pastedimage20241216192508.png)

#### case 2:

if mid ele  < (mid - 1) ele , so my ans is (mid - 1)

#### case 3: 

start ele > mid - element

![alt text](Pastedimage20241216193255.png)

![alt text](Pastedimage20241216193417.png)



#### case 4

![alt text](Pastedimage20241216194556.png) 
![alt text](Pastedimage20241216201207.png)

#### Code : (duplicate value rotation code is also included)
![alt text](Pastedimage20241217225135.png)
![alt text](Pastedimage20241217225200.png)
![alt text](Pastedimage20241217225216.png)
![alt text](Pastedimage20241217225237.png)

## Q.9 rotation count

![alt text](Pastedimage20241217232449.png)

ans = pivot +1

code : https://github.com/kunal-kushwaha/DSA-Bootcamp-Java/blob/main/lectures/10-binary%20search/code/src/com/kunal/RotationCount.java
