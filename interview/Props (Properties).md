---
title: interview Props (Properties)
date: 2024-12-24
---


### **What Are Props?**

In React, **props** (short for "properties") are ==used to pass data from a **parent component** to a **child component**==. Props are ==**read-only**==, which means ==they cannot be modified by the child component; the parent controls them.==

#### Example:

If a parent component has some data, it can pass it to its children like this:

```jsx
function ChildComponent(props) {
    return <h1>Hello, {props.name}!</h1>;
}

function ParentComponent() {
    return <ChildComponent name="Amit" />;
}
```

Here:

- The `ParentComponent` passes a prop `name="Amit"` to the `ChildComponent`.
- The `ChildComponent` accesses it using `props.name`.

---

### **How to Pass Props to Components?**

Props are passed as attributes when calling a child component inside JSX. Let’s see how it works:

#### Example 1: Passing Simple Data

```jsx
function Button(props) {
    return <button>{props.label}</button>;
}

function App() {
    return (
        <div>
            <Button label="Click Me" />
            <Button label="Submit" />
        </div>
    );
}
```

- The `Button` component receives a `label` prop.
- Each `Button` instance gets its own `label`.

#### Example 2: Passing Multiple Props

```jsx
function UserCard(props) {
    return (
        <div>
            <h2>{props.name}</h2>
            <p>Age: {props.age}</p>
        </div>
    );
}

function App() {
    return (
        <UserCard name="Sita" age={25} />
    );
}
```

- The `UserCard` component receives `name` and `age` as props.

---

### **Props Are Immutable**

Props are ==**read-only**.== A child component cannot modify its own props.

#### Example:

If you try to modify a prop like this:

```jsx
function Child(props) {
    props.name = "New Name"; // ❌ Error: Cannot assign to read-only property
    return <h1>{props.name}</h1>;
}
```

It will throw an error because React enforces that **data flows in one direction** (from parent to child).

---

### **Props Drilling**

**Props drilling** occurs when you pass props through multiple layers of components, even if only the last child needs the data. It can make your code messy and hard to maintain.

#### Example:

```jsx
function GreatGrandParent() {
    return <GrandParent message="Hello from GreatGrandParent!" />;
}

function GrandParent(props) {
    return <Parent message={props.message} />;
}

function Parent(props) {
    return <Child message={props.message} />;
}

function Child(props) {
    return <h1>{props.message}</h1>;
}
```

- The `message` prop starts in `GreatGrandParent` and is passed down through `GrandParent` and `Parent` before finally reaching `Child`.
- This creates unnecessary boilerplate and tightly couples components.

---

### **Problems with Props Drilling**

1. **Verbose Code**: You need to manually pass props through intermediate components, even if they don’t need it.
2. **Tightly Coupled Components**: Changes in one component can affect others.
3. **Hard to Maintain**: As your app grows, managing props through multiple layers becomes cumbersome.

---

### **Solutions to Avoid Props Drilling**

Props drilling can be avoided using **state management libraries** or React's built-in tools like **Context API**.

#### 1. **Using Context API**

The **Context API** allows you to share data across components without explicitly passing props through every level.

Example with Context API:

```jsx
import React, { createContext, useContext } from 'react';

const MessageContext = createContext();

function GreatGrandParent() {
    return (
        <MessageContext.Provider value="Hello from GreatGrandParent!">
            <Child />
        </MessageContext.Provider>
    );
}

function Child() {
    const message = useContext(MessageContext); // Access context directly
    return <h1>{message}</h1>;
}
```

- The `MessageContext` is like a global state for the `message` value.
- Any component inside the `Provider` can access the `message` without drilling props.

---

#### 2. **Using State Management Libraries**

Libraries like **Redux**, **MobX**, or **Zustand** allow you to manage global state and share it across components without props drilling.

---

### **When to Use Props and When Not To**

- Use **props** when:
    
    - The data is specific to a child component.
    - You need a simple and direct way to pass data.
- Avoid props (use Context or state management) when:
    
    - The same data is needed by many components at different levels.
    - You find yourself drilling props through components that don’t use them.

---

### **Summary**

1. **Props**:
    
    - Used to pass data from parent to child.
    - Immutable (cannot be modified by the child).
    - Accessed using `props.propertyName`.
2. **Props Drilling**:
    
    - Passing props through multiple layers of components.
    - Can make code messy and harder to maintain.
    - Avoid it by using tools like **Context API** or state management libraries.

Bro, this should make props and props drilling crystal clear! Let me know if you want examples or more details on Context or Redux. 😊