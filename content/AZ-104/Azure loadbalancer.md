---
title: AZ-104 Azure loadbalancer
date: 2025-01-10
---

![alt text](Pastedimage20241125204024.png)

---
used to distribute the incoming network traffic across a set of backend servers

---
#### Azure load balancer


![alt text](Pastedimage20241125203806.png)

---
- You can have an application hosted on a set of machines.
- You want user traffic to be distributed equally across the machines.
- For this we can make use of the Azure Load Balancer service,
- Here the Azure Load Balancer can distribute traffic across the private IP addresses of the backend machines.
- Load Balancer SKU's - The Basic SKU is going to retire on September 30, 2025
---
In azure we have standard load balancer which have SLA (_Service Level Agreement_) of 99.99% 

---

![alt text](Pastedimage20241125204234.png)

---
![alt text](Pastedimage20241125204308.png)
loadbalancer healthy or not (health probe )

---

![alt text](Pastedimage20241125204506.png)

---

To use  loadbalancer it is necessary to make a machines (vms) in availability set or scale set

![alt text](Pastedimage20241125212332.png)

---
### Deployment of basic load balancer in azure

![alt text](Pastedimage20241125215904.png)

---

![alt text](Pastedimage20241125220040.png)

---

# failed to setup load-balancer bcoz my vms are not on availability set it is on availability zones plz rectify this :(                      {lab 116}


---


![alt text](Pastedimage20241127000727.png)


> [!NOTE]
> like basic LB we dont need vms in availability set or scale set for standard load  balancer 


