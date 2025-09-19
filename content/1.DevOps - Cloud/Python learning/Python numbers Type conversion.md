
```python
x = 1
y = 2.8
z = 1j

# convert int to float
a = float(x)

# convert from float to int
b = int(y)

# Convert from int to complex 
c = complex(x)

print(a)
print(b)
print(c)

print(type(a))
print(type(b))
print(type(c))
```

##### Random Number

Python does not have a `random()` function to make a random number, but Python has a built-in module called `random` that can be used to make random numbers:

```python
import random
print(random.randrange(1,100))
```


