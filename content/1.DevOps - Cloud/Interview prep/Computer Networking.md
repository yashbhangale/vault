---
title: Computer Networking
tags: [devops---cloud, interview-prep]
---

### 🔹 Q1: What is an IP address?
**A:** An IP (Internet Protocol) address is a unique identifier assigned to each device connected to a network. It helps in locating and identifying the device on the internet or local network.

### 🔹 Q2: Difference between public and private IP address?
**A:** - **Public IP**: Globally unique, accessible over the internet.
- **Private IP**: Used within a local network; not routable on the internet (e.g., 192.168.x.x, 10.x.x.x).
  
###   🔹 Q3: What is a port?
**A:** A port is a logical access channel for communication between two devices. Each service on a device runs on a specific port (e.g., HTTP – port 80, SSH – port 22).

### 🔹 Q4: Difference between TCP and UDP?
- **TCP** (Transmission Control Protocol): Connection-oriented, reliable, slower (e.g., HTTP, SSH).  
- **UDP** (User Datagram Protocol): Connectionless, faster, but not reliable (e.g., DNS, streaming).

### 🔹 Q5: What is DNS?
**A:** DNS (Domain Name System) translates human-readable domain names (like google.com) into IP addresses (like 142.250.190.78).

### 🔹 Q6: What is a socket?
**A:** A socket is a combination of an IP address and a port number, used to establish a communication endpoint between two devices.

### 🔹 Q7: What is NAT (Network Address Translation)?
**A:** NAT translates private IP addresses to public IP addresses and vice versa, allowing multiple devices in a private network to access the internet using one public IP.

### 🔹 Q8: What is a subnet?
**A:** A subnet is a segmented piece of a larger network, used to divide and manage networks efficiently. It’s defined by a subnet mask or CIDR notation.

### 🔹 Q9: What is CIDR?
**A:** CIDR (Classless Inter-Domain Routing) is a method for allocating IP addresses and routing. Example: `192.168.1.0/24` means 256 IPs (from `.0` to `.255`).


### 🔹 Q10: What is the difference between HTTP and HTTPS?
- **HTTP**: Unsecured communication over port 80.
- **HTTPS**: Secure version using SSL/TLS encryption, over port 443.

### 🔹 Q11: What is a firewall?
**A:** A firewall is a security system that monitors and controls incoming and outgoing traffic based on predefined rules.

### 🔹 Q12: What is the difference between Load Balancer and Reverse Proxy?
- **Load Balancer**: Distributes incoming traffic across multiple servers.
- **Reverse Proxy**: Forwards client requests to backend servers and returns the response. Nginx can act as both.

### 🔹 Q13: Common Networking Commands?
- `ping <host>` – Test if host is reachable.
- `traceroute <host>` – Show path to host.
- `nslookup <domain>` – Check DNS resolution.
- `netstat -tulnp` – List active ports.
- `curl <url>` – Make web requests.
- `telnet <host> <port>` – Test connectivity to port.

### 🔹 Q14: What happens when you type a URL in the browser?
1. DNS lookup to resolve domain name.
2. TCP handshake between client and server.
3. HTTP/HTTPS request sent.
4. Server responds with data.
5. Browser renders the content.

### 🔹 Q15: What is a VPC?
**A:** VPC (Virtual Private Cloud) is a logically isolated network in the cloud (like AWS) where you can launch resources (EC2, databases) in private or public subnets.

### 🔹 Q16: What is the difference between Ingress and Egress traffic?
- **Ingress**: Incoming traffic to a system/network.
- **Egress**: Outgoing traffic from a system/network.

### 🔹 Q17: What is a CDN?
**A:** CDN (Content Delivery Network) caches and delivers content from servers located close to users, improving load time and availability.

### 🔹 Q18: What are some common ports?
- HTTP – 80
- HTTPS – 443
- SSH – 22
- FTP – 21
- DNS – 53
- MySQL – 3306
- PostgreSQL – 5432
- Kubernetes API – 6443

### 🔹 Q19: What is MTU?
**A:** MTU (Maximum Transmission Unit) is the largest size of a packet that can be sent in a network layer protocol. Mismatched MTUs can cause packet fragmentation or drops.

### 🔹 Q20: How do microservices communicate with each other in Kubernetes?
**A:** Usually over internal DNS names and cluster IPs. For example, `http://service-name.namespace.svc.cluster.local`.

### 🔹 Q21: What is a MAC address?
**A:** A MAC (Media Access Control) address is a hardware identifier assigned to a network interface card (NIC) used for communication within the local network.

### 🔹 Q22: What is ARP?
**A:** ARP (Address Resolution Protocol) maps IP addresses to MAC addresses so that devices can communicate within a local network.

### 🔹 Q23: What is the difference between Layer 2 and Layer 3?
- **Layer 2 (Data Link Layer)**: Works with MAC addresses (e.g., switches).
- **Layer 3 (Network Layer)**: Works with IP addresses (e.g., routers).

### 🔹 Q24: What is a routing table?
**A:** A routing table is a data table stored in a router that lists the paths to particular network destinations.

### 🔹 Q25: What is a default gateway?
**A:** The default gateway is the device (usually a router) that routes traffic from a local network to external networks or the internet.

### 🔹 Q26: What is a DHCP server?
**A:** DHCP (Dynamic Host Configuration Protocol) server dynamically assigns IP addresses and network configuration to client devices.

### 🔹 Q27: What is the difference between Static IP and Dynamic IP?
- **Static IP**: Manually assigned and fixed.
- **Dynamic IP**: Automatically assigned by a DHCP server.

### 🔹 Q28: What is port forwarding?
**A:** Port forwarding maps an external port to an internal IP and port, allowing access to services inside a private network from the internet.

### 🔹 Q29: What is a proxy server?
**A:** A proxy server acts as an intermediary between client and server, used for caching, filtering, logging, and hiding IP addresses.

### 🔹 Q30: What is a reverse proxy?
**A:** A reverse proxy (like Nginx or HAProxy) routes client requests to the appropriate backend server and returns the response to the client.

### 🔹 Q31: What is the difference between Load Balancer and Auto Scaling?
- **Load Balancer**: Distributes traffic to healthy instances
- **Auto Scaling**: Dynamically increases/decreases the number of instances based on traffic/load.

### 🔹 Q32: How do containers communicate in Docker?
**A:** By default, Docker containers in the same bridge network can communicate via container name or IP. You can also use custom networks or expose ports to host.

### 🔹 Q33: What is `iptables`?
**A:** `iptables` is a Linux utility used to configure the firewall rules for packet filtering and NAT.

### 🔹 Q34: What is a service mesh?
**A:** A service mesh (e.g., Istio, Linkerd) is a dedicated infrastructure layer to control service-to-service communication in a microservices architecture.

### 🔹 Q35: What is a network namespace?
**A:** Network namespaces provide isolated network stacks (interfaces, routing tables, etc.) for processes — used heavily in containers and Kubernetes pods.

### 🔹 Q36: What is the difference between SNAT and DNAT?
- **SNAT (Source NAT)**: Changes source IP (used in outbound traffic).
- **DNAT (Destination NAT)**: Changes destination IP (used in inbound traffic).

### 🔹 Q37: What is a health check in a load balancer?
**A:** It's a mechanism to determine if a backend server is healthy and able to serve traffic. Unhealthy servers are removed from the load balancing pool.

### 🔹 Q38: What is connection pooling?
**A:** It reuses network connections instead of opening a new one for every request, reducing overhead and improving performance.

### 🔹 Q39: How can you test if a port is open on a remote server?
- Use `telnet <host> <port>`
- Or `nc -zv <host> <port>`

### 🔹 Q40: What is a VPN?
**A:** A VPN (Virtual Private Network) encrypts your internet connection and routes it through a secure server, used to securely connect remote systems to a private network.

Absolutely! The **OSI (Open Systems Interconnection) Model** is a foundational networking concept — and a **must-know for DevOps interviews**, especially when asked about **protocols, ports, firewalls, load balancers, etc.**

---

## 📶 OSI Model – Explained with Interview Q&A

The OSI model has **7 layers**, each with a specific role in data communication.

---

# 🌐 OSI Model – Layers (Top to Bottom):

|Layer No.|Layer Name|Function Summary|Examples|
|---|---|---|---|
|7|**Application**|User interface; network services|HTTP, HTTPS, FTP, SSH, DNS|
|6|**Presentation**|Data formatting, encryption, compression|SSL/TLS, JPEG, MP3|
|5|**Session**|Session management between apps|API calls, NetBIOS|
|4|**Transport**|Reliable delivery, error handling|TCP, UDP|
|3|**Network**|Routing, addressing|IP, ICMP, Routers|
|2|**Data Link**|MAC addressing, frame delivery|Ethernet, MAC, Switches|
|1|**Physical**|Transmission over physical media|Cables, Hubs, Signals, Bits|

### 🔹 Q1: What is the OSI model?
**A:** The OSI model is a conceptual framework that standardizes the functions of a telecommunication or computing system into 7 distinct layers, enabling interoperability between different systems and protocols.

---

### 🔹 Q2: Which layer does IP work on?
**A:** IP works on the **Network Layer (Layer 3)**.

---

### 🔹 Q3: Which protocols work at the Transport layer?
**A:** **TCP and UDP** are the main protocols at the Transport Layer (Layer 4).

---

### 🔹 Q4: What is the role of the Application Layer?
**A:** It provides services directly to the user or application, like file transfers, emails, or browser data. Examples: HTTP, FTP, DNS.

---

### 🔹 Q5: What is the function of the Presentation Layer?
**A:** It handles **encryption**, **decryption**, **data translation**, and **compression**. For example, converting text to ASCII or encrypting via TLS.

---

### 🔹 Q6: What layer does a router operate at?

**A:** **Network Layer (Layer 3)**.

---

### 🔹 Q7: What layer does a switch operate at?
**A:** Traditional switches operate at the **Data Link Layer (Layer 2)**. Layer 3 switches can route as well.

---

### 🔹 Q8: What is the difference between TCP and UDP at the OSI level?
- **TCP (Layer 4):** Connection-oriented, reliable, ensures data arrives in order.
- **UDP (Layer 4):** Connectionless, faster but no guarantee of delivery.
---

### 🔹 Q9: At which layer does SSL/TLS work?

**A:** Mostly in the **Presentation Layer (Layer 6)** but often associated with **Application Layer** in practice (Layer 7).

---

### 🔹 Q10: What is encapsulation in the OSI model?

**A:** Encapsulation is the process of wrapping data with protocol-specific information at each layer (headers/footers), from Application to Physical.

---

## 📦 DevOps Relevance of OSI Layers

|DevOps Tool/Topic|OSI Layer(s) Involved|
|---|---|
|HTTP/HTTPS, APIs|Layer 7 – Application|
|TLS/SSL (e.g., HTTPS)|Layer 6 – Presentation|
|TCP, UDP Port Configs|Layer 4 – Transport|
|IP routing, VPC setup|Layer 3 – Network|
|MAC filtering, VLANs|Layer 2 – Data Link|
|Physical network setup|Layer 1 – Physical|

---

### ✅ Pro Tip for Interviews:

Always give examples from tools you’ve used, like:

> “For example, when I exposed a Docker container, I had to configure the port (Layer 4), IP (Layer 3), and ensure the web app over HTTP was reachable (Layer 7).”

