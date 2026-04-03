---
title: Python_interview
tags: [python-learning]
---
# 🐍 Complete Python Interview Preparation Guide
**Dost, ye file padh kar tu complete Python interview ready ho jaega! Sab kuch ek jagah hai.**

---

## 📚 Table of Contents
1. [Core Python Questions](#core-python-questions)
2. [Data Structures & Built-ins](#data-structures--built-ins)
3. [Intermediate Python](#intermediate-python)
4. [Object-Oriented Programming (OOP)](#object-oriented-programming-oop)
5. [Important Libraries](#important-libraries)
6. [Problem Solving (DSA)](#problem-solving-dsa)
7. [Common Interview Patterns](#common-interview-patterns)
8. [Quick Reference](#quick-reference)

---

## Core Python Questions

### Q1: What is Python? What are its key features?
**Answer:**
Python is a high-level, interpreted programming language. Key features:
- **Simple syntax** - Easy to read and write
- **Interpreted** - No compilation needed, runs directly
- **Dynamic typing** - No need to declare variable types
- **Cross-platform** - Works on Windows, Mac, Linux
- **Large standard library** - Many built-in modules
- **Open source** - Free to use and modify

**Simple samjho:** Python ek aisi language hai jo bilkul English jaisi hai, aur bahut easy hai learn karne ke liye!

### Q2: What are the different data types in Python?
**Answer:**
```python
# Numbers
age = 25          # int (integer)
height = 5.9      # float (decimal)
complex_num = 3+4j # complex

# Text
name = "John"     # str (string)

# Boolean
is_student = True # bool (True/False)

# Collections
fruits = ["apple", "banana"]     # list (mutable)
coordinates = (10, 20)           # tuple (immutable)
person = {"name": "John", "age": 25} # dict (key-value pairs)
unique_nums = {1, 2, 3, 3}      # set (unique elements only)
```

**Simple samjho:** Python mein different types ke boxes hote hain different cheezein store karne ke liye!

### Q3: What's the difference between list and tuple?
**Answer:**
```python
# List - Mutable (changeable)
fruits = ["apple", "banana"]
fruits.append("orange")  # Can add
fruits[0] = "grape"      # Can modify
fruits.remove("banana")  # Can remove

# Tuple - Immutable (not changeable)
coordinates = (10, 20)
# coordinates[0] = 15  # ERROR! Cannot modify
# coordinates.append(30)  # ERROR! Cannot add
```

**Key Differences:**
- **List** uses `[]`, **Tuple** uses `()`
- **List** is mutable, **Tuple** is immutable
- **List** has more methods (append, remove, etc.)
- **Tuple** is faster and uses less memory
- **Tuple** can be used as dictionary keys, **List** cannot

**Simple samjho:** List jaise shopping list - add/remove kar sakte ho. Tuple jaise birth date - fix hai, change nahi kar sakte!

### Q4: What are *args and **kwargs?
**Answer:**
```python
def my_function(*args, **kwargs):
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)

# Usage
my_function(1, 2, 3, name="John", age=25)
# Output:
# Positional arguments: (1, 2, 3)
# Keyword arguments: {'name': 'John', 'age': 25}
```

**Explanation:**
- `*args` - Accepts any number of positional arguments
- `**kwargs` - Accepts any number of keyword arguments
- `args` becomes a tuple
- `kwargs` becomes a dictionary

**Simple samjho:** *args matlab "kitne bhi numbers de do", **kwargs matlab "kitne bhi naam-value pairs de do"!

### Q5: What's the difference between == and is?
**Answer:**
```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True - same values
print(a is b)  # False - different objects
print(a is c)  # True - same object

# Memory addresses
print(id(a))  # 140123456789
print(id(b))  # 140123456790 (different)
print(id(c))  # 140123456789 (same as a)
```

**Key Differences:**
- `==` compares **values**
- `is` compares **object identity** (memory location)
- `is` is faster than `==`
- Use `is` for None, True, False comparisons

**Simple samjho:** == matlab "value same hai?", is matlab "same box hai?"

### Q6: How do you handle exceptions in Python?
**Answer:**
```python
try:
    result = 10 / 0  # This will cause an error
    print(result)
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"Some other error: {e}")
else:
    print("No errors occurred")
finally:
    print("This always runs")
```

**Exception Types:**
- `try` - Code that might cause error
- `except` - Handle specific errors
- `else` - Runs if no error
- `finally` - Always runs
- `raise` - Create your own errors

**Simple samjho:** Try-except matlab "try karo, agar error aaye to handle kar lo"!

### Q7: What are lambda functions?
**Answer:**
```python
# Regular function
def square(x):
    return x * x

# Lambda function (same thing, shorter)
square_lambda = lambda x: x * x

# Usage
print(square(5))        # 25
print(square_lambda(5)) # 25

# Common use with map, filter
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))  # [1, 4, 9, 16, 25]
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]
```

**When to use:**
- Short, simple functions
- One-time use functions
- With map, filter, reduce
- Don't use for complex logic

**Simple samjho:** Lambda matlab "chhota function" - ek line mein function bana do!

---

## Data Structures & Built-ins

### Q8: How do you remove duplicates from a list?
**Answer:**
```python
# Method 1: Using set (loses order)
original = [1, 2, 2, 3, 4, 4, 5]
unique = list(set(original))
print(unique)  # [1, 2, 3, 4, 5] (order may vary)

# Method 2: Preserving order
unique_ordered = []
for item in original:
    if item not in unique_ordered:
        unique_ordered.append(item)
print(unique_ordered)  # [1, 2, 3, 4, 5] (preserves order)

# Method 3: Using dict.fromkeys() (Python 3.7+)
unique_ordered = list(dict.fromkeys(original))
print(unique_ordered)  # [1, 2, 3, 4, 5] (preserves order)
```

**Simple samjho:** Set use karo duplicate remove karne ke liye, lekin order maintain karna hai to loop use karo!

### Q9: How do you merge two dictionaries?
**Answer:**
```python
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}

# Method 1: Using update() (modifies first dict)
dict1.update(dict2)
print(dict1)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# Method 2: Using ** unpacking (Python 3.5+)
merged = {**dict1, **dict2}
print(merged)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# Method 3: Using | operator (Python 3.9+)
merged = dict1 | dict2
print(merged)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}
```

**Simple samjho:** Dono dictionaries ko combine karna - update() use karo ya ** unpacking use karo!

### Q10: What's the difference between append() and extend()?
**Answer:**
```python
list1 = [1, 2, 3]
list2 = [1, 2, 3]

# append() - adds single element
list1.append([4, 5])
print(list1)  # [1, 2, 3, [4, 5]] - list added as single element

# extend() - adds all elements from iterable
list2.extend([4, 5])
print(list2)  # [1, 2, 3, 4, 5] - individual elements added
```

**Key Differences:**
- `append()` adds **one element** to the end
- `extend()` adds **all elements** from an iterable
- `append([1,2])` adds the list as one item
- `extend([1,2])` adds 1 and 2 as separate items

**Simple samjho:** append() matlab "ek box add karo", extend() matlab "box ke andar ki cheezein add karo"!

### Q11: How do you sort a dictionary by value?
**Answer:**
```python
scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 96}

# Method 1: Using sorted() with key parameter
sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1]))
print(sorted_scores)  # {'Charlie': 78, 'Alice': 85, 'Bob': 92, 'Diana': 96}

# Method 2: Using operator.itemgetter
from operator import itemgetter
sorted_scores = dict(sorted(scores.items(), key=itemgetter(1)))
print(sorted_scores)  # {'Charlie': 78, 'Alice': 85, 'Bob': 92, 'Diana': 96}

# Method 3: Sort in descending order
sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
print(sorted_scores)  # {'Diana': 96, 'Bob': 92, 'Alice': 85, 'Charlie': 78}
```

**Simple samjho:** Dictionary ko sort karna - sorted() use karo aur key parameter mein lambda function use karo!

### Q12: What are list comprehensions?
**Answer:**
```python
# Regular way
squares = []
for x in range(5):
    squares.append(x**2)
print(squares)  # [0, 1, 4, 9, 16]

# List comprehension (shorter way)
squares = [x**2 for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]

# With condition
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(even_squares)  # [0, 4, 16, 36, 64]

# Nested list comprehension
matrix = [[1, 2, 3], [4, 5, 6]]
flattened = [num for row in matrix for num in row]
print(flattened)  # [1, 2, 3, 4, 5, 6]
```

**Simple samjho:** List comprehension matlab "list banane ka short way" - ek line mein list bana do!

---

## Intermediate Python

### Q13: What are generators in Python?
**Answer:**
```python
# Generator function
def countdown(n):
    while n > 0:
        yield n  # yield instead of return
        n -= 1

# Usage
for i in countdown(5):
    print(i)  # 5, 4, 3, 2, 1

# Generator expression
squares = (x**2 for x in range(5))
print(list(squares))  # [0, 1, 4, 9, 16]

# Memory efficient
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Only generates numbers as needed
for num in fibonacci(10):
    print(num)
```

**Key Points:**
- Use `yield` instead of `return`
- Memory efficient (lazy evaluation)
- Can only iterate once
- Good for large datasets

**Simple samjho:** Generator matlab "on-demand data" - jab chahiye tab generate karo, pehle se store nahi karo!

### Q14: What are decorators?
**Answer:**
```python
# Simple decorator
def my_decorator(func):
    def wrapper():
        print("Something before function")
        func()
        print("Something after function")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Output:
# Something before function
# Hello!
# Something after function

# Decorator with arguments
def timing_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function took {end - start} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(1)
    return "Done"

result = slow_function()  # Function took 1.0 seconds
```

**Simple samjho:** Decorator matlab "function ko wrap karna" - extra functionality add karna!

### Q15: What's the difference between shallow copy and deep copy?
**Answer:**
```python
import copy

# Original list with nested list
original = [1, 2, [3, 4]]

# Shallow copy
shallow = copy.copy(original)
shallow[2][0] = 999
print(original)   # [1, 2, [999, 4]] - nested list changed!
print(shallow)    # [1, 2, [999, 4]]

# Deep copy
original = [1, 2, [3, 4]]
deep = copy.deepcopy(original)
deep[2][0] = 999
print(original)   # [1, 2, [3, 4]] - original unchanged
print(deep)       # [1, 2, [999, 4]]
```

**Key Differences:**
- **Shallow copy** - Copies only first level, nested objects are shared
- **Deep copy** - Copies all levels, completely independent
- **Shallow copy** is faster
- **Deep copy** uses more memory

**Simple samjho:** Shallow copy matlab "surface level copy", deep copy matlab "complete copy"!

### Q16: How do you handle file operations in Python?
**Answer:**
```python
# Reading a file
with open("data.txt", "r") as file:
    content = file.read()
    print(content)

# Writing to a file
with open("output.txt", "w") as file:
    file.write("Hello, World!")

# Appending to a file
with open("log.txt", "a") as file:
    file.write("New log entry\n")

# Reading line by line (memory efficient)
with open("large_file.txt", "r") as file:
    for line in file:
        print(line.strip())

# JSON file operations
import json

# Writing JSON
data = {"name": "John", "age": 30}
with open("data.json", "w") as file:
    json.dump(data, file)

# Reading JSON
with open("data.json", "r") as file:
    loaded_data = json.load(file)
    print(loaded_data)
```

**Simple samjho:** File operations matlab "file se data lena aur file mein data dalna" - always use `with` statement!

---

## Object-Oriented Programming (OOP)

### Q17: What are the four pillars of OOP?
**Answer:**
```python
# 1. Encapsulation - Data hiding
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Private attribute
    
    def get_balance(self):
        return self.__balance
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

# 2. Inheritance - Reusing code
class Animal:
    def speak(self):
        print("Some sound")

class Dog(Animal):
    def speak(self):
        print("Woof!")

# 3. Polymorphism - Same interface, different behavior
def make_sound(animal):
    animal.speak()  # Works with any animal

dog = Dog()
make_sound(dog)  # Woof!

# 4. Abstraction - Hiding complexity
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def area(self):
        return 3.14 * self.radius ** 2
```

**Simple samjho:** OOP ke 4 pillars - Encapsulation (hide data), Inheritance (reuse code), Polymorphism (same name, different work), Abstraction (hide complexity)!

### Q18: What's the difference between class method and static method?
**Answer:**
```python
class MyClass:
    class_var = "I'm a class variable"
    
    def __init__(self, value):
        self.instance_var = value
    
    @classmethod
    def class_method(cls):
        print(f"Class method called on {cls}")
        print(f"Class variable: {cls.class_var}")
        return cls("from class method")
    
    @staticmethod
    def static_method():
        print("Static method called")
        return "No access to class or instance"
    
    def instance_method(self):
        print(f"Instance method called on {self}")
        print(f"Instance variable: {self.instance_var}")

# Usage
obj = MyClass("test")

# Class method - receives class as first argument
new_obj = MyClass.class_method()

# Static method - no access to class or instance
result = MyClass.static_method()

# Instance method - receives instance as first argument
obj.instance_method()
```

**Key Differences:**
- **Class method** - Receives class as first argument, can access class variables
- **Static method** - No access to class or instance, just a function in class namespace
- **Instance method** - Receives instance as first argument, can access instance variables

**Simple samjho:** Class method matlab "class ke saath kaam", static method matlab "class mein function", instance method matlab "object ke saath kaam"!

### Q19: What are magic methods (dunder methods)?
**Answer:**
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"Person: {self.name}, Age: {self.age}"
    
    def __repr__(self):
        return f"Person('{self.name}', {self.age})"
    
    def __len__(self):
        return len(self.name)
    
    def __add__(self, other):
        return Person(f"{self.name} & {other.name}", 
                     (self.age + other.age) // 2)
    
    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

# Usage
p1 = Person("Alice", 25)
p2 = Person("Bob", 30)

print(p1)           # Person: Alice, Age: 25 (uses __str__)
print(repr(p1))     # Person('Alice', 25) (uses __repr__)
print(len(p1))      # 5 (uses __len__)
print(p1 + p2)      # Person: Alice & Bob, Age: 27 (uses __add__)
print(p1 == p2)     # False (uses __eq__)
```

**Common Magic Methods:**
- `__init__` - Constructor
- `__str__` - String representation (user-friendly)
- `__repr__` - String representation (developer-friendly)
- `__len__` - Length of object
- `__add__` - Addition operator
- `__eq__` - Equality comparison

**Simple samjho:** Magic methods matlab "special functions" - Python automatically call karta hai!

---

## Important Libraries

### Q20: How do you work with JSON in Python?
**Answer:**
```python
import json

# Python object to JSON string
data = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "hobbies": ["reading", "coding"]
}

# Convert to JSON string
json_string = json.dumps(data, indent=2)
print(json_string)

# Write to file
with open("data.json", "w") as file:
    json.dump(data, file, indent=2)

# Read from file
with open("data.json", "r") as file:
    loaded_data = json.load(file)
    print(loaded_data)

# JSON string to Python object
json_str = '{"name": "Alice", "age": 25}'
python_obj = json.loads(json_str)
print(python_obj)
```

**Simple samjho:** JSON matlab "data exchange format" - Python objects ko JSON mein convert karo aur wapas Python mein convert karo!

### Q21: How do you handle command line arguments?
**Answer:**
```python
import sys
import argparse

# Method 1: Using sys.argv
print("Command line arguments:", sys.argv)
# python script.py arg1 arg2
# Output: ['script.py', 'arg1', 'arg2']

# Method 2: Using argparse (recommended)
parser = argparse.ArgumentParser(description="Process some integers")
parser.add_argument("integers", nargs="+", type=int, help="Integers to sum")
parser.add_argument("--sum", dest="accumulate", action="store_const",
                   const=sum, default=max, help="Sum the integers")
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

args = parser.parse_args()
print(args.accumulate(args.integers))
```

**Simple samjho:** Command line arguments matlab "script run karte time values dena" - argparse use karo proper handling ke liye!

### Q22: How do you work with regular expressions?
**Answer:**
```python
import re

text = "Contact us at support@example.com or call 123-456-7890"

# Search for pattern
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
email_match = re.search(email_pattern, text)
if email_match:
    print("Email found:", email_match.group())

# Find all matches
phone_pattern = r'\d{3}-\d{3}-\d{4}'
phones = re.findall(phone_pattern, text)
print("Phone numbers:", phones)

# Replace text
new_text = re.sub(r'\d{3}-\d{3}-\d{4}', 'XXX-XXX-XXXX', text)
print("Masked text:", new_text)

# Split by pattern
words = re.split(r'\s+', text)
print("Words:", words)
```

**Simple samjho:** Regular expressions matlab "pattern matching" - text mein specific patterns find karo!

---

## Problem Solving (DSA)

### Q23: How do you find the two sum problem?
**Answer:**
```python
def two_sum(nums, target):
    # Method 1: Brute force O(n²)
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

def two_sum_optimized(nums, target):
    # Method 2: Hash map O(n)
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []

# Test
nums = [2, 7, 11, 15]
target = 9
print(two_sum(nums, target))        # [0, 1]
print(two_sum_optimized(nums, target))  # [0, 1]
```

**Simple samjho:** Two sum matlab "do numbers find karo jo add hoke target bane" - hash map use karo fast solution ke liye!

### Q24: How do you reverse a linked list?
**Answer:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev = None
    current = head
    
    while current:
        next_temp = current.next  # Store next node
        current.next = prev       # Reverse the link
        prev = current            # Move prev forward
        current = next_temp       # Move current forward
    
    return prev

# Test
# Create list: 1 -> 2 -> 3 -> 4 -> 5
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(5)

# Reverse it
reversed_head = reverse_list(head)

# Print reversed list: 5 -> 4 -> 3 -> 2 -> 1
current = reversed_head
while current:
    print(current.val, end=" -> ")
    current = current.next
print("None")
```

**Simple samjho:** Linked list reverse karna matlab "pointers ko ulta karna" - prev, current, next use karo!

### Q25: How do you find the maximum subarray sum (Kadane's Algorithm)?
**Answer:**
```python
def max_subarray_sum(nums):
    if not nums:
        return 0
    
    max_sum = current_sum = nums[0]
    
    for i in range(1, len(nums)):
        # Either start new subarray or extend existing one
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Test
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(max_subarray_sum(nums))  # 6 (subarray [4, -1, 2, 1])
```

**Simple samjho:** Maximum subarray sum matlab "continuous numbers ka maximum sum" - Kadane's algorithm use karo!

---

## Common Interview Patterns

### Q26: What are the common algorithmic patterns?
**Answer:**
```python
# 1. Two Pointers
def two_pointers_example(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []

# 2. Sliding Window
def sliding_window_example(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum = window_sum - arr[i-k] + arr[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum

# 3. Hash Map
def hash_map_example(arr, target):
    num_map = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []

# 4. Binary Search
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

**Simple samjho:** Common patterns matlab "common solutions" - two pointers, sliding window, hash map, binary search!

### Q27: What are the time complexities?
**Answer:**
```python
# O(1) - Constant time
def get_first_element(arr):
    return arr[0]  # Always takes same time

# O(log n) - Logarithmic time
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# O(n) - Linear time
def linear_search(arr, target):
    for i, num in enumerate(arr):
        if num == target:
            return i
    return -1

# O(n log n) - Linearithmic time
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

# O(n²) - Quadratic time
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

**Simple samjho:** Time complexity matlab "kitna time lagega" - O(1) fastest, O(n²) slowest!

---

## Quick Reference

### Python Data Types
```python
# Numbers
int_num = 42
float_num = 3.14
complex_num = 3 + 4j

# Text
string = "Hello World"

# Boolean
boolean = True

# Collections
list_data = [1, 2, 3]
tuple_data = (1, 2, 3)
dict_data = {"key": "value"}
set_data = {1, 2, 3}
```

### Common String Methods
```python
text = "  Hello World  "
text.strip()        # "Hello World"
text.upper()        # "  HELLO WORLD  "
text.lower()        # "  hello world  "
text.split()        # ['Hello', 'World']
text.replace("World", "Python")  # "  Hello Python  "
```

### Common List Methods
```python
fruits = ["apple", "banana"]
fruits.append("orange")     # Add to end
fruits.insert(1, "grape")   # Insert at index
fruits.remove("banana")     # Remove first occurrence
fruits.pop()                # Remove last element
fruits.sort()               # Sort in place
fruits.reverse()            # Reverse in place
```

### Common Dictionary Methods
```python
person = {"name": "John", "age": 25}
person["email"] = "john@email.com"  # Add/update
del person["age"]                   # Delete
person.get("name")                  # Get value safely
person.keys()                       # Get all keys
person.values()                     # Get all values
person.items()                      # Get all pairs
```

### File Operations
```python
# Reading
with open("file.txt", "r") as f:
    content = f.read()

# Writing
with open("file.txt", "w") as f:
    f.write("Hello World")

# Appending
with open("file.txt", "a") as f:
    f.write("New line")
```

### Exception Handling
```python
try:
    # Code that might cause error
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Always runs")
```

### List Comprehensions
```python
# Basic
squares = [x**2 for x in range(5)]

# With condition
evens = [x for x in range(10) if x % 2 == 0]

# Nested
matrix = [[1, 2, 3], [4, 5, 6]]
flattened = [num for row in matrix for num in row]
```

### Lambda Functions
```python
# Basic
square = lambda x: x**2

# With map
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))

# With filter
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

### OOP Basics
```python
class MyClass:
    def __init__(self, value):
        self.value = value
    
    def method(self):
        return self.value
    
    @classmethod
    def class_method(cls):
        return cls("default")
    
    @staticmethod
    def static_method():
        return "static"
```

---

## 🎯 Interview Tips

### Before the Interview
1. **Practice coding** - Solve problems daily
2. **Review concepts** - Go through this guide
3. **Prepare examples** - Have real-world examples ready
4. **Mock interviews** - Practice with friends

### During the Interview
1. **Think out loud** - Explain your thought process
2. **Ask questions** - Clarify requirements
3. **Start simple** - Begin with brute force, then optimize
4. **Test your code** - Walk through examples
5. **Handle edge cases** - Consider empty inputs, single elements

### Common Mistakes to Avoid
1. **Don't jump to code** - Plan first
2. **Don't ignore edge cases** - Handle them
3. **Don't use complex solutions** - Keep it simple
4. **Don't forget to test** - Verify your solution
5. **Don't give up** - Keep trying different approaches

---

## 🚀 Final Words

**Dost, ye complete guide hai Python interview ke liye!**

**Key Points to Remember:**
- **Practice regularly** - Coding is a skill that improves with practice
- **Understand concepts** - Don't just memorize, understand the why
- **Build projects** - Apply what you learn in real projects
- **Stay updated** - Python evolves, keep learning new features
- **Be confident** - You've got this!

**Good luck with your interviews! 🍀**

---

*Made with ❤️ for Python learners*
