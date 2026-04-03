---
title: Trying things locally
---
Bilkul, chalo bilkul **zero se step‑by‑step** karte hain, is assumption ke saath:
	
- Tumhare paas abhi **sirf `fast_prod_new.py` + `Dockerfile` + `requirements.txt`** hain  
- **Koi model weights folder (e.g. `full_14_08_2025_ch_28k`) nahi hai**  
- Goal: **SageMaker ka flow samajhna** (learning), chahe model actual mein run na bhi kare

Isliye niche 2 cheezein samjho:

- **“Model code”** = `fast_prod_new.py` (ye likha hua logic)  
- **“Model weights/data”** = actual trained parameters ka folder (jo `MODEL_PATH` se load hota hai) – ye abhi tumhare paas nahi hai  

Learning ke liye tum **infra pipeline** samajh sakte ho **bina real weights ke bhi**. Endpoint aayega, `/` ya `/health` call kar paoge; agar load_model fail karega to error dikhega, par flow samajh aa jayega.

Neeche **sab kuch simple Hinglish + numbered steps** mein hai.

---

## STEP 0 – Mental model samjho (very important)

1. **Local world**  
   - Tum `uvicorn fast_prod_new:app --port 8001` chala ke FastAPI app run karte ho (agar model weights hote).
2. **Container world (Docker)**  
   - Wahi app ek **Docker image** mein band hota hai (tumhari `Dockerfile` se).
3. **SageMaker world**  
   - SageMaker **ECR se image** leta hai  
   - Optionally **S3 se model data** leta hai  
   - Fir usse ek **Endpoint** banata hai jisko tum API ki tarah call kar sakte ho.

Abhi tum **sirf Step 2 + 3** (Docker + SageMaker) seekhna chahte ho – totally fine.

---

## STEP 1 – Local pe Docker image build karo

Prerequisite:

- Docker install hai  
- AWS CLI install hai (baad mein use karenge)

Project folder mein jao jahan `Dockerfile` hai:

```bash
cd /home/yash/Desktop/office/Xpressbees

# Docker build
docker build -t xb-internvl-demo .
```

Agar ye **success** ho gaya, matlab tumhara app Docker ke andar run ho sakta hai (theoretically).

Optional test (agar model na hone ki wajah se crash bhi kare, koi problem nahi, hum infra hi seekh rahe hain):

```bash
docker run -p 8001:8001 xb-internvl-demo
```

Browser/postman: `http://localhost:8001/` hit karke dekh lo agar kuch response aata hai (agar model path missing hai to error aayega – acceptable for now).

---

## STEP 2 – AWS account basic setup

1. AWS Console open karo  
2. **Region select karo** – e.g. `ap-south-1 (Mumbai)`  
3. Local terminal pe:

```bash
aws configure
# AWS Access Key, Secret, region (e.g. ap-south-1), output (json)
```

4. Region aur account id note karo:

```bash
export AWS_REGION=ap-south-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
```

---

## STEP 3 – ECR repo banao (image store karne ke liye)

1. Terminal:

```bash
aws ecr create-repository \
  --repository-name xb-internvl-demo \
  --region ${AWS_REGION}
```

2. **ECR login:**

```bash
aws ecr get-login-password --region ${AWS_REGION} \
| docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
```

3. **Local image ko tag + push karo:**

```bash
docker tag xb-internvl-demo:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/xb-internvl-demo:latest

docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/xb-internvl-demo:latest
```

Ab tumhare paas **ECR image URI** hai, kuch aisa:

`123456789012.dkr.ecr.ap-south-1.amazonaws.com/xb-internvl-demo:latest`

Ye SageMaker ko dena hai.

---

## STEP 4 – IAM role (SageMaker ko permissions dena)

1. Console → **IAM → Roles → Create role**  
2. Trusted entity: **SageMaker**  
3. Permissions:
   - Learning ke liye simple: **AmazonSageMakerFullAccess** (production mein strict karna hota hai)
4. Role ka naam: `sagemaker-demo-role`  
5. Role ARN copy karo (something like `arn:aws:iam::123456789012:role/sagemaker-demo-role`)

---

## STEP 5 – SageMaker Model create karo (without model data, learning-only)

Yahan 2 options hote:

- **Real model** ho to S3 `ModelDataUrl` dete  
- Tumhare paas **abhi koi model folder nahi**, to learning ke liye hum **sirf Docker image** de denge, ModelDataUrl blank chalta hai (provided container khud handle kar le).

For now, hum **ModelDataUrl skip** karenge, sirf image denge (endpoint shayad load_model par error kare, but infra flow samajh aa jayega).

### 5.1 Console se

1. AWS Console → **SageMaker → Inference → Models → Create model**  
2. **Model name:** `internvl-demo-model`  
3. **Execution role:** `sagemaker-demo-role`  
4. **Container definition:**
   - Container input options → “Provide model container and inference image”
   - Image URI: `…ecr….amazonaws.com/xb-internvl-demo:latest`
   - **Model data URL:** EMPTY chhodo (learning ke liye)
   - Environment variables:
     - `MODEL_PATH=/app/model` (ya jo tum use karna chaho; abhi model nahi hai to yeh bhi optional hai)

5. Create karo.

---

## STEP 6 – Endpoint configuration

1. SageMaker Console → **Inference → Endpoint configurations → Create**  
2. **Name:** `internvl-demo-ep-config`  
3. **Production variants → Add model**:
   - Model: `internvl-demo-model`
   - Variant name: `AllTraffic`
   - Initial instance count: `1`
   - Instance type: `ml.g4dn.xlarge` (GPU T4, demo ke liye theek)  
4. Create.

---

## STEP 7 – Endpoint create karo

1. SageMaker Console → **Inference → Endpoints → Create endpoint**  
2. **Endpoint name:** `internvl-demo-ep`  
3. Endpoint config: `internvl-demo-ep-config`  
4. Create.  
5. Status “**InService**” hone tak wait karo (5–10 min).

Is time pe SageMaker tumhara ECR image pull karega, container run karega, aur tumhara `fast_prod_new.py` inside container execute hoga.

Agar model path/weights nahi mil rahe, endpoint health fail bhi ho sakta hai – but tumne **pure pipeline** kar liya (ECR → Model → Endpoint).

---

## STEP 8 – Test call (agar endpoint healthy ho)

Agar endpoint “InService” hai, try:

```bash
aws sagemaker-runtime invoke-endpoint \
  --endpoint-name internvl-demo-ep \
  --content-type application/json \
  --body '{"ping": "test"}' \
  output.json \
  --region ${AWS_REGION}
```

- Agar tumne app mein `/invocations` properly nahi banaya, to yahan se error aayega – ye bhi learning ka part hai.
- Tum dhire‑dhire `/ping` aur `/invocations` routes add kar sakte ho jaise maine pehle explain kiya (FastAPI mein simple endpoints).

---

## STEP 9 – Cost control (bahut important)

- Demo khatam ho jaaye → **Endpoint delete** karo:  
  - SageMaker → Endpoints → `internvl-demo-ep` → Delete  
- Endpoint chal raha hai tabhi charge lagta hai. ECR + logs + thoda S3 storage = negligible.

---

## Tumhara special case – “sirf ek python file he, no model”

Iska matlab:

- **Infra flow** (Docker → ECR → SageMaker Model → Endpoint) tum **aaj hi** complete kar sakte ho.
- **Real inference** tabhi chalegi jab:
  - Ya to tum `MODEL_PATH` pe actual model folder download karao (HuggingFace se, ya trained model se)  
  - Ya phir learning ke liye `load_model()` ko temporarily dummy bana do (e.g. kuch simple “Hello from model” return kare), taaki endpoint healthy dikh sake.

Main file edit nahi kar sakta (Ask mode), lekin agar tum chaho to main tumhe **exact dummy code snippet** dikha sakta hoon jo tum `fast_prod_new.py` mein manually paste karke real model ke jagah use kar sakte ho, sirf learning ke liye.

Agar next message mein bolo “haan dummy version ka code dikha”, to main sirf **code snippet + kaha insert karna hai** explain kar dunga.