---
title: beginner
tags: [reactjs]
---
**1. What is React?**

**React** is a JavaScript library developed by Facebook for building fast, interactive user interfaces, especially single-page applications. It uses a **component-based architecture** and a **virtual DOM** to efficiently update and render only the parts of the UI that change.

---
**2. What are the key features of React?**

- **JSX** – HTML-like syntax in JavaScript for easier UI coding.
- **Virtual DOM** – Improves performance by updating only changed parts.
- **Component-Based** – UI is split into reusable components.
- **Unidirectional Data Flow** – Predictable data flow via props and state.
- **Hooks** – Add state and lifecycle to functional components.
- **React Native** – Build mobile apps using the same React concepts.

---

3.**What is JSX?**

**JSX (JavaScript XML)** is a syntax extension for JavaScript used in React. It lets you write HTML-like code inside JavaScript, making it easier to create and visualize UI components. JSX is then compiled to regular JavaScript using tools like Babel.

---
4. **What is the difference between a class component and a functional component?**

**Class Component** vs **Functional Component** in React:

|Feature|Class Component|Functional Component|
|---|---|---|
|Syntax|Uses ES6 classes|Uses functions (simpler syntax)|
|State Management|`this.state`, `this.setState()`|Uses `useState()` Hook|
|Lifecycle Methods|Has methods like `componentDidMount()`|Uses Hooks like `useEffect()`|
|Code Complexity|More verbose|Cleaner and concise|
|Performance|Slightly heavier|More lightweight and faster|

---
5. **What are props in React?**

**Props** (short for _properties_) are **read-only inputs** passed from one component to another in React. They allow **data sharing** between components and help make components **reusable and dynamic**.

Think of props like **function arguments** – they let you customize components. Example:

```jsx
<Greeting name="John" />
```

Here, `name="John"` is a prop passed to the `Greeting` component.

---
6. **What is state in React?**

**State** in React is a built-in object used to **store dynamic data** that affects how the component behaves or renders. Unlike props, **state is mutable** and managed within the component.

You update state using:

- `this.setState()` in class components
- `useState()` Hook in functional components\

Example (functional):
```jsx
const [count, setCount] = useState(0);
```

Here, `count` is the state, and `setCount` updates it.

---

7. **How does setState work?**
**`setState`** is used to update the state in React, and it triggers a **re-render** of the component with the new state.

In **class components**:

```jsx
this.setState({ count: this.state.count + 1 });
```

In **functional components** with `useState`:

```jsx
setCount(count + 1);
```

✅ React batches multiple `setState` calls and updates the DOM efficiently using the **virtual DOM**.  
❗ State updates are **asynchronous**, so don’t rely on the updated state immediately after calling `setState`.

---

8. **What is the virtual DOM?**

 What is the **DOM**?

**DOM** stands for **Document Object Model**.  
It's a programming interface that represents a web page in a structured, tree-like form.

Think of it like this:

- When a browser loads a web page, it turns all the **HTML elements** (like `<div>`, `<p>`, `<button>`) into a **tree of objects**.
- This tree is called the **DOM**, and it lets JavaScript **read, change, add, or remove elements** from the page.

#### Example:

If you have this HTML:

```html
<body>
  <h1>Hello</h1>
  <button>Click me</button>
</body>
```

The browser turns it into a tree:

```
Document
 └── body
     ├── h1 ("Hello")
     └── button ("Click me")
```

JavaScript can then interact with this tree:

```js
document.querySelector("button").textContent = "Clicked!";
```

---

### So what is the **Virtual DOM** then?

The **Virtual DOM** is a **copy** of the real DOM kept in memory (not shown in the browser). It's used by tools like **React** to make updating the UI faster and smoother by avoiding direct manipulation of the real DOM each time something changes.

---

In short:

- **DOM** is the actual page structure the browser uses.
- **Virtual DOM** is a faster, smart version used by frameworks to update the page efficiently.

---

9. **What are React fragments?**

**React Fragments** are a way to group multiple elements **without adding extra nodes** to the DOM.

### Why use them?

In React, a component must return **a single parent element**. If you want to return multiple elements side by side, you usually wrap them in a `<div>`. But that adds an extra element to the DOM  which you often don’t want.

### React Fragment solves this by letting you group elements **without adding extra HTML**.

#### Example with extra `<div>` (not ideal):

```jsx
return (
  <div>
    <h1>Title</h1>
    <p>Description</p>
  </div>
);
```

#### Using React Fragment (better):

```jsx
return (
  <React.Fragment>
    <h1>Title</h1>
    <p>Description</p>
  </React.Fragment>
);
```

Or even shorter with the shorthand syntax:

```jsx
return (
  <>
    <h1>Title</h1>
    <p>Description</p>
  </>
);
```

### Key Point for Interviews:

> **React Fragments** allow you to group multiple elements **without adding extra nodes** to the DOM, helping keep the DOM clean and efficient.

---
10. **What is the difference between controlled and uncontrolled components?**

A **controlled component** in React is a form element (like `<input>`, `<textarea>`, or `<select>`) **whose value is managed by React state**.

#### Example:

```jsx
const [name, setName] = useState("");

<input value={name} onChange={(e) => setName(e.target.value)} />
```

- React controls the input value.
- You always know the current value from state.
- Easier to validate or manipulate input.

---

### 🔓 **Uncontrolled Component**

An **uncontrolled component** keeps its own internal state. React does **not** manage its value directly — instead, you access it using a **ref**.

#### Example:

```jsx
const nameRef = useRef();

<input ref={nameRef} />
```

- Browser controls the input value.
- You read the value only when needed (e.g., on form submit).
- Simpler for basic forms, but less flexible.

---

### 🔍 Key Differences

|Feature|Controlled|Uncontrolled|
|---|---|---|
|State managed by|React (`useState`)|DOM (`ref`)|
|Access to value|Always via state|Via `ref.current.value`|
|Validation/Control|Easier|Harder|
|Use case|Dynamic, complex forms|Simple or quick forms|

---

### 💡 Interview Tip:

> Controlled components give **more control and predictability** in React, while uncontrolled components are **simpler but less flexible**.


---

**What are hooks in React? Name a few commonly used hooks.**