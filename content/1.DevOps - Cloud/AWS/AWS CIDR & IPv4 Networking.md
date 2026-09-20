
# AWS CIDR & IPv4 Networking 

These notes reorganize the handwritten document into a clean, quick-revision format while preserving the concepts and examples from the source. The document focuses on **CIDR notation, IPv4 address calculation, subnetting, and the parent/child relationship between VPCs and subnets**.

---

## 1. What is CIDR?

**CIDR = Classless Inter-Domain Routing**

CIDR notation is used to define an IP network and determine how many IP addresses belong to that network.

Format:

```text
IP-address / prefix-length
```

Example:

```text
11.0.0.0/24
```

Here:

- `11.0.0.0` → Network address
    
- `/24` → 24 bits are used for the network portion
    
- Remaining bits → Host portion
    

The document introduces CIDR in the context of networking and domain routing.

---

# 2. IPv4 Address Basics

An IPv4 address contains **32 bits**.

Example:

```text
11.0.1.125
```

IPv4 has four octets:

```text
11     .     0     .     1     .     125
│            │           │            │
8 bits       8 bits      8 bits       8 bits
```

Therefore:

```text
8 + 8 + 8 + 8 = 32 bits
```

So every IPv4 address is:

```text
32-bit address
```

The document explicitly illustrates `11.0.1.125` as a 32-bit IPv4 address with 8 bits per octet.

---

# 3. Calculating Number of IP Addresses

The key formula is:

```text
Number of IP addresses = 2^(32 - prefix)
```

### Example: `/24`

```text
32 - 24 = 8

2^8 = 256
```

Therefore:

```text
11.0.0.0/24
       ↓
     256 IPs
```

The document gives this example directly.

---

# 4. CIDR Examples

### `/24`

```text
32 - 24 = 8

2^8 = 256
```

Therefore:

```text
/24 → 256 IP addresses
```

---

### `/16`

```text
32 - 16 = 16

2^16 = 65,536
```

Therefore:

```text
/16 → 65,536 IP addresses
```

The document specifically shows:

```text
11.0.0.0/16 = 65,536 IPs
```

---

### `/8`

```text
32 - 8 = 24

2^24 = 16,777,216
```

Therefore:

```text
/8 → 16,777,216 IP addresses
```

This is also shown in the source notes.

---

# 5. Easy CIDR Rule

Remember:

> **Smaller prefix number = larger network = more IP addresses**

For example:

```text
/8
 ↓
Very large network

/16
 ↓
Smaller

/24
 ↓
Even smaller
```

So:

```text
/8  → 16,777,216 IPs
/16 → 65,536 IPs
/24 → 256 IPs
```

The handwritten notes summarize this idea as the CIDR range becoming smaller while the number of IP addresses available changes accordingly.

---

# 6. How to Calculate IP Count

Use this simple 3-step method.

### Step 1 — Start with 32

IPv4 always has:

```text
32 bits
```

### Step 2 — Subtract CIDR prefix

For `/28`:

```text
32 - 28 = 4
```

### Step 3 — Calculate 2ⁿ

```text
2^4 = 16
```

Therefore:

```text
/28 = 16 IP addresses
```

The document demonstrates this exact calculation:

```text
32 - 28 = 4
     ↓
    2^4
     ↓
16 addresses
```

---

# 7. Example: `11.0.1.0/28`

Let's break it down:

```text
CIDR:
11.0.1.0/28
```

Calculate host bits:

```text
32 - 28 = 4
```

Calculate addresses:

```text
2^4 = 16
```

So:

```text
11.0.1.0/28
      ↓
16 IP addresses
```

The document illustrates the range:

```text
11.0.1.0
11.0.1.1
11.0.1.2
11.0.1.3
...
11.0.1.15
```

Total:

```text
16 IP addresses
```

---

# 8. CIDR Range Example

For:

```text
11.0.1.0/28
```

The range is:

```text
11.0.1.0 → 11.0.1.15
```

Therefore:

```text
First address = 11.0.1.0
Last address  = 11.0.1.15
Total         = 16
```

This is shown visually on page 2 of the document.

---

# 9. VPC and Subnet Relationship

The second page introduces an important AWS networking concept:

> **A subnet is a child network carved out of a VPC's CIDR range.**

Example:

```text
VPC
11.0.0.0/16
│
├── Public Subnet
│   11.0.1.0/24
│
└── Private Subnet
    11.0.2.0/24
```

The document depicts a VPC with CIDR `11.0.0.0/16` and two child subnets: `11.0.1.0/24` and `11.0.2.0/24`.

---

# 10. VPC CIDR vs Subnet CIDR

Think of it as:

```text
                VPC
             11.0.0.0/16
          65,536 addresses
                  │
       ┌──────────┴──────────┐
       │                     │
       ▼                     ▼
 Public Subnet          Private Subnet
 11.0.1.0/24            11.0.2.0/24
 256 IPs                256 IPs
```

So the:

**VPC = Parent**

and

**Subnet = Child**

The source explicitly labels the VPC as the parent and the subnets as child networks.

---

# 11. Important CIDR Hierarchy

You can visualize CIDR allocation like this:

```text
Large Network
     │
     ▼
11.0.0.0/16
     │
     ├── 11.0.1.0/24
     │
     ├── 11.0.2.0/24
     │
     ├── 11.0.3.0/24
     │
     └── ...
```

A `/16` network can be divided into many smaller `/24` networks.

For example:

```text
/16
 ↓
65,536 IPs

Each /24
 ↓
256 IPs
```

Conceptually:

```text
65,536 / 256 = 256
```

So a `/16` contains **256 `/24` blocks**.

---

# 12. AWS Networking Mental Model

For AWS, remember:

```text
VPC
 │
 │ CIDR block
 │
 ├── Public Subnet
 │      │
 │      └── Resources
 │
 └── Private Subnet
        │
        └── Resources
```

Example from the notes:

```text
VPC
11.0.0.0/16

├── Public
│   11.0.1.0/24
│
└── Private
    11.0.2.0/24
```

---

# 13. Quick CIDR Reference Table

|CIDR|Host Bits|Total IPv4 Addresses|
|---|--:|--:|
|`/8`|24|16,777,216|
|`/16`|16|65,536|
|`/24`|8|256|
|`/28`|4|16|

Source examples include `/8`, `/16`, `/24`, and `/28`.

---

# 14. Fast Revision Formula

### Memorize this:

```text
IPv4 = 32 bits

IP Count = 2^(32 - CIDR)
```

Examples:

```text
/24 → 2^(32-24)
    → 2^8
    → 256 IPs
```

```text
/16 → 2^(32-16)
    → 2^16
    → 65,536 IPs
```

```text
/28 → 2^(32-28)
    → 2^4
    → 16 IPs
```

---

## 15. One-Line Mental Model

> **CIDR tells you how much of the 32-bit IPv4 address belongs to the network, and the remaining bits determine how many IP addresses exist in that network.**

And in AWS:

> **VPC is the larger/parent CIDR block, while subnets are smaller/child CIDR blocks carved from the VPC.**