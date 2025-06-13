- Sets are used to store multiple items in a single variable.
- Set is one of 4 built-in data types in Python used to store collections of data, the other 3 are [List](https://www.w3schools.com/python/python_lists.asp), [Tuple](https://www.w3schools.com/python/python_tuples.asp), and [Dictionary](https://www.w3schools.com/python/python_dictionaries.asp), all with different qualities and usage.
- A set is a collection which is _unordered_, _unchangeable*_, and _unindexed_.

```python
thisset = {"apple", "banana", "cherry", "apple"}  
print(thisset)
```

```python
thisset = {"apple", "banana", "cherry"}  
  
print("banana" in thisset)
# true
```

###### Add item in set

```python
thisset = {"apple","banana"}
thisset.add("orange")
print(thisset)
```

###### Update item in set

```python
thisset = {"apple", "banana", "cherry"}  
tropical = {"pineapple", "mango", "papaya"}  
  
thisset.update(tropical)  
  
print(thisset)
# {'apple', 'mango', 'cherry', 'pineapple', 'banana', 'papaya'}
```

###### Remove item in set

```python
thisset = {"apple", "banana", "cherry"}  
thisset.remove("banana")  
print(thisset)
```




###### Methods 

![[Pasted image 20250305112257.png]]

