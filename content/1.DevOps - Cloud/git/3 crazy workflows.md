---
title: 3 crazy workflows
tags: [devops---cloud, git]
---

![[Pasted image 20260206131226.png]]

GitFlow : industry standard (but last year its a bad approach)


![[Pasted image 20260206131455.png]]

![[Pasted image 20260206131628.png]]


3 Git Workflows Every Developer Should Know (Interview Notes)

---

# 1️⃣ [[Git Flow]]

![Image](https://wac-cdn.atlassian.com/dam/jcr%3Acc0b526e-adb7-4d45-874e-9bcea9898b4a/04%20Hotfix%20branches.svg?cdnVersion=3217)

![Image](https://itknowledgeexchange.techtarget.com/coffee-talk/files/2021/01/gitflow-hotfix-branch-diagram.jpg)





## 📌 Definition

Git Flow is a **branch-heavy workflow** designed for **structured development with planned releases**.

It separates **development**, **production**, **features**, **releases**, and **hotfixes** into dedicated branches.

---

## 🌳 Branch Structure

### Permanent branches:

- `main` → Production-ready code    
- `develop` → Integration branch (latest development)

### Supporting branches:

- `feature/*` → New features
- `release/*` → Preparing release
- `hotfix/*` → Emergency production fixes

---

## 🔄 Typical Flow

1. Create feature from `develop`
2. Merge feature back to `develop`
3. Create `release/*` from `develop`
4. QA + bug fixes on release branch
5. Merge release → `main` AND → `develop`
6. Tag version
7. Deploy

Hotfix:

- Branch from `main`
- Fix bug
- Merge back to `main` + `develop`

---

## ✅ Advantages

- Clear separation of concerns    
- Supports multiple production versions
- Excellent for large teams
- Strong release management

---

## ❌ Disadvantages

- Complex    
- Too many long-lived branches
- Slow feedback loop
- Hard for continuous deployment

---

## 🎯 Best Used When

- Enterprise environments    
- Versioned releases
- Traditional SDLC
- Banking / healthcare / legacy systems

---

## 🧠 Interview Key Points

### Q: Why use Git Flow?

👉 For **controlled releases** and **strict production stability**.

---

### Q: Difference between develop and main?

👉 `develop` = working code  
👉 `main` = production code

---

---

# 2️⃣ GitHub Flow


![Image](https://miro.medium.com/1%2AbDd_LRmc9oVQif2n4Q14SA.png)

Widely used with GitHub.

---

## 📌 Definition

GitHub Flow is a **lightweight workflow** built around **Pull Requests + Continuous Deployment**.

Only ONE permanent branch:

👉 `main`

Everything else is temporary.

---

## 🌳 Branch Structure

- `main` (production)
- short-lived feature branches

---

## 🔄 Typical Flow

1. Create branch from `main`
2. Make changes
3. Push branch
4. Open Pull Request
5. Code review + CI
6. Merge into `main`
7. Deploy immediately

---

## ✅ Advantages

- Simple
- Perfect for CI/CD
- Easy rollback
- Fast iteration
- Minimal branching

---

## ❌ Disadvantages

- No formal release branches
- Requires strong testing
- Less control for regulated industries

---

## 🎯 Best Used When

- Startups    
- SaaS products
- Web apps
- Continuous deployment environments

---

## 🧠 Interview Key Points

### Q: How is GitHub Flow different from Git Flow?

👉 No `develop` branch  
👉 No release branches  
👉 Everything merges directly to `main`

---

### Q: What makes GitHub Flow safe?

👉 Pull Requests + automated CI tests.

---

---

# 3️⃣ Trunk-Based Development


![Image](https://media.licdn.com/dms/image/v2/C5112AQGl_qtb6AJxbg/article-cover_image-shrink_600_2000/article-cover_image-shrink_600_2000/0/1578033300107?e=2147483647&t=pxdFkyKHz0dDeaHanQfCyyty1bDdITJcVfU3ewMDmiw&v=beta)



---

## 📌 Definition

Trunk-Based Development means:

👉 Everyone commits to a single branch (`main` / `trunk`)  
👉 Feature branches exist for **hours or days only**

---

## 🌳 Branch Structure

- `main` (trunk)
- ultra-short feature branches (optional)    

---

## 🔄 Typical Flow

1. Small change
2. Commit to trunk
3. CI runs
4. Deploy    

Unfinished features are hidden using:

- Feature flags
- Toggle    

---

## ✅ Advantages

- Fastest delivery    
- No merge hell
- Perfect for DevOps
- Encourages small commits
- Excellent for microservices

---

## ❌ Disadvantages

- Requires strong CI    
- Needs automated testing
- Demands discipline

---

## 🎯 Best Used When

- DevOps teams    
- Cloud-native systems
- Microservices
- High deployment frequency

---

## 🧠 Interview Key Points

### Q: Why Trunk-Based is preferred in DevOps?

👉 Enables **continuous integration + continuous delivery**.

---

### Q: How do you deploy incomplete features?

👉 Feature flags.

---

---

# ⚡ Comparison Table (Interview Gold)

| Workflow    | Branches | Release Style | Speed  | Best For   |
| ----------- | -------- | ------------- | ------ | ---------- |
| Git Flow    | Many     | Scheduled     | Slow   | Enterprise |
| GitHub Flow | Few      | Continuous    | Medium | SaaS / Web |
| Trunk-Based | Minimal  | Continuous    | Fast   | DevOps     |

---

# 🎯 Final Interview Summary (Say This)

> Git Flow is used for structured release management.  
> GitHub Flow is a lightweight PR-based workflow for continuous delivery.  
> Trunk-Based Development focuses on committing frequently to a single branch and is ideal for DevOps pipelines.


