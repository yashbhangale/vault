---
title: Access Modifiers in Java
tags:
  - java
---

Access modifiers in Java determine the visibility and accessibility of classes, methods, and variables

## 1. public  access Modifiers
The `public` modifier allows access from **anywhere** (other classes and packages).


```java
// File: Main.java
public class Main {
    public static void main(String[] args) {
        Person person = new Person();
        person.name = "John";  // Accessible because it's public
        person.displayInfo();  // Accessible because it's public
    }
}

// File: Person.java
public class Person {
    public String name;  // Public variable, accessible from anywhere

    public void displayInfo() {  // Public method, accessible from anywhere
        System.out.println("Name: " + name);
    }
}
```

## 2. private access modifiers

The `private` modifier restricts access to **within the same class only**. You can't access it from outside the class.

```java
public class BankAccount {
    private double balance;  // Private variable, not accessible from outside the class

    public BankAccount(double initialBalance) {
        balance = initialBalance;
    }

    // Public method to access the private variable
    public void deposit(double amount) {
        balance += amount;
    }

    public void displayBalance() {
        System.out.println("Balance: " + balance);
    }
}

public class Main {
    public static void main(String[] args) {
        BankAccount account = new BankAccount(1000);
        // account.balance = 500;  // Error! 'balance' is private
        account.deposit(500);     // We can access this public method
        account.displayBalance(); // We can access this public method
    }
}
```

## 3. protected access modifier

The `protected` modifier allows access within the **same package** and **subclasses** (even in different packages).

```java
// File: Animal.java
public class Animal {
    protected String type = "Animal";  // Protected variable

    protected void displayType() {  // Protected method
        System.out.println("This is a " + type);
    }
}

// File: Dog.java (same package or subclass in a different package)
public class Dog extends Animal {
    public void showType() {
        System.out.println("Dog type: " + type);  // Accessible because it's protected
        displayType();  // Accessible because it's protected
    }
}

// File: Main.java
public class Main {
    public static void main(String[] args) {
        Dog dog = new Dog();
        dog.showType();  // Accessible because 'Dog' is a subclass of 'Animal'
    }
}
```

## 4. **Default (No Modifier)**

If no access modifier is specified, the class or member is **package-private** (accessible only within the same package).

```java
// File: PackageExample.java (package-private class)
class PackageExample {
    String message = "Hello!";  // Package-private variable

    void showMessage() {  // Package-private method
        System.out.println(message);
    }
}

// File: Main.java (same package)
public class Main {
    public static void main(String[] args) {
        PackageExample example = new PackageExample();
        example.showMessage();  // Accessible because both classes are in the same package
    }
}
```

### Key Points:

- **`public`**: Accessible from **anywhere**.
- **`private`**: Accessible **only within the class**.
- **`protected`**: Accessible within the **same package** or **subclasses**.
- **Default** (no modifier): Accessible within the **same package** only.

