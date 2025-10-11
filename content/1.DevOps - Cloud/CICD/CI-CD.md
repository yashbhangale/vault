
### 1. What is CI/CD, and why is it important?

Answer:  
CI/CD stands for Continuous Integration and Continuous Delivery/Deployment.

- Continuous Integration (CI) is the practice of frequently merging code changes into a shared repository and running automated tests to detect issues early.
- Continuous Delivery/Deployment (CD) automates the release process so that software can be delivered quickly and reliably to production.  
    Importance: It reduces integration issues, improves code quality, accelerates releases, and enables faster feedback loops.

---

### 2. What’s the difference between Continuous Integration, Delivery, and Deployment?

Answer:

- CI: Developers merge code often; automated builds and tests run each time.
- Continuous Delivery: Code is always ready to be deployed but the deployment itself might require manual approval.
- Continuous Deployment: Every successful change is automatically pushed to production without human intervention.  
    Example: [[github actions]] CI → ArgoCD handles Continuous Deployment.

---

### 3. What problems does CI/CD solve in software development?

Answer:

- Integration conflicts between developers
- Manual, error-prone deployments
- Long release cycles
- Inconsistent environments
- Lack of visibility into test and deployment status
- Delayed bug discovery  
    CI/CD brings automation, faster delivery, and confidence in code releases.

---

### 4. What is a pipeline in CI/CD?

Answer:  
A pipeline is a sequence of automated steps (build → test → deploy) that code changes go through before release.  
Each stage ensures the code meets quality, security, and performance standards.  
Example:

```yaml
Build → Unit Test → Security Scan → Deploy to Staging → Manual Approval → Deploy to Production
```

---

### 5. What are typical stages in a CI/CD pipeline?

Answer:

1. Source: Triggered when code is pushed to a repo.
2. Build: Compile or package code, create Docker image.
3. Test: Run unit/integration tests.
4. Security/Quality: Run Trivy or SonarQube scans.
5. Deploy: Push image to registry, deploy to dev/staging/prod.
6. Monitor: Check deployment success and performance.

---

### 6. What happens in the “build” stage vs “deploy” stage?

Answer:

- Build stage: Converts source code into a runnable artifact (e.g., JAR, container image).
- Deploy stage: Takes that artifact and places it in the target environment (e.g., Kubernetes cluster, VM).  
    Example:
- Build: `docker build -t myapp:v1 .`
- Deploy: `kubectl apply -f deployment.yaml`

---

### 7. What are some popular CI/CD tools?

Answer:

- CI tools: Jenkins, [[github actions]], GitLab CI, CircleCI, Travis CI, Azure DevOps
- CD tools: ArgoCD, Spinnaker, FluxCD, Harness
- Other tools in ecosystem:
    - Artifact storage: Nexus, JFrog Artifactory
    - Monitoring: Prometheus, Grafana, SigNoz
    - Scanning: Trivy, SonarQube

---

### 8. Explain a simple CI/CD workflow for a microservice-based app.

Answer:

1. Developer commits code to GitHub.
2. GitHub Action triggers build.
3. Docker image is built and pushed to registry (e.g., DockerHub or Azure Container Registry).
4. Unit tests and security scans run automatically.
5. If tests pass, ArgoCD detects new image tag → deploys to AKS (Kubernetes).
6. SigNoz monitors deployment health.

---

### 9. How would you implement CI/CD using [[github actions]]?

Answer:

1. Create `.github/workflows/deploy.yml` file.
2. Define jobs:
    - Build: Run `npm install` or `mvn package`.
    - Test: Run unit/integration tests.
    - Deploy: Push Docker image and trigger ArgoCD or Helm deployment.
3. Use secrets in GitHub → `Settings > Secrets`.
4. Add triggers like `on: [push, pull_request]`.  
    Example:

```yaml
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t ${{ secrets.REGISTRY }}/app:${{ github.sha }} .
```

---

### 10. How do you trigger pipelines automatically?

Answer:  
Pipelines are triggered by events, such as:

- Code push or pull request (CI)
- Merging into a main branch
- New Docker image pushed
- Scheduled cron job
- Manual trigger (for controlled deployment)  
    Example:  
    [[github actions]]: `on: push`  
    GitLab CI: `only: [main]`

---
### 11. What is a runner (GitLab) or an agent (Jenkins)?

Answer:

- A runner/agent is the machine (VM, container, or node) that executes your pipeline jobs.
- It checks out code, runs commands, and reports results.  
    Example:
- Jenkins agent executes build/test commands.
- GitLab runners can be shared or self-hosted for custom environments.
---

### 12. How do you handle secrets in CI/CD pipelines?

Answer:

- Use encrypted secrets in your CI tool (e.g., GitHub Secrets, Jenkins Credentials).
- Don’t hardcode passwords, tokens, or API keys in scripts.
- For advanced setups:
    - Use HashiCorp Vault, Azure Key Vault, or AWS Secrets Manager.
    - Mount secrets as environment variables or files.  
        Best practice: Rotate secrets periodically and restrict access per environment.

---

### 13. How do you set up environment-specific deployments (dev, staging, prod)?

Answer:  
Use environment variables and configuration files for each environment.  
Example structure:

```
values-dev.yaml
values-staging.yaml
values-prod.yaml
```

Then deploy with Helm:

```bash
helm upgrade app ./chart -f values-prod.yaml
```

In pipelines, use conditional logic:

```yaml
if: github.ref == 'refs/heads/main'
```

to deploy only to production.

---

### 14. Explain how you’d deploy a Dockerized app to Kubernetes using CI/CD.

Answer:

1. Build Docker image → tag → push to registry.
2. Pipeline updates `values.yaml` or `deployment.yaml` with new image tag.
3. ArgoCD or kubectl applies the changes to AKS cluster.
4. Run health checks post-deployment.  
    Tools: [[github actions]] (CI) + ArgoCD (CD) + Helm (packaging).

---

### 15. What is a Helm chart, and how is it used in CD?

Answer:  
A Helm chart is a package manager for Kubernetes  it defines templates and configurations for deploying apps.  
In CD, Helm is used to:

- Deploy consistent manifests
- Manage versioning and rollbacks
- Use variables per environment (`values.yaml`)  
    Example:

```bash
helm upgrade myapp ./helm-chart --set image.tag=v1.0.2
```

---

### 16. How can you roll back a failed deployment?

Answer:

- Helm: `helm rollback release-name <revision>`
- ArgoCD: Revert to a previous Git commit or use Argo’s rollback UI.
- Jenkins: Trigger a rollback pipeline with last stable build artifact.  
    Best practice: Keep old images and manifests versioned in your repo or registry.

---
### 17. How do you ensure zero-downtime deployment?

Answer:  
Use rolling updates, blue-green, or canary deployments.

- Rolling: Replace pods gradually.
- Blue-Green: Deploy new version alongside old; switch traffic after validation.
- Canary: Release to a subset of users before full rollout.  
    Kubernetes `deployment` controller handles rolling updates by default.

---
### 18. What are common security practices in CI/CD pipelines?

Answer:

- Store secrets securely (never in repo).
- Run static analysis (SAST) and dependency scans.
- Sign and verify build artifacts.
- Use least privilege for runners.
- Audit pipeline logs regularly.
- Restrict pipeline triggers (e.g., from trusted branches only).

---

### 19. How do you integrate security scans (e.g., Trivy, SonarQube, Snyk)?

Answer:  
Add a security stage in pipeline after build/test:

```yaml
- name: Security Scan
  run: trivy image myapp:${{ github.sha }}
```

- Trivy: Scans Docker images for vulnerabilities.
- SonarQube: Checks code quality and security hotspots.
- Snyk: Monitors open-source dependencies.  
    Fail pipeline if high-severity issues are found.

---

### 20. How do you handle credentials securely in CI/CD?

Answer:

- Use your CI tool’s secret management (encrypted vars).
- Limit who can view/edit secrets.
- Prefer short-lived tokens (OIDC with cloud providers).
- Rotate credentials periodically.
- Never log secrets in console outputs.  
    Example: GitHub → `${{ secrets.AZURE_CREDENTIALS }}` injected at runtime.

---
