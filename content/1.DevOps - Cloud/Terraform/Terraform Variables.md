##[[Interview Questions _ terraform]]


## 🧱 What are Terraform Variables? (Simple Meaning)

Terraform variables are **inputs** to your infrastructure code.

Instead of hard-coding values like region, VM size, or instance count, you **parameterize** them.

👉 Think of variables as **function arguments** for infrastructure.

![Image](https://k21academy.com/wp-content/uploads/2024/04/Datatypes.webp)


---

## 🔹 Why Variables Matter (Very Important)

Without variables ❌

```hcl
instance_type = "t2.micro"
```

With variables ✅

```hcl
instance_type = var.instance_type
```

### Benefits

- Reusable code
- Easy environment switch (dev / prod)
- Secure secrets handling
- Industry best practice

---

## 1️⃣ Declaring a Variable (variables.tf)

Basic syntax:

```hcl
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}
```

### Key parts

|Field|Meaning|
|---|---|
|variable|Variable name|
|type|Data type|
|default|Optional fallback value|
|description|Human-readable info|

---

## 2️⃣ Using a Variable (main.tf)

```hcl
resource "aws_instance" "demo" {
  ami           = "ami-0abcdef"
  instance_type = var.instance_type
}
```

👉 `var.` is mandatory to access variables.

---

## 3️⃣ Variable Types (VERY IMPORTANT)

### 🔸 String

```hcl
variable "region" {
  type    = string
  default = "ap-south-1"
}
```

---

### 🔸 Number

```hcl
variable "instance_count" {
  type    = number
  default = 2
}
```

Usage:

```hcl
count = var.instance_count
```

---

### 🔸 Boolean

```hcl
variable "enable_monitoring" {
  type    = bool
  default = true
}
```

---

### 🔸 List

```hcl
variable "availability_zones" {
  type    = list(string)
  default = ["ap-south-1a", "ap-south-1b"]
}
```

Usage:

```hcl
availability_zone = var.availability_zones[0]
```

---

### 🔸 Map (Very Common)

```hcl
variable "instance_tags" {
  type = map(string)
  default = {
    Name = "DevServer"
    Env  = "Dev"
  }
}
```

Usage:

```hcl
tags = var.instance_tags
```

---

## 4️⃣ Variable Without Default (Mandatory Input)

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}
```

Terraform will **ask during apply**:

```bash
terraform apply
```

---

## 5️⃣ Using terraform.tfvars (REAL WORLD)

Create file: `terraform.tfvars`

```hcl
instance_type = "t3.medium"
instance_count = 3
```

Terraform **auto-loads** this file ✅

💡 Best practice:

- `variables.tf` → definition
- `terraform.tfvars` → values

---

## 6️⃣ Passing Variables via CLI

```bash
terraform apply -var="instance_type=t3.large"
```

Multiple:

```bash
terraform apply \
  -var="instance_type=t3.large" \
  -var="instance_count=2"
```

---

## 7️⃣ Environment-wise Variables (DevOps Style)

```
env/
 ├── dev.tfvars
 ├── prod.tfvars
```

```bash
terraform apply -var-file=env/dev.tfvars
terraform apply -var-file=env/prod.tfvars
```

🔥 This is how **real companies manage infra**.

---

## 8️⃣ Sensitive Variables (Security MUST)

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}
```

✔ Value hidden in logs  
❌ Still stored in state file (use Vault later)

---

## 9️⃣ Output Variables (Bonus but Important)

```hcl
output "public_ip" {
  value = aws_instance.demo.public_ip
}
```

After apply:

```bash
Outputs:
public_ip = 13.234.x.x
```

---

## 🔟 Common Beginner Mistakes ❌

|Mistake|Fix|
|---|---|
|Hardcoding values|Use variables|
|Forget `var.`|Always prefix|
|Not typing variables|Always define type|
|Secrets in code|Use sensitive vars|
|One tfvars for all env|Use env-based files|

---

## 🧠 Interview + Real Job Tip

If asked:

> “How do you manage Terraform variables in production?”

Say:

> “We define variables in `variables.tf`, store environment-specific values in separate `.tfvars` files, and pass secrets securely using CI/CD or secret managers.”

🔥 This answer sounds **experienced**.

---

## 📌 Your Practice Task (IMPORTANT)

Do this today:

1. Create `variables.tf`
2. Create `main.tf`
3. Create `terraform.tfvars`
4. Use **string + number + map**
5. Run `terraform plan`

If you want, next I can teach:

- **Terraform locals**
- **Variable validation**
- **Modules with variables**
- **Terraform variables for AKS / AWS**
- **CKA + Terraform interview questions**
