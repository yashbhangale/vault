# DNS Configuration Guide

This guide shows you how to get the LoadBalancer address and configure DNS records for your domains.

## Step 1: Configure kubectl (if not already done)

```bash
aws eks update-kubeconfig --region eu-north-1 --name 20api-eks
```

## Step 2: Get the LoadBalancer Address

### Method 1: Using kubectl

```bash
kubectl get svc -n ingress-nginx ingress-nginx-controller
```

Look for the `EXTERNAL-IP` or `EXTERNAL-HOSTNAME` column. Example output:

```
NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP                                                              PORT(S)                      AGE
ingress-nginx-controller   LoadBalancer   10.100.x.x      a1b2c3d4e5f6-1234567890.eu-north-1.elb.amazonaws.com   80:32456/TCP,443:31567/TCP   5m
```

### Method 2: Get only the hostname (recommended)

```bash
kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

This will output something like:
```
a1b2c3d4e5f6-1234567890.eu-north-1.elb.amazonaws.com
```

### Method 3: Get the IP address (if available)

```bash
kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

**Note:** AWS LoadBalancers typically use hostnames, not static IPs. The IP may change, so use the hostname (CNAME) when possible.

## Step 3: Configure DNS Records in Hostinger

Once you have the LoadBalancer address, configure DNS records in your Hostinger account:

### Option A: Using CNAME (Recommended for subdomains)

1. **For `argo.20api.com` (subdomain):**
   - **Type:** CNAME
   - **Name:** `argo`
   - **Value:** `a1b2c3d4e5f6-1234567890.eu-north-1.elb.amazonaws.com` (your LoadBalancer hostname)
   - **TTL:** 300 (or Auto)
   - **Click Save**

2. **For `www.20api.com` (subdomain):**
   - **Type:** CNAME
   - **Name:** `www`
   - **Value:** `a1b2c3d4e5f6-1234567890.eu-north-1.elb.amazonaws.com` (your LoadBalancer hostname)
   - **TTL:** 300 (or Auto)
   - **Click Save**

### Option B: Using A Record (For root domain - if LoadBalancer provides IP)

**Note:** Most DNS providers don't allow CNAME at the root domain (apex domain). You have a few options:

#### Option B1: Use A Record with LoadBalancer IP (Not recommended - IP can change)
1. Get the LoadBalancer IP:
   ```bash
   kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
   ```
2. In Hostinger:
   - **Type:** A
   - **Name:** `@` (or leave blank for root)
   - **Value:** [LoadBalancer IP]
   - **TTL:** 300
   - **Click Save**

#### Option B2: Use Hostinger's ALIAS/ANAME feature (Recommended)
If Hostinger supports ALIAS or ANAME records:
- **Type:** ALIAS (or ANAME)
- **Name:** `@` (root)
- **Value:** `a1b2c3d4e5f6-1234567890.eu-north-1.elb.amazonaws.com`
- **TTL:** 300
- **Click Save**

#### Option B3: Move DNS to Route53 (Best for production)
For production, consider moving DNS to AWS Route53 which supports ALIAS records natively:
1. Transfer DNS management to Route53
2. Create ALIAS record pointing to LoadBalancer
3. This is the most reliable solution

## DNS Configuration Summary

Here's what you need to configure:

| Domain | Type | Name | Value |
|--------|------|------|-------|
| `argo.20api.com` | CNAME | `argo` | `[LoadBalancer Hostname]` |
| `www.20api.com` | CNAME | `www` | `[LoadBalancer Hostname]` |
| `20api.com` | ALIAS/A or CNAME* | `@` or blank | `[LoadBalancer Hostname or IP]` |

*Note: Root domain (`20api.com`) CNAME depends on Hostinger support.

## Step 4: Verify DNS Configuration

After configuring DNS, wait 5-15 minutes for DNS propagation, then verify:

```bash
# Check DNS resolution for subdomain
nslookup argo.20api.com

# Check DNS resolution for root domain
nslookup 20api.com

# Or use dig
dig argo.20api.com
dig 20api.com
```

Expected output should show your LoadBalancer hostname or IP.

## Step 5: Access Your Applications

Once DNS propagates:

1. **ArgoCD:**
   - URL: `http://argo.20api.com`
   - Username: `admin`
   - Password: Get it with:
     ```bash
     kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode
     ```

2. **Your React App:**
   - URL: `http://20api.com`
   - Or: `http://www.20api.com`

## Troubleshooting

### DNS not resolving?
- Wait 5-15 minutes for DNS propagation
- Check DNS records are correct in Hostinger
- Verify LoadBalancer is active: `kubectl get svc -n ingress-nginx`

### Getting "502 Bad Gateway"?
- Check ingress controller pods: `kubectl get pods -n ingress-nginx`
- Check ArgoCD pods: `kubectl get pods -n argocd`
- Check application pods: `kubectl get pods -n app`

### LoadBalancer showing "pending"?
- Wait a few minutes for AWS to provision the LoadBalancer
- Check AWS console for LoadBalancer status
- Verify node group is ready: `kubectl get nodes`

## Quick Reference Commands

```bash
# Get LoadBalancer hostname
kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

# Get LoadBalancer IP
kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

# Check all services
kubectl get svc --all-namespaces

# Check ingress
kubectl get ingress --all-namespaces

# Check DNS resolution
nslookup argo.20api.com
nslookup 20api.com
```

