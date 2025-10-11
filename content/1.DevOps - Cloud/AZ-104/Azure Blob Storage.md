
- Cloud storage solution by Microsoft Azure for storing **unstructured data** (images, videos, docs, backups).
- "Blob" = **Binary Large Object**.
- Scalable, secure, and accessible via internet.

---

### 🔸 **Blob Types**

1. **Block Blob** – For large files like images/videos/documents. Most common.
2. **Append Blob** – For logs and data that is appended over time.
3. **Page Blob** – For virtual hard disks (used with Azure VMs).

---

### 🔸 **Storage Structure**

- **Storage Account** → top-level container.
- **Container** → like a folder inside the account.
- **Blob** → actual file/data object.

---

### 🔸 **Access Tiers**

1. **Hot** – Frequently used data (high cost, low latency).
2. **Cool** – Infrequently accessed (lower cost).
3. **Archive** – Rarely accessed, long-term (very cheap, slow access).

---

### 🔸 **Security**

- **SAS Token** – Temporary secure access link.
- **RBAC** – Role-based permissions.
- **Encryption** – Data is encrypted at rest.

---

### 🔸 **Common Use Cases**

- Storing media for apps/websites.
- Data backups and disaster recovery.
- Log files and telemetry.
- Big data storage for analytics/ML.

---

### 🔸 **Access Methods**

- **Azure Portal** (UI)
- **Azure CLI / PowerShell**
- **SDKs (Python, C#, etc.)**
- **Azure Storage Explorer**
- **REST API**
