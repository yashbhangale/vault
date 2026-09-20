this notes are created while setting up landing zones

# AWS Resource Access Manager (RAM) — Structured Notes

These notes reorganize the handwritten document into a clean, revision-friendly format while keeping the original concepts and workflow intact. The document focuses on **AWS Resource Access Manager (RAM)**, a **centralized network/resource-sharing architecture**, and the setup of **VPCs, subnets, route tables, and shared resources**.

---

## 1. AWS Resource Access Manager — Overview

**AWS Resource Access Manager (RAM)** is used to share supported AWS resources between different AWS accounts.

### Basic architecture from the document

```text
                    AWS Organization
                           │
                           ▼
                  ┌──────────────────┐
                  │  Network Account  │
                  │                  │
                  │       VPC        │
                  │    ┌───────┐     │
                  │    │ Public│     │
                  │    │Subnet │     │
                  │    └───────┘     │
                  │    ┌───────┐     │
                  │    │  Pvt  │     │
                  │    │Subnet │     │
                  │    └───────┘     │
                  └────────┬─────────┘
                           │
                     AWS RAM Share
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       Development Account 1     Development Account 2
```

The idea is to keep networking resources centrally managed in a **Network Account** and allow other accounts to consume the shared resources.

---

# 2. Why Use a Centralized Network Account?

The document highlights several advantages of this approach.

### Key advantages

**1. Centralized Management**

- Networking resources can be managed from one account.
- Reduces duplication across AWS accounts.

**2. Efficient Resource Utilization**

- Existing network infrastructure can be shared instead of creating separate infrastructure for every account.

**3. Improved Security & Compliance**

- Centralized networking makes it easier to apply consistent security controls.
- Network configuration can be managed from a controlled account.

**4. Simplified Billing**

- Centralizing certain infrastructure can simplify management and cost tracking.

**5. Enhanced Collaboration**

- Multiple AWS accounts can consume shared networking resources.

**6. Faster Deployment**

- Development/application accounts can use existing network infrastructure instead of building networking from scratch.

These benefits are explicitly listed in the first page of the document.

---

# 3. Network Account Structure

The document starts with a **Network Account** containing:

- VPC
- Public subnet
- Private subnet

These resources are then intended to be shared with other accounts such as:

- Development Account 1
- Development Account 2

The general flow is:

```text
Network Account
      │
      └── VPC
          ├── Public Subnet
          └── Private Subnet
                    │
                    ▼
              AWS RAM Share
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
   Dev Account 1          Dev Account 2
```

---

# 4. VPC and Subnet CIDR Planning

The document specifically introduces **IPv4 CIDR ranges** and subnet creation.

### Example VPC CIDR

```text
VPC CIDR:
10.0.0.0/16
```

Then individual subnets can be carved out of this CIDR.

For example:

```text
VPC
10.0.0.0/16
│
├── Public Subnet
│   └── 10.0.1.0/24
│
└── Private Subnet
    └── 10.0.2.0/24
```

The handwritten document specifically shows `10.0.1.0/24` for a subnet and another `10.0.2.0/24` block for the private subnet.

### Important concept

A subnet's CIDR must be **inside the VPC's CIDR range** and must not overlap with another subnet in the same VPC.

---

# 5. Creating a Subnet

The document's workflow for creating a subnet is:

### Step 1 — Choose VPC

Select the required VPC.

Example:

```text
VPC Name:
demo-eun1-ram-vpc
```

### Step 2 — Give the subnet a name

Example:

```text
Subnet Name:
demo-eun1-ram-public-subnet
```

### Step 3 — Specify IPv4 CIDR

Example:

```text
10.0.1.0/24
```

### Step 4 — Create the subnet

For the private subnet, use another CIDR block from the same VPC range.

Example:

```text
10.0.2.0/24
```

The page-2 diagram lays out this exact sequence: **Create Subnet → Choose VPC → Subnet Name → CIDR Range**.

---

# 6. Internet Gateway

For the **public subnet**, the document indicates creating an **Internet Gateway (IGW)**.

### Flow

```text
Internet
   │
   ▼
Internet Gateway
   │
   ▼
Public Route Table
   │
   ▼
Public Subnet
```

The document notes the need to create an Internet Gateway and associate it with the VPC.

---

# 7. Route Tables

Route tables determine where network traffic from a subnet should go.

The document creates separate route tables for:

- Public subnet
- Private subnet

### Public Route Table

Example naming convention:

```text
demo-eun1-ram-public-rt
```

The public route table is associated with the **public subnet**.

### Private Route Table

Example:

```text
demo-eun1-ram-private-rt
```

The private route table is associated with the **private subnet**.

The notes explicitly mention creating route tables for both public and private subnets.

---

# 8. Public Route Table Configuration

A public subnet needs a route to the Internet Gateway.

The document shows adding a route similar to:

```text
Destination:
0.0.0.0/0

Target:
Internet Gateway
```

### Meaning

```text
0.0.0.0/0
     │
     ▼
Internet Gateway
```

`0.0.0.0/0` represents the default IPv4 route — traffic destined outside the VPC can be sent through the configured target.

The document specifically instructs to ensure the **public subnet has a public IGW route** and then add/edit the route accordingly.

---

# 9. Subnet ↔ Route Table Association

This is an important part of the setup.

### Public subnet

```text
Public Subnet
      │
      ▼
Public Route Table
      │
      ▼
Internet Gateway
```

### Private subnet

```text
Private Subnet
      │
      ▼
Private Route Table
```

The document specifically instructs to associate the **public route table with the public subnet** and the **private route table with the private subnet**.

---

# 10. AWS Resource Access Manager — Resource Share

Once the networking resources are created, the next step is to use **AWS Resource Access Manager** to share the resources.

The document's final page moves into:

```text
Management Account
        │
        ▼
Resource Access Manager
        │
        ▼
Create Resource Share
```

---

# 11. Creating the Resource Share

The intended process is:

```text
AWS RAM
  │
  └── Create Resource Share
          │
          ├── Select resources
          │
          ├── Select accounts/principals
          │
          └── Create Share
```

The purpose is to make the selected networking resources available to the required AWS accounts.

---

# 12. Important IDs to Record

One of the most important points in the document is on **page 5**.

When working with Resource Manager/RAM, the notes emphasize recording the **resource IDs**, rather than relying on VPC/subnet names.

Specifically:

```text
VPC ID
Subnet ID
```

The handwritten note says that in Resource Manager, the **VPC and Subnet IDs** are shown for shared resources, and these IDs should be noted.

### Example

```text
VPC:
vpc-xxxxxxxx

Public Subnet:
subnet-xxxxxxxx

Private Subnet:
subnet-yyyyyyyy
```

**Remember:** AWS resource names are human-readable labels; resource IDs are the actual identifiers used to uniquely reference resources.

---

# 13. Launching an EC2 Instance in the Shared Network

The final page also describes creating an **EC2 instance in the management account** and using the Resource Access Manager/shared networking setup.

The flow shown is:

```text
Management Account
       │
       ▼
Create EC2 Instance
       │
       ▼
Use Resource Access Manager
       │
       ▼
Select shared VPC / Subnet
```

The notes emphasize that when looking at the shared resources, you should identify them using their **VPC ID and Subnet ID**.

---

# 14. Complete End-to-End Workflow

Here's the entire process from the document in a clean sequence:

```text
                    AWS ORGANIZATION
                          │
                          ▼
                 ┌─────────────────┐
                 │  Network Account│
                 └────────┬────────┘
                          │
                          ▼
                     Create VPC
                     10.0.0.0/16
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
       Public Subnet            Private Subnet
       10.0.1.0/24              10.0.2.0/24
              │                       │
              ▼                       ▼
       Public Route Table       Private Route Table
              │
              ▼
       Internet Gateway
              │
              ▼
       0.0.0.0/0 → IGW
              │
              ▼
        AWS RAM Resource Share
              │
        ┌─────┴─────┐
        ▼           ▼
     Dev Acc 1    Dev Acc 2
        │           │
        └─────┬─────┘
              ▼
       Consume Shared
       Network Resources
```

---

# 15. Quick Revision Sheet

### AWS RAM

**Purpose:** Share supported AWS resources across AWS accounts.

### Network Account

Central account responsible for networking infrastructure.

### VPC

Example:

```text
10.0.0.0/16
```

### Public Subnet

Example:

```text
10.0.1.0/24
```

Associated with:

```text
Public Route Table
```

Public route:

```text
0.0.0.0/0 → Internet Gateway
```

### Private Subnet

Example:

```text
10.0.2.0/24
```

Associated with:

```text
Private Route Table
```

### RAM

Used to share the required network resources with other AWS accounts.

### IDs to remember

```text
VPC ID
Subnet ID
```

The document particularly stresses recording these IDs when working with the shared resources.

---

## 16. Practical Mental Model

Think of the architecture like this:

> **Network Account = landlord**  
> **VPC/Subnets = infrastructure**  
> **AWS RAM = mechanism for sharing the infrastructure**  
> **Development Accounts = tenants/users of the shared infrastructure**

So instead of:

```text
Account 1 → VPC
Account 2 → VPC
Account 3 → VPC
```

you can have:

```text
              Network Account
                    │
                  VPC
                    │
              AWS RAM Share
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       Account 1 Account 2 Account 3
```

This is the core architectural idea behind the notes.