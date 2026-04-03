---
title: request based matrics
tags: [office]
---

# ------------------------------

# **1. NODE-LEVEL ALERTS**

# ------------------------------

### **Node not ready**

```
kube_node_status_condition{condition="Ready", status!="true"} == 1
```

### **Node unreachable**

```
up{job="node-exporter"} == 0
```

### **Node CPU > 80%**

```
100 - avg by (instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100 > 80
```

### **Node memory > 80%**

```
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
/
node_memory_MemTotal_bytes * 100 > 80
```

### **Disk usage > 80%**

```
node_filesystem_usage{fstype!~"tmpfs|overlay"} * 100 > 80
```

### **Disk I/O latency high**

```
rate(node_disk_io_time_seconds_total[5m]) > 0.5
```

### **GPU usage > 80%**

```
DCGM_FI_DEV_GPU_UTIL > 80
```

---

# ------------------------------

# **2. NODE RESOURCE PRESSURE**

# ------------------------------

### **Evictions due to memory/disk pressure**

```
kube_pod_status_reason{reason=~"Evicted"} > 0
```

### **Out of disk**

```
kube_node_status_condition{condition="DiskPressure", status="true"} == 1
```

---

# ------------------------------

# **3. POD-LEVEL ALERTS**

# ------------------------------

### **CrashLoopBackOff**

```
kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff"} > 0
```

### **Pod stuck Pending**

```
kube_pod_status_phase{phase="Pending"} == 1
```

### **Liveness probe failures**

```
increase(kube_pod_container_status_last_terminated_reason{reason="LivenessProbeFailed"}[5m]) > 0
```

### **Readiness probe failures**

```
increase(kube_pod_container_status_last_terminated_reason{reason="ReadinessProbeFailed"}[5m]) > 0
```

### **Container restarts > 5 in 10 minutes**

```
increase(kube_pod_container_status_restarts_total[10m]) > 5
```

### **OOMKilled**

```
kube_pod_container_status_last_terminated_reason{reason="OOMKilled"} == 1
```

### **High CPU usage in container**

```
rate(container_cpu_usage_seconds_total[5m]) > 0.8
```

### **High memory usage in container**

```
container_memory_usage_bytes / container_memory_working_set_bytes > 0.8
```

---

# ------------------------------

# **4. DEPLOYMENT / STATEFULSET**

# ------------------------------

### **Replicas not matching desired**

```
kube_deployment_status_replicas_available < kube_deployment_spec_replicas
```

### **Deployment rollout failure**

```
kube_deployment_status_condition{condition="Progressing", status="false"} == 1
```

### **StatefulSet update failures**

```
kube_statefulset_status_replicas_ready < kube_statefulset_status_replicas
```

---

# ------------------------------

# **5. INGRESS / NETWORK Alerting**

# ------------------------------

### **Ingress high latency**

```
histogram_quantile(0.99, sum(rate(nginx_ingress_controller_request_duration_seconds_bucket[5m])) by (le)) > 1
```

### **Ingress 4xx or 5xx spike**

```
rate(nginx_ingress_controller_requests{status=~"4..|5.."}[5m]) > 0
```

### **Network packet loss**

```
rate(node_network_receive_errs_total[5m]) > 0
```

### **DNS issues**

```
rate(coredns_dns_request_count_total[5m]) == 0
```

---

# ------------------------------

# **6. PVC / STORAGE ALERTS**

# ------------------------------

### **PVC usage > 80%**

```
kubelet_volume_stats_used_bytes
/
kubelet_volume_stats_capacity_bytes * 100 > 80
```

### **PVC provisioning failed**

```
kube_persistentvolumeclaim_status_phase{phase="Pending"} == 1
```

### **Slow volume provisioning**

```
kube_persistentvolume_status_phase{phase="Pending"} == 1
```

---

# ------------------------------

# **7. APPLICATION-LEVEL ALERTS**

# ------------------------------

### **App latency > SLA**

```
histogram_quantile(0.99, sum(rate(app_request_duration_seconds_bucket[5m])) by (le)) > 1
```

### **Error rate > X%**

```
(
  sum(rate(http_requests_total{status_code=~"5.."}[5m]))
/
  sum(rate(http_requests_total[5m]))
) * 100 > 5
```

### **Low throughput**

```
rate(http_requests_total[5m]) < 1
```

### **DB connection pool exhaustion**

```
db_max_connections - db_active_connections < 5
```

### **Slow SQL queries**

```
rate(db_query_duration_seconds_sum[5m]) / rate(db_query_duration_seconds_count[5m]) > 0.2
```

### **Kafka / MQ backlog**

```
kafka_consumer_lag > 1000
```

---

# ------------------------------

# **8. SECURITY ALERTS**

# ------------------------------

### **Failed login spike**

```
increase(login_failures_total[10m]) > 20
```

### **Unauthorized API attempts**

```
increase(apiserver_request_total{code="403"}[10m]) > 10
```

### **Privileged containers running**

```
kube_pod_container_security_context_privileged == 1
```

### **Containers running as root**

```
kube_pod_container_security_context_run_as_user == 0
```

### **Image vulnerabilities found**

```
trivy_image_vulnerabilities{severity="CRITICAL"} > 0
```

---

# ------------------------------

# **9. REQUEST-BASED METRICS 

# ------------------------------

These are your pure request-level metrics.

### **Total requests**

```
sum(http_requests_total)
```

### **RPS (requests per second)**

```
rate(http_requests_total[1m])
```

### **Request count per status code**

```
sum by (status_code)(rate(http_requests_total[1m]))
```

### **Latency P50**

```
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

### **Latency P90**

```
histogram_quantile(0.90, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

### **Latency P99**

```
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

### **Error rate**

```
rate(http_requests_total{status_code=~"5.."}[5m])
```

### **Error %**

```
(
  sum(rate(http_requests_total{status_code=~"5.."}[5m]))
/
  sum(rate(http_requests_total[5m]))
) * 100
```

### **Slow requests (>1 sec)**

```
rate(http_request_duration_seconds_bucket{le="1"}[5m])
```

