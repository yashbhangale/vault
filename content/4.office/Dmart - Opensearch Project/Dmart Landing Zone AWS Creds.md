


Dmart AWS SSO: https://aeldm.awsapps.com/start
	username : oneture
	 Password : 0_NyQY9{y
	 MFA : AWS sso: oneture

---
IAM Admin Creds:  Console sign-in URL :: [https://528087308771.signin.aws.amazon.com/console](https://528087308771.signin.aws.amazon.com/console)
		UserName : oneture
		 Password : 0_NyQY9{y

---

![[Pasted image 20260911160056.png]]


![[Pasted image 20260911160252.png]]


# Checklist 

# AWS Landing Zone — Post-Control Tower Checklist

## 1. Management Account Security

-  **Enable/Mandate MFA for Management Account root user**
    
    - [x]  Verify MFA is enabled
    - [x]  Secure root credentials
    - [x]  Do not use root for daily operations

---

## 2. IAM Identity Center

- [x]  **Enable AWS IAM Identity Center**
- [ ]  Integrate with D-Mart corporate IdP
    - [ ]  GCP / Google Workspace
    - [ ]  Okta
    - [ ]  Active Directory

- [ ]  Define user groups
    - [ ]  Platform/Admin
    - [ ]  Developers
    - [ ]  Security
    - [ ]  Auditors
- [ ]  Remove/reduce dependency on long-lived IAM users
- [ ]  Enable auditable SSO-based access

---

## 3. Permission Sets

- [ ]  Define **least-privilege Permission Sets**
- [ ]  Define time-bound/elevated access where required
- [ ]  Create standard Permission Sets
    
    - [ ]  Administrator
    - [ ]  PowerUser
    - [ ]  ReadOnly
    - [ ]  Security/Audit
- [ ]  Assign Permission Sets to groups/accounts
- [ ]  Document account → group → permission mapping
- [ ]  Avoid shared credentials/root access

---

## 4. Baseline SCPs / Governance

- [x]  Define baseline Service Control Policies
- [x]  Restrict workloads to **ap-south-1** where applicable
- [x]  Prevent disabling of security services
- [x]  Restrict unauthorized security configuration changes
- [x]  Define root-user restrictions for member accounts
- [x]  Test SCPs in non-production before enforcement

---

## 5. Security Services — Future

> Enable once the required services are deployed/ready.

- [x]  Enable **Amazon GuardDuty** organization-wide
- [x]  Enable **AWS Security Hub** organization-wide
- [x]  Enable **AWS Config**
- [ ]  Deploy **Config Conformance Packs**
- [ ]  Define centralized security findings/monitoring
- [ ]  Define security alerting process

---

## 6. Organization-wide CloudTrail

- [x]  Configure **organization-wide CloudTrail**
- [x]  Send CloudTrail logs to **Log Archive account**
- [x]  Create dedicated S3 bucket for audit logs
- [ ]  Enable S3 **Object Lock / immutable storage**
- [ ]  Enable appropriate encryption
- [x]  Restrict Log Archive access
- [x]  Define log retention period
	- [x]  Validate logs from all member accounts

---

## 7. Encryption & KMS

-  Define encryption baseline
-  Decide **AWS-managed vs Customer-managed KMS keys**
-  Define EBS encryption
-  Define S3 encryption
-  Define database encryption
-  Define KMS key ownership/access model
-  Define key rotation policy
-  Document encryption standards

---

## 8. Centralized Internet Egress

-  Design centralized internet egress through **Infrastructure account**
-  Deploy NAT Gateway
-  Define inspection architecture
-  Evaluate **AWS Network Firewall / 3rd-party firewall**
-  Route workload internet traffic through centralized egress
-  Define egress logging/monitoring
-  Restrict direct internet access where not required

---

## 9. Mandatory Tagging

-  Define mandatory tags:
    -  `Project`
    -  `Environment`
    -  `CostCenter`
    -  `Owner`
-  Define tagging standards/values
-  Enforce using SCP/Config where practical
-  Validate tags across workload resources
-  Use tags for cost allocation/reporting

---

## 10. Backup & Disaster Recovery

-  Define **AWS Backup** strategy
-  Define OpenSearch snapshot strategy
-  Enable S3 versioning where required
-  Create centralized/cross-account backup vaults
-  Define backup retention
-  Define cross-account backup
-  Define cross-region backup if required
-  Define restore testing process
-  Document RPO/RTO requirements

---

# Final Landing Zone Sign-off

-  Management Account secured
-  IAM Identity Center configured
-  Permission Sets implemented
-  SCP baseline implemented
-  Security services planned/enabled
-  Organization-wide CloudTrail configured
-  Encryption baseline defined
-  Network egress architecture defined
-  Tagging policy defined
-  Backup/DR strategy defined
-  Architecture & operational documentation completed