```
kubectl cordon aks-ondemandv2-36021883-vmss000005
```

```
kubectl drain aks-ondemandv2-36021883-vmss000005 --ignore-daemonsets --delete-emptydir-data
```

```
kubectl uncordon aks-ondemandv2-36021883-vmss000005
```


```
kubectl get nodes
```

