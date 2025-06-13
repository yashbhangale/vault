---
title: AZ-104 DNS
date: 2024-12-20
---

**DNS (Domain Name System)** is the internet's system for translating human-friendly domain names (like `www.example.com`) into machine-readable IP addresses (like `192.0.2.1`) that computers use to communicate with each other.

---

### **How DNS Works**

1. **User Request**:
    - When you type a URL (e.g., `www.example.com`) in a browser, your computer sends a request to resolve the domain name into an IP address.
2. **DNS Query Process**:
    - The query goes through several stages:
        1. **Recursive Resolver**: A DNS server that acts as an intermediary, finding the IP address for the requested domain.
        2. **Root Server**: The resolver contacts a root DNS server to get information about the domain's **TLD (Top-Level Domain)** (e.g., `.com`).
        3. **TLD Nameserver**: The resolver queries the nameserver for the TLD to get the authoritative server's location for the domain.
        4. **Authoritative Nameserver**: Finally, the resolver queries the authoritative nameserver for the domain, which provides the IP address.
3. **Response**:
    - The resolver sends the IP address back to your computer, which uses it to connect to the server hosting the website.

---

### **Key Components of DNS**

1. **Domain Names**:
    
    - Human-readable names (e.g., `example.com`) that map to IP addresses.
2. **IP Addresses**:
    
    - Machine-readable numerical labels (e.g., `192.168.1.1` for IPv4, or `2001:db8::1` for IPv6).
3. **DNS Records**:
    
    - Specific instructions within the DNS system that define how the domain name is handled. Common types include:
        - **A Record**: Maps a domain to an IPv4 address.
        - **AAAA Record**: Maps a domain to an IPv6 address.
        - **CNAME Record**: Aliases one domain to another.
        - **MX Record**: Specifies mail servers for email handling.
        - **TXT Record**: Holds text data, often for verification or security.
4. **DNS Servers**:
    
    - Machines responsible for resolving domain names into IP addresses:
        - **Recursive Resolver**: Finds the IP address on behalf of the client.
        - **Root Server**: First step in the DNS hierarchy.
        - **TLD Nameserver**: Provides information about domains in a specific TLD.
        - **Authoritative Nameserver**: Final authority for a specific domain.

---

### **Importance of DNS**

1. **Ease of Use**:
    
    - Users can remember domain names instead of numeric IP addresses.
2. **Scalability**:
    
    - Enables the global distribution of websites and services.
3. **Redundancy**:
    
    - Distributed nature ensures high availability and reliability.
4. **Security Features**:
    
    - Modern DNS supports features like DNSSEC to prevent attacks like spoofing.

---

### **Common DNS Use Cases**

- **Web Browsing**: Resolving domain names for websites.
- **Email**: Directing email to appropriate mail servers (via MX records).
- **CDN (Content Delivery Network)**: Distributing traffic to the nearest servers.
- **Load Balancing**: Distributing requests across multiple servers.

In essence, DNS acts as the internet's "phonebook," helping users access online resources seamlessly!