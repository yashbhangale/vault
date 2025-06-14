 # 1. **What are hooks in React? Name a few commonly used hooks.**

### 🔄 What Are Hooks in React?

**Hooks** are special functions in React that let you **use state and other React features in functional components** (without writing class components).

They were introduced in **React 16.8** to make functional components more powerful and easier to manage.

---

### 🧠 Why use Hooks?

Before hooks, things like state and lifecycle methods were only available in **class components**. Hooks bring those capabilities to **function components**, making your code cleaner and more reusable.

---

### 🛠️ Commonly Used React Hooks

1. **`useState()`** – Add state to a functional component
    
    ```js
    const [count, setCount] = useState(0);
    ```
    
2. **`useEffect()`** – Perform side effects (like data fetching or subscriptions)
    
    ```js
    useEffect(() => {
      console.log("Component mounted or updated");
    }, []);
    ```
    
3. **`useRef()`** – Access or store a DOM element or mutable value
    
    ```js
    const inputRef = useRef(null);
    ```
    
4. **`useContext()`** – Access values from React context
    
    ```js
    const theme = useContext(ThemeContext);
    ```
    
5. **`useReducer()`** – For complex state logic (like Redux-style updates)
    
    ```js
    const [state, dispatch] = useReducer(reducer, initialState);
    ```
    

---

### ✅ Interview Definition:

> **Hooks are built-in functions in React that let you "hook into" state, lifecycle, and other React features from function components.**

---

# 2. **What is the useEffect hook?**

### 🔁 What is the `useEffect` Hook in React?

The **`useEffect`** hook lets you **run side effects** in your function components — like fetching data, updating the DOM, setting up timers, or subscribing to events.

It replaces lifecycle methods like `componentDidMount`, `componentDidUpdate`, and `componentWillUnmount` from class components.

---

### 📦 Basic Syntax:

```jsx
useEffect(() => {
  // Side effect logic here
}, [dependencies]);
```

---

### 🧠 When is `useEffect` used?

1. **On component mount** (like `componentDidMount`)
    ```jsx
    useEffect(() => {
      console.log("Component mounted");
    }, []);
    ```

2. **On state or prop change** (like `componentDidUpdate`)
    ```jsx
    useEffect(() => {
      console.log("Count changed!");
    }, [count]);
    ```

3. **Cleanup on unmount** (like `componentWillUnmount`)
    ```jsx
    useEffect(() => {
      const timer = setInterval(() => console.log("Tick"), 1000);
      return () => clearInterval(timer); // Cleanup
    }, []);
    ```

---

### ✅ Interview Definition:

> `useEffect` is a React hook that runs **side effects** after rendering, and can clean them up when needed. It’s used for tasks like data fetching, timers, subscriptions, and DOM updates.

---

# 3. What is the difference between useEffect and useLayoutEffect?

### ⚡ Key Difference Between `useEffect` and `useLayoutEffect`:

|Feature|`useEffect`|`useLayoutEffect`|
|---|---|---|
|**When it runs**|**After** the browser paints the UI|**Before** the browser paints the UI|
|**Blocking UI paint?**|❌ No – non-blocking|✅ Yes – blocking (synchronous)|
|**Use case**|Side effects like data fetching|Read/measure DOM before paint (e.g., for animations, layout fixes)|

---

### 🔁 `useEffect` (Async, after paint)

Runs **after** the DOM is painted. It's good for:

- API calls
- Event listeners
- Timers

```jsx
useEffect(() => {
  console.log("Runs after paint");
}, []);
```

---

### 🧱 `useLayoutEffect` (Sync, before paint)

Runs **synchronously before paint**, so the user **won’t see layout flickers**. Use it when:

- You need to measure layout (`getBoundingClientRect`)
- You need to update styles before the screen is shown

```jsx
useLayoutEffect(() => {
  console.log("Runs before paint");
}, []);
```

---

### ✅ Interview Summary:

> `useEffect` runs **after render**, ideal for non-blocking effects.  
> `useLayoutEffect` runs **before the browser paints**, ideal for layout measurements or DOM updates that must happen before the screen is visible.

---

# 4. **What is the useContext hook?**

The **`useContext`** hook lets you **access values from a React Context** directly inside your functional components — without needing to use a `<Context.Consumer>` wrapper.

---

### 👀 Why use it?

When you want to share data (like a theme, user info, or language setting) across many components **without passing props manually through every level**, React’s **Context API** is the solution — and `useContext` makes it easy to consume that shared data.

---

### 🛠️ Basic Example:

```jsx
// 1. Create a context
const ThemeContext = React.createContext("light");

// 2. Provide the context in a parent component
<ThemeContext.Provider value="dark">
  <App />
</ThemeContext.Provider>

// 3. Use the context value in a child component
import { useContext } from 'react';

const ThemedComponent = () => {
  const theme = useContext(ThemeContext); // "dark"
  return <div className={`theme-${theme}`}>Current theme: {theme}</div>;
};
```

---

### ✅ Interview Definition:

> `useContext` is a React hook that lets you **read and use values from a React Context** in function components, enabling cleaner and more efficient global state management.

---

# 5. **How do you optimize performance in a React app?**

#### 1. **Use `React.memo()`**

Prevents unnecessary re-renders of functional components if props haven't changed.

```jsx
const MyComponent = React.memo((props) => { ... });
```

#### 2. **Use `useMemo()` and `useCallback()`**

- `useMemo`: Memoizes expensive calculations
- `useCallback`: Memoizes functions to avoid re-creating on each render

```jsx
const memoizedValue = useMemo(() => expensiveCalc(data), [data]);
const handleClick = useCallback(() => doSomething(), []);
```

#### 3. **Code Splitting with React.lazy and Suspense**

Load components only when needed (e.g., route-based loading).

```jsx
const LazyComponent = React.lazy(() => import('./MyComponent'));
```

#### 4. **Avoid Unnecessary Re-renders**

- Keep component trees shallow
- Lift state only when necessary
- Use keys properly in lists

#### 5. **Use `shouldComponentUpdate` or `PureComponent` (Class)**

For class components, optimize re-renders by checking prop/state changes.

#### 6. **Use Efficient Lists with `react-window` or `react-virtualized`**

Only render visible items in large lists to save memory and CPU.

#### 7. **Minimize Inline Functions and Objects in JSX**

They cause re-renders due to reference changes.

#### 8. **Debounce or Throttle Input/Scroll Events**

Avoid triggering expensive updates on every keystroke or scroll.

#### 9. **Lazy Load Images and Assets**

Reduce initial load time by loading media only when needed.

---

### ✅ Interview Summary:

> Optimize React performance by **avoiding unnecessary re-renders**, using **memoization (`memo`, `useMemo`, `useCallback`)**, implementing **code-splitting**, and optimizing **large lists and DOM updates**.

---
# 6. **What is React Router and how does it work?**
**React Router** is a **routing library for React** that lets you create **single-page applications (SPAs)** with **multiple views** — without reloading the page.

It enables navigation between components using **URLs**, just like traditional websites, but handled **entirely in the browser**.

---

### ⚙️ How Does It Work?

React Router uses the **HTML5 History API** (or hash routing) to manage navigation **without refreshing the page**.

#### Key Concepts:

1. **`<BrowserRouter>`** – Wraps your app and enables routing using clean URLs.
    
2. **`<Routes>` and `<Route>`** – Define which component should load for which URL.
    
3. **`<Link>` or `useNavigate()`** – Navigate between routes without a full reload.
    

---

### 🛠️ Example:

```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link> | <Link to="/about">About</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}

const Home = () => <h2>Home Page</h2>;
const About = () => <h2>About Page</h2>;
```

---

### ✅ Interview Summary:

> **React Router** enables navigation in React apps **without page reloads**, using components like `<Route>`, `<Link>`, and hooks like `useNavigate()` to map URLs to components.

---

# 7.**How do keys work in React lists?**

### 🔑 How Do Keys Work in React Lists?

In React, **keys** are special props used to **identify elements in a list**. They help React **track which items have changed, been added, or removed**, so it can **efficiently update the UI**.

---

### 🛠️ Why are keys important?

When rendering a list:

```jsx
{items.map(item => (
  <li key={item.id}>{item.name}</li>
))}
```

React uses the `key` to:

- Match current and previous list items.
- Avoid re-rendering unchanged items.
- Improve performance and prevent bugs.

---

### ✅ Best Practices:

- Use a **unique and stable** value like `id` from your data.
- Avoid using the **array index as a key**, especially if the list can change (add/remove/reorder items), as it can cause incorrect DOM updates.

---

### ❌ Bad:

```jsx
{items.map((item, index) => (
  <li key={index}>{item.name}</li> // Can cause bugs!
))}
```

### ✅ Good:

```jsx
{items.map(item => (
  <li key={item.id}>{item.name}</li> // Unique and stable
))}
```

---

### ✅ Interview Summary:

> Keys in React lists **help identify which items change**, making updates more efficient. Always use **unique, stable keys** (like IDs), not array indices.

---

# 8. **What is the difference between useState and useReducer?**

### 🔄 `useState` vs `useReducer`

|Feature|`useState`|`useReducer`|
|---|---|---|
|**Purpose**|Manage **simple state**|Manage **complex state logic**|
|**Usage**|Directly update state with setters|Use a **reducer function** and `dispatch`|
|**Syntax Simplicity**|Easier to read/write|More structured and scalable|
|**Best for**|Few state variables, simple changes|Multiple related state values or actions|

---

### 🧠 `useState` Example (Simple)

```jsx
const [count, setCount] = useState(0);

<button onClick={() => setCount(count + 1)}>Increment</button>
```

---

### 🧠 `useReducer` Example (Complex)

```jsx
const reducer = (state, action) => {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    default:
      return state;
  }
};

const [state, dispatch] = useReducer(reducer, { count: 0 });

<button onClick={() => dispatch({ type: 'increment' })}>+</button>
```

---

### ✅ Interview Summary:

> `useState` is best for **simple state**, while `useReducer` is ideal for **complex state logic**, especially when dealing with **multiple actions or values**.

---
# 9. **What are higher-order components (HOC)?**

A **Higher-Order Component (HOC)** is a **function** that takes a component and **returns a new component** with added behavior or props.

It’s a **pattern for reusing logic** across multiple components — kind of like a wrapper or enhancer.

---

### 📦 Basic Syntax:

```jsx
const withExtraInfo = (WrappedComponent) => {
  return function EnhancedComponent(props) {
    return <WrappedComponent {...props} extra="Extra Prop" />;
  };
};
```

Then use it like:

```jsx
const MyComponentWithInfo = withExtraInfo(MyComponent);
```

---

### 🔍 Why use HOCs?

- Reuse component logic (e.g., auth, theming, logging)
    
- Add props or wrap behavior without modifying original components
    

---

### 🛠️ Real Example: withLoading HOC

```jsx
const withLoading = (WrappedComponent) => {
  return function ({ isLoading, ...rest }) {
    if (isLoading) return <p>Loading...</p>;
    return <WrappedComponent {...rest} />;
  };
};

const UserList = ({ users }) => (
  <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
);

const UserListWithLoading = withLoading(UserList);
```

---

### ✅ Interview Summary:

> A **Higher-Order Component (HOC)** is a function that takes a component and returns a new one with **enhanced behavior or shared logic**, enabling **code reuse and separation of concerns**.


# 10. **What is prop drilling and how can it be avoided?**

**Prop drilling** happens when you pass data (props) from a **parent component** through **many intermediate components** just to reach a deeply nested child.

📉 It can make your code harder to read, maintain, and scale — especially if those middle components don’t actually use the prop themselves.

---

### 🛠️ Example of Prop Drilling:

```jsx
function App() {
  const user = { name: "Alice" };
  return <Parent user={user} />;
}

function Parent({ user }) {
  return <Child user={user} />;
}

function Child({ user }) {
  return <GrandChild user={user} />;
}

function GrandChild({ user }) {
  return <p>{user.name}</p>;
}
```

Here, `user` is being passed down through multiple levels just to get to `GrandChild`.

---

### 🛑 How to Avoid Prop Drilling:

#### 1. **React Context API** (Best built-in solution)

Share data globally without passing it through every level.

```jsx
const UserContext = React.createContext();

function App() {
  const user = { name: "Alice" };
  return (
    <UserContext.Provider value={user}>
      <Parent />
    </UserContext.Provider>
  );
}

function GrandChild() {
  const user = useContext(UserContext);
  return <p>{user.name}</p>;
}
```

#### 2. **State Management Libraries**

- Redux
    
- Zustand
    
- Recoil  
    Useful for large apps with complex state needs.
    

#### 3. **Component Composition**

Pass components as children or props to reduce deep nesting.

---

### ✅ Interview Summary:

> **Prop drilling** is passing props through multiple levels unnecessarily. Avoid it using the **Context API**, **state management tools**, or **component composition**.

Would you like a quick visual diagram showing prop drilling vs context?