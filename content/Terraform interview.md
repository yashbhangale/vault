### 1. **What is Terraform?**

**Answer:**  
Terraform is an **open-source Infrastructure as Code (IaC)** tool by **HashiCorp** that lets you **provision and manage infrastructure** across cloud providers (AWS, Azure, GCP, etc.) using **declarative configuration files**.

- Instead of manually creating resources, you define the infrastructure in `.tf` files.

---

### 2. **What are the key features of Terraform?**

**Answer:**

- **IaC**: Define infrastructure in code for automation.
- **Multi-Cloud**: Supports AWS, Azure, GCP, Kubernetes, etc.
- **Immutable Infrastructure**: Updates by recreating resources instead of modifying them in place.
- **Execution Plan (`terraform plan`)**: Previews changes before applying.
- **State Management**: Tracks current infrastructure.

---

### 3. **What is a Terraform Provider?**

**Answer:**  
Providers are **plugins** that allow Terraform to interact with APIs of cloud platforms (AWS, Azure, GCP) or other services (GitHub, Kubernetes).  
Example:

```hcl
provider "aws" {
  region = "us-east-1"
}
```

---
### 4. **What is a Terraform Module?**

**Answer:**  
A module is a **container for multiple resources** that can be reused.

- **Root module:** The main working directory.
- **Child module:** Reusable module called inside root.  
    Example:

```hcl
module "vpc" {
  source = "./modules/vpc"
}
```

---

### 5. **Explain Terraform State.**

**Answer:**  
Terraform stores infrastructure details in a **state file (`terraform.tfstate`)** to track real-world resources.

- Helps Terraform know what exists and what needs to change.    
- Can be stored **locally** or **remotely (e.g., S3, Azure Blob)**.

---

### 6. **What is the difference between `terraform plan` and `terraform apply`?**

| Command           | Purpose                                                  |
| ----------------- | -------------------------------------------------------- |
| `terraform plan`  | Shows changes **without applying** them. (Dry-run)       |
| `terraform apply` | Applies changes to create/update/destroy infrastructure. |

---

### 7. **What is the purpose of `terraform init`?**

**Answer:**  
Initializes a Terraform working directory.

- Downloads providers & modules.
- Sets up backend configuration.

---

### 8. **What is a Backend in Terraform?**

**Answer:**  
Backends define **where the state file is stored** (local or remote).  
Examples:

- **Local backend:** State stored in local disk (default).    
- **Remote backend:** AWS S3, Azure Blob, Terraform Cloud.

---

### 9. **What are Terraform Variables and Outputs?**

**Answer:**

- **Variables:** Store reusable values (like region, instance type).    
    ```hcl
    variable "region" { default = "us-east-1" }
    ```

- **Outputs:** Display values after apply (like IP address).

    ```hcl
    output "instance_ip" { value = aws_instance.my_vm.public_ip }
    ```    

---

### 10. **What is the difference between `terraform import` and `terraform taint`?**

- `terraform import`: Brings **existing infrastructure** under Terraform management.
- `terraform taint`: Marks a resource to be **destroyed and recreated** during the next apply.

---

## ⚡ **Intermediate Level Questions**

These test practical usage.

### 11. **How do you handle Secrets in Terraform?**

**Answer:**

- Use **Terraform Variables** with `sensitive = true`.    
- Store in **environment variables** or **Vault/KMS/Secret Manager**.
- Avoid committing `.tfstate` with secrets (use remote backend with encryption).

---

### 12. **What are Terraform Workspaces?**

**Answer:**  
Workspaces allow **multiple state files** within the same configuration.

- Useful for managing **dev/test/prod** in a single codebase.  
    Commands:    

```bash
terraform workspace new dev
terraform workspace select prod
```

---

### 13. **How does Terraform handle dependencies between resources?**

**Answer:**  
Terraform automatically creates a **dependency graph**.

- Explicitly using `depends_on` if needed:    

```hcl
resource "aws_instance" "example" {
  depends_on = [aws_vpc.main]
}
```

---

### 14. **What is `terraform refresh`?**

**Answer:**  
Updates the state file to match the actual infrastructure **without changing resources**.

---

### 15. **What is the difference between `terraform destroy` and `terraform apply -destroy`?**

- `terraform destroy`: Destroys all managed resources.
- `terraform apply -destroy`: Also destroys resources but **allows plan preview** before deletion.

---

### 16. **How do you lock state in Terraform?**

**Answer:**  
State locking prevents simultaneous changes.

- AWS S3 backend → Use **DynamoDB** for state locking.    
- Terraform Cloud → Built-in locking.

---

### 17. **How to upgrade a Terraform provider?**

**Answer:**

1. Change version in `required_providers`.    
2. Run:

```bash
terraform init -upgrade
```

---

### 18. **Explain Terraform Lifecycle Rules.**

**Answer:**  
Control resource behavior using `lifecycle` block:

```hcl
lifecycle {
  create_before_destroy = true
  prevent_destroy       = true
  ignore_changes        = [tags]
}
```

---

### 19. **How do you perform a Terraform rollback?**

**Answer:**  
Terraform has no direct rollback.

- Use **version control** (Git) to revert `.tf` files.    
- Apply previous state using:

```bash
terraform apply "previous-plan.tfplan"
```

---

### 20. **How does Terraform handle drift?**

**Answer:**  
Drift = Infrastructure changes **outside Terraform**.

- Run `terraform plan` to detect.    
- Run `terraform apply` to fix drift.

---

## 🚀 **Advanced/Scenario-Based Questions**

### 21. **How do you manage Terraform in a team environment?**

**Answer:**

- Use **remote state backend** (S3 + DynamoDB lock).    
- Enable **state locking**.
- Implement **CI/CD pipelines** (GitHub Actions, Jenkins).
- Follow Git branching (feature/dev/prod).

---

### 22. **What is the difference between Terraform and Ansible?**

|Feature|Terraform|Ansible|
|---|---|---|
|Purpose|**Provisioning** infra|**Configuration Management**|
|Execution|Declarative|Procedural|
|State|Maintains state file|No state file|

---

### 23. **How do you handle multi-cloud deployments in Terraform?**

**Answer:**

- Use multiple providers:  

```hcl
provider "aws" {
  region = "us-east-1"
}

provider "google" {
  project = "my-gcp-project"
}
```

---

### 24. **How do you secure Terraform state files?**

**Answer:**

- Store in **encrypted remote backends (S3 + KMS)**.
- Enable **IAM policies** for restricted access.
- Use **Terraform Cloud/Enterprise**.

---

### 25. **What is the difference between Terraform Cloud and Terraform Enterprise?**

|Feature|Terraform Cloud|Terraform Enterprise|
|---|---|---|
|Hosting|SaaS (managed by HashiCorp)|Self-hosted|
|Pricing|Free + Paid tiers|Paid only|
|Best for|Small/medium teams|Large orgs needing private control|

---

### 26. **How do you manage different environments (Dev/Stage/Prod)?**

**Answer:**

- Use **Workspaces** or **Directory structure**:

```
environments/
  dev/
  prod/
  staging/
```

- Use `tfvars` files for environment-specific variables.

---

### 27. **What is a Null Resource?**

**Answer:**  
Used to **execute provisioners** (like shell scripts) without creating actual infrastructure.

```hcl
resource "null_resource" "example" {
  provisioner "local-exec" {
    command = "echo Hello World"
  }
}
```

---

### 28. **How do you test Terraform code?**

**Answer:**

- `terraform plan` for dry-run.
- Use tools like **Terratest** (Go testing framework).
- Use **Checkov/TFLint** for security & syntax checks. 

---

### 29. **Explain Remote-Exec and Local-Exec Provisioners.**

- **local-exec:** Runs commands **on the machine running Terraform**.    
- **remote-exec:** Runs commands **inside the created resource** (e.g., SSH into an EC2).

---

### 30. **What is the difference between `count` and `for_each`?**

|Feature|`count`|`for_each`|
|---|---|---|
|Type|Numeric loop (0..n)|Map/Set iteration|
|Best use|Identical resources|Unique resources with different keys|

---

## 🔥 Quick Terraform Commands Table

|Command|Purpose|
|---|---|
|`terraform init`|Initialize directory|
|`terraform plan`|Preview changes|
|`terraform apply`|Apply changes|
|`terraform destroy`|Destroy infra|
|`terraform fmt`|Format code|
|`terraform validate`|Validate syntax|
|`terraform graph`|Dependency graph|

---

## ✅ **Tips for Interviews**

- Always mention **remote backend with locking** for team use.
    
- Emphasize **idempotency** (same code → same infra).
    
- Highlight experience with **AWS S3 + DynamoDB** or **Terraform Cloud**.
    
- If asked about rollback, explain **version control & previous plan** strategy.
    

---

Would you like me to create a **one-page PDF cheat sheet** of these questions for quick revision?