---
title: interview java oops in hinglish
date: 2024-12-27
---

Bhai, Java ka **Object-Oriented Programming (OOPs)** concept ekdum basic aur important hai. Yeh samajhne ke baad programming easy aur logical lagti hai. Main ekdum ground level se, examples ke saath, saari cheezein samjhaunga. Chalo shuru karte hain!

---

### **1. Object-Oriented Programming (OOPs) Kya Hai?**

- OOPs ek programming paradigm hai jo **objects** ke upar kaam karta hai.
- Har object ke paas **data (attributes)** aur **behavior (methods)** hota hai.

#### **Real-Life Example:**

Socho tum ek `Car` bana rahe ho:

- **Attributes**: Color, model, engine power, brand, etc.
- **Behavior**: Start, stop, accelerate, brake, etc.

Yeh pura ka pura OOPs ka base hai – real-world entities ko code mein model karna.

---

### **2. 4 Pillars of OOPs**

OOPs ke 4 main features hain:

1. **Encapsulation**
2. **Inheritance**
3. **Polymorphism**
4. **Abstraction**

Ab inhe examples ke saath samjhte hain.

---

### **3. Class and Object (Base Concepts)**

#### **Class:**

- Ek blueprint ya template hoti hai jo **objects** banane ke liye use hoti hai.
- Socho `Car` ek class hai, aur tum isse different objects (`Honda`, `BMW`) bana sakte ho.

#### **Object:**

- Ek **instance** of a class hota hai.
- Agar `Car` class hai, toh `Honda` ek object hoga jo attributes aur methods define karega.

#### **Code Example:**

```java
class Car {  // This is a class (blueprint)
    String brand;    // Attribute
    int speed;       // Attribute

    void start() {   // Method
        System.out.println(brand + " is starting!");
    }

    void accelerate() {
        System.out.println(brand + " is accelerating at " + speed + " km/h!");
    }
}

public class Main {
    public static void main(String[] args) {
        // Creating objects
        Car honda = new Car(); // Object 1
        honda.brand = "Honda";
        honda.speed = 120;
        
        Car bmw = new Car();   // Object 2
        bmw.brand = "BMW";
        bmw.speed = 150;

        // Using methods
        honda.start();       // Output: Honda is starting!
        honda.accelerate();  // Output: Honda is accelerating at 120 km/h!

        bmw.start();         // Output: BMW is starting!
        bmw.accelerate();    // Output: BMW is accelerating at 150 km/h!
    }
}
```

---

### **4. Encapsulation**

- Data ko **wrap** karna aur usse **hide** karna.
- Attributes ko `private` banate hain aur access karne ke liye **getters** aur **setters** ka use karte hain.
- Encapsulation ka fayda:
    - Data secure rehta hai.
    - Code modular aur maintainable banata hai.

#### **Code Example:**

```java
class Student {
    private String name;  // Private attribute
    private int age;

    // Setter for name
    public void setName(String name) {
        this.name = name;
    }

    // Getter for name
    public String getName() {
        return name;
    }

    // Setter for age
    public void setAge(int age) {
        if (age > 0) {  // Validation
            this.age = age;
        } else {
            System.out.println("Age must be positive!");
        }
    }

    // Getter for age
    public int getAge() {
        return age;
    }
}

public class Main {
    public static void main(String[] args) {
        Student student = new Student();

        // Using setters to set data
        student.setName("Yash");
        student.setAge(20);

        // Using getters to get data
        System.out.println("Name: " + student.getName());  // Output: Yash
        System.out.println("Age: " + student.getAge());    // Output: 20
    }
}
```

---

### **5. Inheritance**

- Ek class (child) doosri class (parent) se properties aur methods **inherit** karti hai.
- Use karte ho jab ek concept ya entity ke multiple variations ho.

#### **Example:**

Parent Class: `Animal`  
Child Classes: `Dog`, `Cat`

#### **Code Example:**

```java
// Parent class
class Animal {
    String name;

    void eat() {
        System.out.println(name + " is eating.");
    }
}

// Child class
class Dog extends Animal {
    void bark() {
        System.out.println(name + " is barking.");
    }
}

// Child class
class Cat extends Animal {
    void meow() {
        System.out.println(name + " is meowing.");
    }
}

public class Main {
    public static void main(String[] args) {
        Dog dog = new Dog();
        dog.name = "Tommy";
        dog.eat();      // Output: Tommy is eating.
        dog.bark();     // Output: Tommy is barking.

        Cat cat = new Cat();
        cat.name = "Kitty";
        cat.eat();      // Output: Kitty is eating.
        cat.meow();     // Output: Kitty is meowing.
    }
}
```

---

### **6. Polymorphism**

- **Many forms** ka matlab hai ki same method ko alag-alag tarike se use kar sakte ho.
- 2 types:
    1. **Compile-Time Polymorphism (Method Overloading)**:
        - Same method name but different parameters.
    2. **Run-Time Polymorphism (Method Overriding)**:
        - Child class parent class ke method ko override karta hai.

#### **Code Example (Overloading):**

```java
class Calculator {
    // Method 1: Add 2 numbers
    int add(int a, int b) {
        return a + b;
    }

    // Method 2: Add 3 numbers
    int add(int a, int b, int c) {
        return a + b + c;
    }
}

public class Main {
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        System.out.println(calc.add(10, 20));       // Output: 30
        System.out.println(calc.add(10, 20, 30));  // Output: 60
    }
}
```

#### **Code Example (Overriding):**

```java
class Vehicle {
    void start() {
        System.out.println("Vehicle is starting.");
    }
}

class Car extends Vehicle {
    @Override
    void start() {
        System.out.println("Car is starting.");
    }
}

public class Main {
    public static void main(String[] args) {
        Vehicle vehicle = new Vehicle();
        vehicle.start();  // Output: Vehicle is starting.

        Vehicle car = new Car();
        car.start();      // Output: Car is starting.
    }
}
```

---

### **7. Abstraction**

- Bas important details dikhani hain, internal implementation **hide** karna.
- Achieve karte ho:
    1. **Abstract Classes**
    2. **Interfaces**

#### **Abstract Class Example:**

```java
abstract class Shape {
    abstract void draw(); // Abstract method (no body)

    void display() {
        System.out.println("This is a shape.");
    }
}

class Circle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing a circle.");
    }
}

public class Main {
    public static void main(String[] args) {
        Shape shape = new Circle();
        shape.draw();    // Output: Drawing a circle.
        shape.display(); // Output: This is a shape.
    }
}
```

#### **Interface Example:**

```java
interface Animal {
    void sound();  // Method without body
}

class Dog implements Animal {
    public void sound() {
        System.out.println("Dog barks.");
    }
}

public class Main {
    public static void main(String[] args) {
        Animal dog = new Dog();
        dog.sound();  // Output: Dog barks.
    }
}
```

---

### **8. Why Use OOPs?**

1. **Code Reusability**: Inheritance se code reuse hota hai.
2. **Modularity**: Code easily manageable hota hai (encapsulation).
3. **Flexibility**: Polymorphism se same method ka alag behavior milta hai.
4. **Real-World Modeling**: Real-world objects ko model karna easy hai.

---

### Final Words:

Bhai, bas concepts ko clear rakh aur coding practice kar. OOPs ek bar samajh gaya toh tumhare code ka structure aur readability next level pe chali jayegi! Agar aur doubt ho, toh bata de, ek aur example ke saath samjha dunga.