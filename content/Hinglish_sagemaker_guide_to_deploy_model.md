
Tumhara app **FastAPI + InternVL (GPU)** wala hai, isliye SageMaker pe deploy karne ke liye MLOps POV se yeh cheezen karna padengi.

---

# SageMaker pe deploy karne ke liye (MLOps POV)

## 1. **Deployment type choose karo**

- **Real-time endpoint** – synchronous, client wait karega; tumhara inference 1–2 min bhi ho sakta hai, isliye timeout (e.g. 5 min) aur heavy instance (GPU) chahiye.
- **Asynchronous inference** – request submit karo, response baad mein S3/callback se lo; long-running ke liye better, MLOps thoda zyada (S3 input/output, optional SNS).
- **Serverless inference** – cold start + GPU support limited; is stack ke liye usually real-time ya async better.

**Practical:** Pehle **Real-time GPU endpoint** se start karo; agar timeout/latency issue aaye to **Async inference** pe shift karo.

---

## 2. **Container – “Bring Your Own Container” (BYOC)**

Tumhara existing **Dockerfile** use ho sakta hai, bas SageMaker ke contract ke hisaab se thoda adapt karna padega.

**SageMaker real-time container contract:**

- **GET /ping** – 200 OK (health).
- **POST /invocations** – request body yahan aata hai; response yahi se return hota hai.

Tumhare paas abhi **POST /process_request** hai. Do options:

- **Option A (recommended):** Container same FastAPI chalaye, aur **extra routes** add karo:
  - `GET /ping` → `return {"status": "ok"}` (ya existing health logic).
  - `POST /invocations` → body ko tumhare `RequestItem` format mein map karke andar wahi logic call karo jo abhi `/process_request` mein hai; response same structure return karo.
- **Option B:** Alag adapter script jo SageMaker’s `/invocations` receive kare aur internally FastAPI client se `/process_request` hit kare (extra hop, usually need nahi).

**Container env:**

- **MODEL_PATH** – SageMaker model artifact mount karta hai **/opt/ml/model** pe. Isliye SageMaker Model create karte waqt **Environment: MODEL_PATH=/opt/ml/model** set karna.
- Baaki (HOST, PORT, LOG_LEVEL, DB-related env) bhi SageMaker Model/Endpoint **Environment** se pass kar sakte ho.

---

## 3. **Model artifact – S3**

- **full_14_08_2025_ch_28k** (jo abhi local/volume pe hai) ko **tar/compressed** karke **S3 bucket** mein upload karo.
  - e.g. `model.tar.gz` → `s3://your-bucket/models/internvl/full_14_08_2025_ch_28k/model.tar.gz`
- SageMaker **Model** create karte waqt **ModelDataUrl** yehi S3 path hoga.
- Container start pe SageMaker isko **/opt/ml/model** pe extract karke mount karta hai; tum `MODEL_PATH=/opt/ml/model` se use karoge.

**MLOps:** Model versioning ke liye S3 path mein version/date daal do, e.g. `.../v1.0/...` ya `.../20250814/...`.

---

## 4. **SageMaker resources – step-by-step**

| Step | Kya karna hai |
|------|----------------|
| 1. **ECR** | Docker image build karo (same Dockerfile), tag karo, ECR repository create karke push karo. |
| 2. **S3** | Model folder → `model.tar.gz` → S3 upload. |
| 3. **IAM** | SageMaker execution role: ECR read, S3 read (model bucket), CloudWatch logs, agar DB/Secrets chahiye to VPC/Secrets Manager access. |
| 4. **SageMaker Model** | Image = ECR image URI, ModelDataUrl = S3 model path, Environment = { MODEL_PATH=/opt/ml/model, ... }. |
| 5. **Endpoint config** | Instance type = GPU (e.g. **ml.g5.xlarge** / **ml.g4dn.xlarge**), instance count (1 se start). |
| 6. **Endpoint** | Model + Endpoint config use karke endpoint create karo. |

Invoke call pe SageMaker endpoint URL pe **POST /invocations** hit hoga (tum adapter se isko `/process_request` logic se connect karoge).

---

## 5. **MLOps checklist – kya kya karna hoga**

- **CI/CD**
  - Code + Dockerfile change → build image → push ECR → SageMaker **Model** naya version create (naya image URI / model URI).
  - Endpoint **update** (new endpoint config) ya blue/green style new endpoint + traffic shift.
- **Config**
  - Env (MODEL_PATH, DB, timeouts, etc.) SageMaker Model/Endpoint env se; secrets **Secrets Manager** se read (code mein env var se).
- **Monitoring**
  - CloudWatch: invocations, model latency, 4xx/5xx; optional **SageMaker Model Monitoring** (data drift) baad mein.
- **Security**
  - Endpoint IAM role minimal (sirf required S3/ECR/CloudWatch); production ke liye VPC + private subnet + security group; DB agar same VPC mein to private access.
- **Scaling**
  - Real-time: endpoint config mein instance count 2+ ya **auto-scaling** (invocations/custom metric).
  - Async: same scaling + S3 input/output design.
- **Versioning**
  - Model S3 path versioned; image tag = git tag / build id; SageMaker Model name mein version (e.g. `internvl-v1-0`).

---

## 6. **Tumhare code se direct link**

- **sql_conn** – production mein DB credentials SageMaker env / Secrets Manager se aane chahiye; container ko network/SG dena padega jahan DB hai (e.g. VPC).
- **Request timeout** – tumhare app mein 300s hai; SageMaker endpoint **invocation timeout** bhi at least itna (e.g. 300s) set karna.
- **Heavy GPU** – InternVL + 2000 tokens ke liye **ml.g5.xlarge** (ya bada) better; cost vs latency trade-off.

---

## 7. **Short “to-do” list (MLOps POV)**

1. **Container:** Dockerfile same; add **/ping** and **/invocations** (adapter) so that SageMaker contract satisfy ho.
2. **Model:** Bundle model → S3 upload → versioned path.
3. **IAM:** SageMaker role with ECR, S3, CloudWatch (and VPC/Secrets if needed).
4. **SageMaker:** Model (ECR + S3 + env) → Endpoint config (GPU instance) → Endpoint create.
5. **CI/CD:** Build → ECR push → Model/Endpoint update (script ya pipeline).
6. **Ops:** Monitoring (CloudWatch), timeout/config, scaling, secrets.

Agar tum bata do ki abhi **Real-time** pe jaana hai ya **Async**, to us hisaab se **/invocations** adapter ka exact request/response format (SageMaker style) bhi step-by-step likh sakta hoon (code structure, no file edit – Ask mode mein).