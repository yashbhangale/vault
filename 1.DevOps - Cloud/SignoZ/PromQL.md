---
title: SignoZ PromQL
date: 2025-01-14
---

**PromQL (Prometheus Query Language)** is a query language used in **Prometheus** (a popular open-source monitoring system) to retrieve and manipulate time-series data stored in its database.

PromQL is powerful and flexible, enabling you to extract metrics, perform calculations, and create custom visualizations and alerts.

PromQL is also utilized in observability tools like SigNoz, which builds on Prometheus for metrics storage and querying.

## Key Concepts

1. metrics :
- The data you want to query, such as CPU usage, memory usage, or HTTP requests.
- Example: `http_requests_total` (a counter metric for total HTTP requests).

2. **Labels**:
- Key-value pairs that provide additional context to metrics.
- Example: `http_requests_total{method="GET", status="200"}` filters the metric for GET requests with a 200 status code.

3. **Time-Series**:
- Metrics are stored over time, enabling queries for historical trends or snapshots of data.

4. **Operators**:
- PromQL supports mathematical and logical operators for aggregating and comparing metrics.
- Examples: `+`, `-`, `*`, `/`, `and`, `or`.

5. **Functions**:
- Built-in functions to analyze metrics.
- Examples:
    - `rate()` calculates the rate of increase over time.
    - `avg()`, `max()`, `min()` for aggregations.
    - `histogram_quantile()` for histogram metrics.

6. **Aggregations**:
- Aggregates data based on dimensions (labels).
- Example: `sum(http_requests_total)` gives the total HTTP requests across all dimensions.












**PromQL (Prometheus Query Language)** is a query language used in **Prometheus** (a popular open-source monitoring system) to retrieve and manipulate time-series data stored in its database. PromQL is powerful and flexible, enabling you to extract metrics, perform calculations, and create custom visualizations and alerts.

PromQL is also utilized in observability tools like SigNoz, which builds on Prometheus for metrics storage and querying.

---
### **Basic PromQL Queries**

1. **Retrieve a Metric**:
    ```promql
    http_requests_total
    ```
    Retrieves all data points for `http_requests_total`.
    
2. **Filter by Labels**:
    ```promql
    http_requests_total{method="GET", status="200"}
    ```
    Retrieves metrics only for GET requests with a 200 status code.
    
3. **Calculate Rate of Change**:
    ```promql
    rate(http_requests_total[5m])
    ```
    Calculates the per-second rate of HTTP requests over the last 5 minutes.
    
4. **Aggregation Example**:
    ```promql
    sum(rate(http_requests_total[5m]))
    ```
    Calculates the total rate of HTTP requests across all dimensions.

5. **Grouping**:    
    ```promql
    sum(rate(http_requests_total[5m])) by (method)
    ```    
    Groups the total rate of HTTP requests by the `method` label.    

---

### **Use in SigNoz**

In SigNoz, PromQL is used to:

- Query metrics for visualizations in dashboards.
- Create custom metrics-based alerts.
- Perform in-depth troubleshooting by querying specific metrics.

Example: To create an alert for high CPU usage, you might use a query like:

```promql
rate(node_cpu_seconds_total{mode="idle"}[5m]) < 0.2
```
