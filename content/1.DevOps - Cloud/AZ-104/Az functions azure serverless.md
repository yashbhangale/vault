---
title: Az functions azure serverless
tags: [devops---cloud, az-104]
---
### ⚡ What is Azure Functions?

**Azure Functions** is a **serverless compute service** in Microsoft Azure that lets you run small pieces of code (called _functions_) **without managing servers or infrastructure**.

---

### 🔧 Key Features:

- **Event-driven**: Runs code in response to events like HTTP requests, timers, queue messages, etc.
- **Serverless**: Azure manages all infrastructure and scaling.
- **Pay-per-use**: You’re billed only for the time your code runs.
- **Supports multiple languages**: C#, JavaScript, Python, PowerShell, etc.
- **Easily integrates** with other Azure services like Blob Storage, Service Bus, Cosmos DB.

---

### ✅ Short Use Case:

A company wants to **resize uploaded images** automatically.

- A user uploads an image to **Azure Blob Storage**.
- This triggers an **Azure Function**.
- The function resizes the image and stores the new version in another container.

No server setup, and they only pay when the function runs.

---

Let me know if you want a visual diagram or difference between Azure Functions and App Service.



Yes, **Azure Functions** is **similar to ==AWS Lambda**== — both are **serverless computing services** offered by their respective cloud platforms.

---

### 🔁 **Azure Functions vs AWS Lambda: Quick Comparison**

| Feature            | Azure Functions                                | AWS Lambda                                  |
| ------------------ | ---------------------------------------------- | ------------------------------------------- |
| **Provider**       | Microsoft Azure                                | Amazon Web Services (AWS)                   |
| **Trigger Types**  | HTTP, Timer, Queue, Blob, etc.                 | HTTP (API Gateway), S3, DynamoDB, etc.      |
| **Languages**      | C#, JavaScript, Python, Java, PowerShell, etc. | Node.js, Python, Java, Go, Ruby, .NET, etc. |
| **Execution Time** | Default 5 mins, extendable to 60 mins          | Default 3 secs, extendable to 15 mins       |
| **Pricing Model**  | Pay-per-use (consumption or premium plans)     | Pay-per-use                                 |
| **Cold Start**     | Possible in consumption plan                   | Possible in standard usage                  |
| **Integration**    | Seamless with Azure ecosystem                  | Seamless with AWS ecosystem                 |

---

### ✅ Summary:

> **Azure Functions = AWS Lambda for Azure.**  
> Both are great for building lightweight, event-driven, auto-scaling apps **without managing servers**.

Want help choosing one based on your project?