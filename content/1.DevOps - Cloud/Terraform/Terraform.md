1. iac writing a infra in version control scripts 
2. terraform is agent less
3. terraform is declarative


**Terraform** is an **open-source Infrastructure as Code (IaC)** tool created by **HashiCorp**. It allows you to define, provision, and manage cloud and on-premise infrastructure using a declarative configuration language called **HashiCorp Configuration Language (HCL)**.

---

### 🔍 **What Terraform Does**

Terraform automates the creation and management of your infrastructure. Instead of manually setting up servers, databases, networking, and other components, you write code that describes what you want, and Terraform does the rest.

---

### 💡 **Key Concepts of Terraform**

|Concept|Description|
|---|---|
|**Providers**|These are plugins for Terraform to interact with different services (e.g., AWS, Azure, GCP, Kubernetes, etc.).|
|**Resources**|The basic building blocks like VMs, buckets, networks defined in Terraform files.|
|**Modules**|Group of resources combined into reusable components.|
|**State**|Terraform keeps track of what infrastructure it has deployed using a `.tfstate` file.|
|**Plan**|Command to preview what Terraform will do (e.g., add, change, destroy).|
|**Apply**|Executes the actual changes as per the plan.|
|**Destroy**|Tears down everything managed by Terraform.|

---

### 🧱 **Structure of a Terraform Project**

```
main.tf       --> main configuration
variables.tf  --> variables used in config
outputs.tf    --> output values after apply
terraform.tfstate --> state file
```

---

### ⚙️ **Basic Workflow**

1. **Write Configuration**    
    ```hcl
    provider "aws" {
      region = "us-east-1"
    }
    
    resource "aws_instance" "example" {
      ami           = "ami-0c55b159cbfafe1f0"
      instance_type = "t2.micro"
    }
    ```

2. **Initialize Terraform**

    ```
    terraform init
    ```

3. **Preview Plan**

    ```
    terraform plan
    ```

4. **Apply Changes**

    ```
    terraform apply
    ```

5. **Destroy Infrastructure**

    ```
    terraform destroy
    ```


---

### 🌐 **Providers Supported by Terraform**

- **Cloud**: AWS, Azure, Google Cloud, Oracle Cloud
- **Container**: Docker, Kubernetes
- **SaaS**: GitHub, Datadog, Cloudflare
- **Others**: VMware, OpenStack, etc.

---

### 📌 **Real-World Use Cases**

1. **Provisioning Cloud Infrastructure**: Automate AWS EC2, RDS, S3 bucket creation.
2. **CI/CD Pipelines**: Spin up environments dynamically in DevOps workflows.
3. **Disaster Recovery**: Recreate infra from code during failures.
4. **Multi-cloud Deployment**: Manage resources across AWS + GCP using same tool.
5. **Scaling Infrastructure**: Define autoscaling groups, load balancers easily.

---

### 🧠 **Advantages**

- ✅ **Infrastructure as Code**
- ✅ **Idempotent** (same code = same result)
- ✅ **Version-controlled Infrastructure**
- ✅ **Reusable and Modular**
- ✅ **Supports Multi-cloud**
- ✅ **State Management**

---

### ⚠️ **Challenges**

- 🔧 Managing state in teams (use remote state via S3 + DynamoDB)
- 🚫 Error-prone if plan is not reviewed
- 🔄 Terraform is declarative, but sometimes you need imperative logic (handled via `count`, `for_each`, etc.)

---

### 🎓 **In Interviews / Exams**

- **What is Terraform?**
    > Tool for Infrastructure as Code to automate and manage cloud resources.

- **Difference from other tools like Ansible?**
    > Terraform is declarative and manages infrastructure. Ansible is imperative and is more for configuration management.
    
- **What is tfstate?**
    
    > File used to keep track of the current state of infrastructure.
    
- **Why use modules?**
    
    > For reusability and maintainability of Terraform code.
    

---

Let me know if you want a cheat sheet, real code examples, or help setting it up for AWS or Azure.



![[Pasted image 20250523185656.png]]

![[Pasted image 20250523185800.png]]

 ![[Pasted image 20250523190202.png]]
![[Pasted image 20250523190414.png]]

![[Pasted image 20250523190526.png]]


![[Pasted image 20250523190606.png]]


![[Pasted image 20250523190621.png]]


![[Pasted image 20250523190651.png]]


