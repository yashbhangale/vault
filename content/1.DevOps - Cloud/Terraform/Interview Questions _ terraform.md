
---

## 🔥 MOST ASKED Terraform Variables Interview Questions

---

### 1️⃣ What are variables in Terraform?

**Answer (Interview-ready):**  
Terraform variables are **inputs** that allow us to parameterize infrastructure code so it becomes **reusable, configurable, and environment-independent**.

---

### 2️⃣ Why do we use variables instead of hard-coding values?

**Answer:**

- Reusability across environments
- Easier maintenance
- Secure handling of sensitive data
- Cleaner and scalable IaC

---

### 3️⃣ How do you declare a variable in Terraform?

```hcl
variable "instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "t2.micro"
}
```

---

### 4️⃣ What are the supported variable types?

**Answer:**

- `string`
- `number`
- `bool`
- `list(type)`
- `set(type)`
- `map(type)`
- `object({})`
- `tuple([])`

---

### 5️⃣ Difference between list and set?

|List|Set|
|---|---|
|Ordered|Unordered|
|Allows duplicates|No duplicates|
|Index-based access|No index|

```hcl
list(string)
set(string)
```

---

### 6️⃣ What happens if a variable has no default value?

**Answer:**  
Terraform treats it as **required** and will prompt the user during `terraform apply` unless provided via `.tfvars`, CLI, or environment variables.

---

### 7️⃣ How can you pass variable values?

**Answer:**

1. Default value
2. `terraform.tfvars`
3. `-var` CLI flag
4. `-var-file`
5. Environment variables (`TF_VAR_name`)

---

### 8️⃣ What is terraform.tfvars?

**Answer:**  
A file used to **assign values to variables**, which Terraform **automatically loads** during execution.

```hcl
instance_type = "t3.medium"
```

---

### 9️⃣ How do you manage variables for multiple environments?

**Answer:**  
By using **separate tfvars files**.

```bash
terraform apply -var-file=dev.tfvars
terraform apply -var-file=prod.tfvars
```

---

### 🔟 How do you mark a variable as sensitive?

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}
```

**Follow-up Answer:**  
Sensitive values are **hidden from logs**, but still stored in the **state file**.

---

### 1️⃣1️⃣ Where are sensitive variables stored?

**Answer:**  
In the Terraform **state file**, even if marked sensitive.  
For production, we integrate **Vault / AWS Secrets Manager / Azure Key Vault**.

---

### 1️⃣2️⃣ Can Terraform variables be validated?

✅ Yes.

```hcl
variable "instance_count" {
  type = number

  validation {
    condition     = var.instance_count > 0
    error_message = "Instance count must be greater than zero"
  }
}
```

---

### 1️⃣3️⃣ Difference between variables and locals?

|Variables|Locals|
|---|---|
|Input values|Computed values|
|Passed externally|Defined internally|
|Change per env|Derived from logic|

---

### 1️⃣4️⃣ What is variable precedence order?

**Answer (High-value question):**

Highest → Lowest

1. CLI `-var`
2. CLI `-var-file`
3. `terraform.tfvars`
4. `*.auto.tfvars`
5. Default value

---

### 1️⃣5️⃣ Can variables be overridden?

**Answer:**  
Yes, using CLI flags or environment-specific tfvars files.

---

### 1️⃣6️⃣ How do environment variables work in Terraform?

```bash
export TF_VAR_region="ap-south-1"
```

Terraform auto-loads it as:

```hcl
var.region
```

---

### 1️⃣7️⃣ Can you use variables in backend configuration?

**Answer:**  
❌ No. Backend configuration does **not support variables** directly.  
Workaround: use `-backend-config` files.

---

### 1️⃣8️⃣ How do variables work with modules?

**Answer:**  
Modules **accept input variables** and return **outputs**.

```hcl
module "vpc" {
  source = "./vpc"
  cidr   = var.vpc_cidr
}
```

---

### 1️⃣9️⃣ Difference between map and object?

|Map|Object|
|---|---|
|Same type values|Mixed types|
|Dynamic keys|Fixed structure|

---

### 2️⃣0️⃣ What are common mistakes with Terraform variables?

**Answer:**

- Hardcoding values
- Storing secrets in code
- No validation
- Single tfvars for all environments
- Not typing variables

---

## 🧠 ADVANCED QUESTIONS (IMPRESS INTERVIEWER)

---

### 2️⃣1️⃣ Can you dynamically construct variables?

```hcl
locals {
  name = "${var.env}-${var.app}"
}
```

---

### 2️⃣2️⃣ How do you pass variables in CI/CD?

**Answer:**  
Using:

- Environment variables
- Secret managers
- Pipeline variable injection

Example:

```bash
TF_VAR_db_password=$DB_PASSWORD terraform apply
```

---

### 2️⃣3️⃣ How do you prevent wrong variable usage in prod?

**Answer:**

- Variable validation
- Separate prod tfvars
- CI/CD approval gates
- Policy as Code (Sentinel / OPA)

---

## 🧾 ONE-LINE CHEAT SHEET (Memorize)

> “Terraform variables make infrastructure reusable, environment-agnostic, and secure by separating configuration from code.”

---

