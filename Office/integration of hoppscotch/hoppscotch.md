```
helm template hoppscotch helm/charts/hoppscotch \
  --namespace=hoppscotch \
  --create-namespace \
  --values=helm/values/hoppscotch/values-${ENVIRONMENT}.yaml \
  > application-manifests/${ENVIRONMENT}/hoppscotch/manifests.yaml

```