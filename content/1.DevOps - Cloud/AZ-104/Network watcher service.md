---
title: AZ-104 Network watcher service
date: 2025-01-10
---



#### Connection troubleshoot tool

![alt text](Pastedimage20241120115712.png)

![alt text](Pastedimage20241120112716.png)


Azure Network Watcher is a monitoring and diagnostic service that provides tools to troubleshoot and gain insights into your Azure network resources. It helps ensure your Azure virtual networks operate efficiently by identifying connectivity issues, diagnosing performance problems, and monitoring network traffic.


### **Key Features of Azure Network Watcher**

1. **Network Diagnostics**:
    
    - **Connection Troubleshooting**: Checks connectivity between a virtual machine and an endpoint (e.g., another VM, an on-premises server, or a public endpoint).
    - **Network Security Group (NSG) Flow Logs**: Captures network traffic through NSGs for analysis.
    - **IP Flow Verify**: Validates whether traffic is allowed or denied to/from a specific IP address by NSG rules.

1. **Monitoring and Insights**:
    
    - **Packet Capture**: Captures network traffic packets for detailed analysis.
    - **Network Performance Monitor**: Provides insights into the performance of connections between resources.
    - **Topology Viewer**: Visualizes your network architecture and dependencies.

2. **Metrics and Logs**:
    
    - Collects and analyzes metrics/logs related to network health and usage (e.g., traffic volume, latency).

3. **Connection Monitor**:
    
    - Continuously monitors the connectivity of Azure resources to external endpoints or within Azure.

4. **Diagnostic Tools**:
    
    - **Next Hop Analysis**: Identifies the next hop in the network route for traffic.
    - **VPN Diagnostics**: Troubleshoots VPN gateway and connections.




### **When to Use Azure Network Watcher**

- Troubleshooting connectivity issues in Azure VNets.
- Monitoring and analyzing network traffic for performance or security concerns.
- Visualizing network topologies for better architecture understanding.
- Diagnosing issues with NSG rules or VPN configurations.
- Capturing packets for in-depth problem analysis during outages.

Network Watcher is an essential tool for maintaining healthy and secure Azure networks.