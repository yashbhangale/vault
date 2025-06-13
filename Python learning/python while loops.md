##### Python Loops

Python has two primitive loop commands:

- while loops
- for loops

With the while loop we can execute a set of statements _as long as a condition is true._

```python
i = 1  
while i < 6:  
  print(i)  
  i += 1
```

##### Use of break statement

```python
i = 1
while i < 6:
  print(i)
  if (i == 3):
    break
  i += 1
```

##### use of continue statement

```python
i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)

# Note that number 3 is missing in the result
```

##### the else statement 
With the else statement we can run a block of code once when the condition no longer is true:

```python
i = 1  
while i < 6:  
  print(i)  
  i += 1  
else:  
	  print("i is no longer less than 6")
```