---
title: AZ-104 AZure application gateway
date: 2024-12-20
---


**Azure Application Gateway** is a web traffic load balancer designed specifically for **HTTP(S) traffic** at the **application layer (OSI Layer 7)**. It enables you to manage and optimize the delivery of web applications by offering advanced features like URL-based routing, SSL termination, session persistence, and a Web Application Firewall (WAF) for security.

---

### **Key Features of Azure Application Gateway**

1. **Layer 7 Load Balancing**:
    - Routes traffic based on HTTP(S) properties, such as URLs, headers, or cookies.
    - Example: Route `/api` requests to one backend pool and `/app` requests to another.
1. **URL Path-Based Routing**:
    - Directs requests to specific backend servers based on the URL path.
    - Example: Route requests to `/images` to a storage service and `/data` to an API service.
1. **SSL Offloading**:
    - Terminates SSL/TLS at the gateway, reducing the processing load on backend servers.
    - Optionally re-encrypts traffic when forwarding to backends (end-to-end encryption).
1. **Web Application Firewall (WAF)**:    
    - Protects web applications from common vulnerabilities like SQL injection, cross-site scripting (XSS), and others.
    - Based on OWASP (Open Web Application Security Project) core rule set.
5. **Multi-Site Hosting**:
    - Hosts multiple applications on the same Application Gateway using different domain names.
    - Example: Serve `www.site1.com` and `www.site2.com` from the same gateway.
6. **Redirection Support**:
    - Supports HTTP to HTTPS redirection or custom URL redirection.
7. **Session Affinity**:
    - Ensures requests from a particular client are always sent to the same backend server during a session.
8. **Autoscaling**:
    - Automatically scales based on traffic load to ensure high availability and performance.
9. **Custom Error Pages**:
    - Displays custom error messages for 403, 502, or other errors.

---

### **When to Use Azure Application Gateway**

1. **HTTP/HTTPS Traffic Load Balancing**:
    - When your application relies heavily on web traffic and you need application-layer routing.
2. **Web Application Security**:
    - Use WAF to protect against vulnerabilities and attacks.
3. **Hosting Multiple Web Applications**:
    - Ideal for scenarios where you need to host and route traffic for multiple domains or paths.
4. **SSL Offloading**:
    - If you want to reduce the overhead of SSL/TLS encryption on backend servers.
5. **Dynamic Routing Based on URL/Headers**:
    - When you need advanced traffic distribution based on request details.
6. **Autoscaling Web Traffic Handling**:
    - For unpredictable or growing traffic demands.

---

### **How Azure Application Gateway Works**

1. **Frontend**:
    - The Application Gateway listens for incoming HTTP/HTTPS requests on a public or private IP.
2. **Routing Rules**:
    - Configured rules determine how traffic is routed to backend pools based on URL paths, hostnames, or other properties.
3. **Backend Pools**:
    - A set of backend servers (e.g., VMs, App Services, AKS) that handle the actual requests.
4. **Health Probes**:
    - Monitors the health of backend servers to ensure traffic is sent only to healthy instances.

---

### **Comparison: Application Gateway vs. Load Balancer**

| **Feature**                  | **Application Gateway**               | **Load Balancer**   |
| ---------------------------- | ------------------------------------- | ------------------- |
| **OSI Layer**                | Layer 7 (Application)                 | Layer 4 (Transport) |
| **Traffic Type**             | HTTP(S)                               | Any TCP/UDP         |
| **Routing**                  | URL-based, header-based, cookie-based | IP-based            |
| **SSL Offloading**           | Yes                                   | No                  |
| **Web Application Firewall** | Yes                                   | No                  |

---

Azure Application Gateway is ideal for managing web applications with sophisticated traffic-routing and security needs. It is often used in conjunction with **Azure Front Door** for global load balancing or paired with a **Load Balancer** for hybrid scenarios.