---
title: impt interviews questions
tags: [dsa]
---
# [[Hash Map]]

# two sum  [hash tables]
video reference : https://www.youtube.com/watch?v=7jDS9KQEDbI

![[Pasted image 20250301000328.png]]

- whenever there is searching then there is sort 
- try to sort ele first in searching (for bruteforce method)


```java
class Solution {

	public int[] twoSum(int[] nums, int target) {

		Map<Integer, Integer> map = new HashMap<>();
		for (int i = 0; i < nums.length; i++ ){

			int complement = target - nums[i];
			// Check if complement exists in `map`
			if(map.containsKey(complement)) {
				return new int[]{map.get(complement), i};
			}
			// Store the current number in `map`
			map.put(nums[i], i);
		}
		throw new IllegalArgumentException("No 2 sum found ");
	}
}
```

```python
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        num_map = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_map:
                return [num_map[complement], i]
            num_map[num] = i
        return[]
```

```python
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        n = len(nums)
        for i in range(n):
            for j in range(i+1, n):
                if nums[i] + nums[j] == target:
                    return[i,j]
        return []
```

![[Pasted image 20250302140941.png]]

---

# Contain Duplicates: [[Hash SET]]
Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.



![[Pasted image 20250302152620.png]]


```java
class Solution {

	public boolean containsDuplicate(int[] nums) {
	// Create the hashset to store integers
		Set<Integer> intSet = new HashSet<>();
		// Iterate over each element
		for (int num : nums) {
			// Check if num is present in hashset
			if (intSet.contains(num))
				return true;
			// Add the num in hashset
			intSet.add(num);
		}
		return false;
		}
	}
```

```python
class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False
```

```python
class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        nums.sort()
        for i in range (len(nums) - 1):
            if nums[i] == nums[i+1]:
                return True
        return False
```
---

# Valid Anagram:
leetcode 242:

with HashMap

```python
class Solution:
	def isAnagram(self, s: str, t: str) -> bool:
		if len(s) != len(t):
			return False
		countS,countT = {}, {}
		for i in range(len(s)):
			countS[s[i]] = 1 + countS.get(s[i], 0)
			countT[t[i]] = 1 + countT.get(t[i], 0)
		for c in countS:
			if countS[c] != countT.get(c, 0):
				return False
		return True
```

with sorting:

```python
class Solution: 
	def isAnagram(self, s: str, t: str) -> bool: 
		sorted_s = sorted(s) 
		sorted_t = sorted(t) 
		return sorted_s == sorted_t
```


---

# Intersection of two arrays  leetcode 349

**Example 1:**

**Input:** nums1 = [1,2,2,1], nums2 = [2,2]
**Output:** [2]

**Example 2:**

**Input:** nums1 = [4,9,5], nums2 = [9,4,9,8,4]
**Output:** [9,4]
**Explanation:** [4,9] is also accepted.

```python
class Solution:
def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
	seen = set(nums1)
	res = []

	for n in nums2:
		if n in seen:
			res.append(n)
			seen.remove(n)
	return res
```

---

# Majority Element - leetcode 169
Given an array `nums` of size `n`, return _the majority element_.

The majority element is the element that appears more than `⌊n / 2⌋` times. You may assume that the majority element always exists in the array.

**Example 1:**

**Input:** nums = [3,2,3]
**Output:** 3

**Example 2:**

**Input:** nums = [2,2,1,1,1,2,2]
**Output:** 2

```python
class solution;
	def majorityElement(self, nums: List[int]) -> int:
		count = {}
		res, maxCount = 0,0

		for n in nums:
			count[n] = 1 + count.get(n,0)
				res = n if count[n] > maxCount else res
				maxCount = max(count[n], maxCount)
		return res
```

time complexity = o(n)
space complexity = o(n)


solution no. 2
https://youtu.be/7pnhv842keE?t=270

```python
class solution
	def majorityElement(self, nums: List[int]) -> int:
		res, count = 0,0
		for n in nums:
			if count == 0:
				res = n
			count += (1 if n == res else -1)
		return res
```


