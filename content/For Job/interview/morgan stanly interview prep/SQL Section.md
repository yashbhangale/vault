---
title: SQL Section
tags: [for-job, interview, morgan-stanly-interview-prep]
---

1) Write a query to get the **second highest salary** from an employee table

```sql
SELECT DISTINCT salary
FROM Employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;
```

2) Difference between `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN`.
   
   Inner join : returns only rows which have values in both tables
   Excludes non matching rows

```sql
SELECT e.name, d.department_name
FROM employees e
INNER JOIN departments d 
ON e.department_id = d.department_id;
```

left join 
- Returns **all rows from the left table** + matching rows from the right.
- If no match → returns `NULL` for right table columns.

```SQL
SELECT e.name, d.name
FROM employee e 
LEFT JOIN department d
ON e.department.id = d.department_id;
```


Similarly for right join 

```sql
SELECT e.name, d.department_name
FROM employees e
RIGHT JOIN departments d 
ON e.department_id = d.department_id;
```


full outer join , return both rows from both tables

```sql
SELECT e.name, d.department_name
FROM employees e 
FULL OUTER JOIN departments d
ON e.department_id = d.department_id;
```



### CROSS JOIN

The `CROSS JOIN` keyword returns the Cartesian product of the two tables, meaning it will return all possible combinations of rows from both tables. No `ON` clause is used.

```sql
SELECT column_name(s)
FROM table1
CROSS JOIN table2;
```


#### Where and Having

`WHERE` is used to filter individual rows before any grouping occurs,
`HAVING` is used to filter groups _after_ they have been created by a `GROUP BY` clause


### **Q1. A scheduled job failed because of a SQL error — how do you troubleshoot?**

- Check job logs / error message.
- Identify failing SQL query.
- Re-run query manually to reproduce error.
- Fix issue (syntax, missing table/data, permission).
- Re-run job after fix.

---

### **Q2. A query is running very slow — what steps will you take?**

- Check execution plan (`EXPLAIN`). 
- Verify indexes are used.
- Optimize joins/subqueries.
- Remove unnecessary functions in WHERE.
- Add filters early (reduce dataset).

---

### **Q3. How do you handle a deadlock / lock issue in DB?**

- Identify blocking session (DB tools / `sp_who2` / `pg_stat_activity`).
- Kill/terminate the offending query if needed.
- Analyze queries causing locks, optimize them.
- Suggest retry mechanism at application level.    

---

### **Q4. What are the common reasons for slow queries?**

- Missing index.
- Too many joins/subqueries.
- Functions used in WHERE clause.
- Huge table scan (no filters).

---

### **Q5. How do you monitor database health in production?**

- Track **indexes** (unused/missing).
- Check **blocking queries**.
- Monitor **long running queries**.
- Review **error logs** and system alerts.
- Use monitoring tools (Splunk, AppDynamics, Elastic, etc.).

---