kubectl edit configmap signoz-otel-collector -n signoz

ADDED this 👇

```
receivers:
  httplogreceiver/heroku:
    endpoint: 0.0.0.0:8081
    source: heroku
  httplogreceiver/json:
    endpoint: 0.0.0.0:8082
    source: json
  jaeger:
    protocols:
      grpc:
        endpoint: 0.0.0.0:14250
      thrift_http:
        endpoint: 0.0.0.0:14268
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
        max_recv_msg_size_mib: 16
      http:
        endpoint: 0.0.0.0:4318
  prometheus/dcgm:
    config:
      scrape_configs:
        - job_name: "dcgm"
          scrape_interval: 15s
          static_configs:
            - targets:
                - "dcgm-exporter.default.svc.cluster.local:9400"
  filelog:
    include:
      - /var/log/containers/*.log
    multiline:
      line_start_pattern: ^\d{4}-\d{2}-\d{2}
```


```
service:
  pipelines:
    logs:
      exporters:
      - clickhouselogsexporter
      - metadataexporter
      processors:
      - batch
      receivers:
      - otlp
      - httplogreceiver/heroku
      - httplogreceiver/json
      - filelog
```


```
kubectl rollout restart deployment signoz-otel-collector -n signoz
```

