```python
thisdict = {  
  "brand": "Ford",  
  "model": "Mustang",  
  "year": 1964  
}
```

Dictionaries are used to store data values in key:value pairs.
A dictionary is a collection which is ordered*, changeable and ==do not allow duplicates.==

> As of Python version 3.7, dictionaries are _ordered_. In Python 3.6 and earlier, dictionaries are _unordered_.

```python
thisdict = {  
  "brand": "Ford",  
  "model": "Mustang",  
  "year": 1964  
}  
print(thisdict)

# {'brand': 'Ford', 'model': 'Mustang', 'year': 1964}
```


##### Dictionary Items

- Dictionary items are ordered, changeable, and do not allow duplicates.
- Dictionary items are presented in key:value pairs, and can be referred to by using the key name.

```python
thisdict = {  
  "brand": "Ford",  
  "model": "Mustang",  
  "year": 1964  
}  
print(thisdict["brand"])

# Ford
```

##### The dict() Constructor
```python
thisdict = dict(name = "John", age = 36, country = "Norway")  
print(thisdict)
```

#####  Accessing Items

```python
thisdict = {
	"brand": "Ford",
	"model": "Mustang",
	"year": 1964
}

x = thisdict["model"]
```

##### Get Items
The `items()` method will return each item in a dictionary, as tuples in a list.

```python
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

x = thisdict.items()

print(x)
# dict_items([('brand', 'Ford'), ('model', 'Mustang'), ('year', 1964)])
```

```python
car = {
"brand": "Ford",
"model": "Mustang",
"year": 1964
}

x = car.items()

print(x) #before the change

car["year"] = 2020

print(x) #after the change

# dict_items([('brand', 'Ford'), ('model', 'Mustang'), ('year', 1964)])  
# dict_items([('brand', 'Ford'), ('model', 'Mustang'), ('year', 2020)])
```

```python
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
if "model" in thisdict:
  print("Yes, 'model' is one of the keys in the thisdict dictionary")

# Yes, 'model' is one of the keys in the thisdict dictionary
```

##### Change Values
```python
thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

thisdict["year"] = 2018

print(thisdict)

# {'brand': 'Ford', 'model': 'Mustang', 'year': 2018}
```

```python
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.update({"year": 2020})

print(thisdict)
# {'brand': 'Ford', 'model': 'Mustang', 'year': 2020}
```

![[Pasted image 20250305160427.png]]


