
## **1. Introduction to IAM**

- **Definition**:  
    IAM (Identity and Access Management) is a global AWS service that helps you securely control access to AWS services and resources.        

- **Purpose**:  
    It lets you manage _who_ (users, groups, roles) can _access what_ (services, resources) and _how_ (through permissions).

- **Global Service**:  
    IAM is **not region-specific** — the configuration applies globally.

- **Key Concepts**:      
    - **Users**: Individual identities with credentials (for humans).        
    - **Groups**: Collection of users with shared permissions.
    - **Roles**: Temporary access entities (for services olications).
    - **Policies**: JSON documents defining permissions.

- **Root Account**:  
    The first account created with full permissions. It should be **used rarely** and protected with **MFA**.

- **Principle of Least Privilege**:  
    Always grant the **minimum permissions** necessary for users or services to perform their tasks.    

---

## **2. IAM Policies**

- **Definition**:  
    Policies are **JSON-based documents** that define permissions (what actions are allowed or denied).

- **Structure of a Policy**:

```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": "s3:ListBucket",
          "Resource": "arn:aws:s3:::example-bucket"
        }
      ]
    }
    ```
    
    - **Version**: Policy language version.        
    - **Statement**: Main policy block.
    - **Effect**: `Allow` or `Deny`.
    - **Action**: Specifies AWS service actions (e.g., `s3:ListBucket`).
    - **Resource**: Defines specific resource (ARN).

- **Types of Policies**:    
    - **AWS Managed Policies**: Created and maintained by AWS (e.g., `AmazonEC2FullAccess`).
    - **Customer Managed Policies**: Created and controlled by users.
    - **Inline Policies**: Directly attached to one user, group, or role.

- **Policy Evaluation Logic**:
    
    1. By default, all requests are **denied**.
    2. An explicit **Allow** overrides the default deny.
    3. An explicit **Deny** always overrides an Allow.

---

## **3. Multi-Factor Authentication (MFA)**

- **Definition**:  
    MFA adds an extra layer of security by requiring **a second form of verification** (password + MFA code).

- **Why Use MFA**:    
    - Protects against stolen credentials.
    - Essential for **root account** and privileged users.

- **Types of MFA Devices**:    
    - **Virtual MFA Device** (e.g., Google Authenticator, Authy).
    - **Hardware Key Fob** (physical devices).
    - **U2F Security Key** (e.g., YubiKey).

- **Usage**:    
    - Enable MFA on IAM users or the root account.
    - Can enforce MFA-based conditions in policies using `aws:MultiFactorAuthPresent`.

---

## **4. AWS Access Keys (CLI and SDK)**

- **Purpose**:  
    Access keys allow **programmatic access** to AWS via CLI or SDKs.

- **Components**:    
    - **Access Key ID** – like a username.
    - **Secret Access Key** – like a password.

- **Creation and Management**:    
    - Each IAM user can have **up to two active access keys** for rotation.
    - Keys can be created, disabled, or deleted from the IAM console.
    
- **Security Best Practices**:    
    - Never share or hard-code access keys.
    - Rotate access keys periodically.
    - Use **IAM Roles** or **AWS SSO** instead of permanent keys when possible.

---

## **5. AWS CLI (Command Line Interface)**

- **Definition**:  
    The AWS CLI is a **unified tool** to manage AWS services from the terminal.    

- **Installation**:  
    Can be installed on Linux, macOS, or Windows.

- **Configuration Command**:

```bash
    aws configure
```

    - Prompts for access key, secret key, default region, and output format.     

- **Basic Usage Example**:

  ```bash
    aws s3 ls
    aws ec2 describe-instances
    aws iam list-users
    ```

- **Profiles**:  
    You can create multiple named profiles for different accounts/environments using `--profile`.    

- **Advantages**:    
    - Automates repetitive tasks.
    - Useful in scripting and DevOps pipelines.

---

## **6. AWS CloudShell**

- **Definition**:  
    CloudShell is a **browser-based shell** pre-configured with the AWS CLI, SDKs, and common tools.
        
- **Features**:    
    - Automatically authenticated with your **IAM credentials**.
    - Pre-installed AWS tools (Python, Git, Node.js).
    - Persistent **home directory** (1 GB storage).

- **Advantages**:
    - No local setup required.
    - Secure and easy to use for quick CLI tasks.

- **Use Case Example**:

   ```bash
	aws s3 cp file.txt s3://mybucket/
    ```

    No need to configure keys  authentication handled automatically.    

---

## **7. IAM Roles**

- **Definition**:  
    Roles are **temporary credentials** that grant permissions to AWS services or users without using long-term credentials.
    
- **Key Use Cases**:    
    - **EC2 Role**: Allows an EC2 instance to access AWS resources (like S3 or DynamoDB).
    - **Cross-Account Access**: Share resources across AWS accounts securely.
    - **Service Role**: Allows AWS services (like Lambda, ECS, or CodeBuild) to perform actions.

- **How Roles Work**:    
    - IAM roles use **temporary security tokens** (via AWS STS).
    - Assigned dynamically, not tied to a specific user.
- **Trust Policy**:
    - Defines _who can assume the role_.
    - Example:
  ```json
        {
          "Effect": "Allow",
          "Principal": {"Service": "ec2.amazonaws.com"},
          "Action": "sts:AssumeRole"
        }
        ```        
- **Benefits**:
    - No need to store credentials.
    - Ideal for automation and applications.

---

## **8. IAM Security Tools**

- **IAM Credentials Report**:    
    - Lists all users and their credential status (passwords, MFA, keys, etc.).
    - Helps with auditing and compliance.
    - Command:

```bash
        aws iam generate-credential-report
        aws iam get-credential-report
   ```

- **IAM Access Advisor**:    
    - Shows the **last access time** of each service per user/role.
    - Useful for identifying unused permissions and cleaning up policies.

- **IAM Access Analyzer**:    
    - Identifies resources shared with external entities (e.g., public S3 buckets).
    - Helps enforce least privilege by detecting unintended access.

- **Password Policy**:
    - Set organization-wide rules (length, rotation, complexity).

---

### **Summary**

| Feature            | Description                          | Use Case                              |
| ------------------ | ------------------------------------ | ------------------------------------- |
| **IAM User**       | Individual identity with credentials | Developer or admin login              |
| **IAM Group**      | Set of users with shared permissions | Assign same access to teams           |
| **IAM Role**       | Temporary credentials for services   | EC2, Lambda, Cross-account access     |
| **Policy**         | JSON permission document             | Define access rules                   |
| **MFA**            | Two-step verification                | Secure root/admin accounts            |
| **Access Key**     | CLI/SDK credentials                  | Programmatic access                   |
| **CloudShell**     | Browser-based AWS CLI                | Quick tasks without local setup       |
| **Security Tools** | Audit and analysis features          | Ensure compliance and least privilege |
