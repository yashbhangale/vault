
# DMart Search - Architecture & End-to-End Flow

This document explains, in plain terms, how the DMart search system is built,
how a shopper's search reaches it, and how a developer changes the code and
ships those changes to AWS Lambda. Every step lists the AWS services involved.

The system is a grocery search service. Behind the scenes it uses OpenSearch
for retrieval (keyword + vector search), a machine-learning model for
re-ranking results, and several AWS services glued together with AWS CDK
(infrastructure as code).

---

## 1. The Big Picture (one paragraph)

A shopper types a query in a web UI. The UI calls an **API Gateway** URL.
API Gateway forwards the request to an **AWS Lambda** function. The Lambda runs
the search pipeline: it cleans up the query, turns it into a vector using a
**SageMaker** embedding model, asks **Amazon OpenSearch** for matching products
(keyword + vector "hybrid" search), re-ranks the results with a machine-learning
model (LTR / LambdaMART), formats the response, and sends it back. Supporting
data (synonyms, dictionaries, ML model artifacts) lives in **Amazon S3**. Secrets
(the API key) live in **AWS Secrets Manager**. Some Lambdas are packaged as
container images stored in **Amazon ECR**, and those images are built by **AWS
CodeBuild**. Long-running data/indexing jobs are orchestrated by **AWS Step
Functions** on schedules set by **Amazon EventBridge**. Everything is monitored
by **Amazon CloudWatch**.

```
                                          ┌─────────────────────────────────────────┐
                                          │              AWS Cloud                    │
  ┌──────────┐   HTTPS    ┌──────────────┐│   invoke    ┌──────────────────────────┐ │
  │  Shopper │──────────▶ │ API Gateway  │├───────────▶ │  Lambda: SearchFunction  │ │
  │  Browser │            │ (REST, /v1)  ││             │  (container image)       │ │
  │  (UI)    │◀────────── │              │├◀─────────── │                          │ │
  └──────────┘   JSON     └──────────────┘│   response  └─────────────┬────────────┘ │
                                          │                           │              │
                                          │        ┌──────────────────┼───────────┐  │
                                          │        ▼                  ▼           ▼  │
                                          │  ┌───────────┐    ┌─────────────┐ ┌────────────┐
                                          │  │ SageMaker │    │ OpenSearch  │ │  Bedrock   │
                                          │  │ (embed    │    │ (hybrid     │ │ (optional  │
                                          │  │  query)   │    │  BM25+kNN)  │ │  LLM steps)│
                                          │  └───────────┘    └─────────────┘ └────────────┘
                                          │        ▲                  ▲           ▲  │
                                          │        │   S3 (dictionaries, ML model) │  │
                                          │        └──────── Secrets Manager ──────┘  │
                                          └─────────────────────────────────────────┘
```

---

## 2. AWS Services Used (quick reference)

| Service | What it does here |
|---|---|
| **Amazon API Gateway** | Public HTTPS entry point. Two REST APIs: a Search API and a Suggest API, both on stage `v1`. |
| **AWS Lambda** | Runs all application code. Functions: search, suggest, home feed, health, and indexing functions. |
| **Amazon OpenSearch** | The search engine. Stores product documents and runs hybrid (keyword BM25 + vector kNN) queries. |
| **Amazon SageMaker** | Hosts the embedding model (Qwen) that turns text into vectors. Separate endpoints for query vs document embedding. |
| **Amazon Bedrock** | Optional LLM steps: category selection and query verification (Claude Haiku). Off by default for query verification. |
| **Amazon S3** | Stores dictionaries, synonyms, suggestion catalogs, and versioned artifacts. Bucket: `dmart-search-dictionaries`. |
| **AWS Secrets Manager** | Stores the API key (`X-Api-Key`) that protects the search/suggest endpoints. |
| **Amazon ECR** | Container image registry. Stores the Docker images for the container-based Lambdas (search, indexing). |
| **AWS CodeBuild** | Builds the Docker image from the `Dockerfile` and pushes it to ECR. |
| **AWS CDK / CloudFormation** | Infrastructure as code. Defines and deploys every AWS resource above. |
| **AWS Step Functions** | Orchestrates long, multi-hour indexing jobs (main index, category index). |
| **Amazon EventBridge** | Schedules recurring jobs (e.g. dictionary refresh, suggestion index rebuild). |
| **Amazon CloudWatch** | Logs and alarms for every Lambda function. |
| **AWS IAM** | Per-function roles that grant each Lambda only the permissions it needs. |

Deployment region is `ap-south-1` (Mumbai) and the AWS account referenced in
config is `234865294302`.

---

## 3. Project Layout (where things live)

```
dmart-search-aos-ltr-v2/
├── buildspec.yml                 # CodeBuild recipe: build Docker image -> push to ECR
├── README.md                     # this file
└── lambda_migration/
    ├── frontend/index.html       # the search UI (static HTML/CSS/JS single page app)
    ├── functions/                # one folder per Lambda function
    │   ├── search/               #   main search (container image, has Dockerfile)
    │   ├── suggest/              #   autocomplete / autosuggest (zip + layers)
    │   ├── home_feed/            #   home page feed (zip + layers)
    │   ├── health/               #   health check (zip + layers)
    │   ├── main_index/           #   product indexing job (container image)
    │   ├── category_index/       #   category profile indexing job (container image)
    │   ├── suggestion_index/     #   suggestion index rebuild job (container image)
    │   └── term_dictionary_refresh/  # dictionary refresh job (container image)
    ├── shared/                   # business logic reused across functions
    │   ├── search_pipeline/      #   query processing, hybrid query, synonyms, routing
    │   ├── postprocessing/       #   response formatting, variant grouping, intent tiers
    │   └── reranking/            #   LTR reranker + legacy RRF merger
    ├── layers/                   # Lambda Layers (shared code + vendored dependencies)
    ├── infrastructure/           # AWS CDK app (the "infrastructure as code")
    │   ├── app.py                #   wires all 7 stacks together
    │   ├── deploy_config.py      #   single source of truth for all config/env values
    │   └── stacks/               #   one file per CloudFormation stack
    ├── scripts/                  # helper scripts (build_layers.sh, S3 bootstrap, etc.)
    ├── workflows/                # Step Functions state machine definitions (.asl.json)
    ├── data/                     # source data (synonyms, dictionaries)
    └── docs/                     # architecture, API contracts, runbooks
```

---

## 4. How a Shopper Accesses the UI (runtime flow)

The UI (`lambda_migration/frontend/index.html`) is a single self-contained
HTML page. It holds one constant near the top:

```js
const API_BASE = 'https://o5fvjqt1ok.execute-api.ap-south-1.amazonaws.com/v1';
```

That URL is an **API Gateway** stage. When a shopper interacts with the page:

1. **Typing in the search box** fires an autocomplete call to
   `GET {API_BASE}/api/autocomplete?query=...&storeid=...` -> API Gateway ->
   **SuggestFunction** Lambda.
2. **Submitting a search** calls `POST {API_BASE}/api/search` (JSON body) ->
   API Gateway -> **SearchFunction** Lambda.
3. **Loading the home page** calls `GET {API_BASE}/api/home?storeId=...` ->
   API Gateway -> **HomeFeedFunction** Lambda.

> Note: the CDK code (see `api_stack.py`) defines the newer route shapes
> `GET /search`, `GET /autocomplete`, `GET /autosuggest`, `GET /home`, and
> `GET /health` on two separate REST APIs. The bundled `index.html` still points
> at the older `/api/*` routes on the currently deployed gateway. When you cut
> over to the CDK-managed APIs, update `API_BASE` (and the paths) in the UI.

### What happens inside SearchFunction (the search pipeline)

The order below mirrors `functions/search/service.py`:

1. **Process the query** - spell correction, tokenization, normalization.
2. **Route the query** - decide the relevant category (optionally using
   **Bedrock** Claude Haiku for category selection).
3. **Embed the query** - call the **SageMaker** query-embedding endpoint
   (`qwen-query-embedding-endpoint-v6`) to turn the text into a 1024-dim vector.
4. **Hybrid search** - build one native OpenSearch "hybrid" query (keyword BM25
   + vector kNN) and run it against **OpenSearch** using its search pipeline.
5. **Extract intent** from the query.
6. **LTR re-rank** - if `LTR_ENABLED` is on, re-score results with the
   LambdaMART model (LightGBM) baked into the container image.
7. **Intent-tier reorder**, **variant grouping** (group product variants under a
   parent), then **pagination**.
8. **Format the response** and return JSON to API Gateway, which returns it to
   the browser.

### Authentication

There is no gateway authorizer. Instead, **SearchFunction** and
**SuggestFunction** validate an `X-Api-Key` request header inside the handler,
comparing it (constant-time) against a key stored in **AWS Secrets Manager**
(secret `uat/dmart/api/auth`, field `uat-dmart-api-key`). `/search` enforces the
key by default (`ENFORCE_API_KEY=true`); `/autocomplete` and `/autosuggest`
always enforce it; `/home` and `/health` are open. The key is cached for 300
seconds to avoid a Secrets Manager call on every request.

---

## 5. How a Developer Makes Changes

There are two kinds of Lambda in this project, and they are changed and deployed
differently.

- **Zip-based Lambdas** (`suggest`, `home_feed`, `health`): plain Python. CDK
  zips the function folder plus its Lambda Layers and uploads it. No Docker.
- **Container-image Lambdas** (`search`, `main_index`, `category_index`,
  `suggestion_index`, `term_dictionary_refresh`): packaged as Docker images
  because they carry heavy dependencies (LightGBM, pandas, numpy) and, for
  search, the baked-in ML model. These images are built by CodeBuild and stored
  in ECR.

### Typical change loop

1. Edit code under `functions/<name>/` (function entry point) and/or
   `shared/` (reused logic). For example, the search ranking logic lives in
   `shared/search_pipeline/` and `shared/reranking/`.
2. Update config if needed in `infrastructure/deploy_config.py` (this is the
   single source of truth for endpoints, index names, feature flags, image URIs,
   etc. - all read from environment variables or CDK context with safe fake
   defaults).
3. Run tests in `lambda_migration/tests/`.
4. Rebuild layers, rebuild the image (if it is a container Lambda), and deploy
   with CDK. See the next two sections.

---

## 6. How Changes Deploy to AWS Lambda (CodeBuild + ECR + CDK)

The deployment has two halves that meet at ECR:

```
                    HALF A: build the container image
  ┌─────────────┐   docker build   ┌──────────────┐   docker push   ┌───────────┐
  │  Dockerfile │────────────────▶ │  CodeBuild   │───────────────▶ │    ECR    │
  │ (functions/ │  (buildspec.yml) │  project     │                 │ dmart-    │
  │  search/)   │                  │              │                 │ search-   │
  └─────────────┘                  └──────────────┘                 │ function  │
                                                                     └─────┬─────┘
                                                                           │ image URI
                    HALF B: deploy the infrastructure                      ▼
  ┌─────────────┐   cdk deploy    ┌──────────────┐   creates/updates ┌───────────┐
  │  CDK app    │───────────────▶ │ CloudFormation│───────────────▶ │  Lambda   │
  │ (app.py +   │                 │  stacks       │  (references     │ Function  │
  │  stacks/)   │                 │               │   ECR image URI) │           │
  └─────────────┘                 └──────────────┘                  └───────────┘
```

### Half A - Build the image with CodeBuild and push to ECR

The image build is intentionally **outside** CDK (the build environment has no
Docker daemon, and building a several-hundred-MB image on every deploy is slow).
A separate CodeBuild project runs `buildspec.yml` at the repo root. Its steps:

1. **pre_build**: log in to **ECR** with `aws ecr get-login-password`, then
   `cd lambda_migration`.
2. **build**: `docker build -f functions/search/Dockerfile -t dmart-search-function:latest .`
   The build context is the whole `lambda_migration/` folder so the Dockerfile
   can copy in `shared/` and `layers/shared-config-client/`. The image is based
   on `public.ecr.aws/lambda/python:3.12`, installs `libgomp` (needed by
   LightGBM), copies shared + function code, and bakes in the LTR model.
3. **post_build**: tag and `docker push` to
   `234865294302.dkr.ecr.ap-south-1.amazonaws.com/dmart-search-function:latest`.

> One-time prerequisite before building the search image: copy the LTR model
> artifacts and history CSVs into `functions/search/ltr_model` and
> `functions/search/ltr_history` (documented in the Dockerfile header). The same
> CodeBuild pattern builds `dmart-main-index` and `dmart-category-index` images.

**AWS services in Half A:** CodeBuild (runner), ECR (registry), IAM (CodeBuild's
role and ECR permissions).

### Half B - Deploy infrastructure with CDK

CDK reads the pushed image by its **ECR URI** (from
`deploy_config.search_function_image_uri`) and wires everything together.

Prerequisite step (do this before every synth/deploy): build the Lambda Layers.

```bash
cd lambda_migration
bash scripts/build_layers.sh      # vendors deps into layers/*/python/
```

`build_layers.sh` packages three layers - `shared-config-client`,
`nlp-utilities`, `response-formatting` - and vendors their pip dependencies for
the Lambda Python 3.12 runtime (manylinux_2_28, x86_64) so CDK does not need
Docker to build them.

Then synth/deploy the CDK app:

```bash
cd lambda_migration/infrastructure
cdk synth      # produces the CloudFormation template (safe, creates nothing)
cdk deploy      # creates/updates real AWS resources
```

`app.py` instantiates 7 stacks in dependency order:

1. **StateStack** - the S3 dictionary/state bucket.
2. **LayerStack** - the three Lambda Layers.
3. **SecurityStack** - one IAM role per function (least privilege: only the
   OpenSearch domain, SageMaker endpoint, Bedrock model, S3 keys, and Secrets
   Manager secret each function actually needs).
4. **LambdaStack** - the runtime Lambdas: `SearchFunction` (from the ECR image),
   plus `SuggestFunction`, `HomeFeedFunction`, `HealthCheckFunction` (zip +
   layers). This is where each function's memory, timeout, and environment
   variables are set. `SearchFunction` uses `DockerImageCode.from_ecr(...)`,
   which is how a code change reaches Lambda: CodeBuild pushes a new image tag,
   and `cdk deploy` points the function at it.
5. **ApiStack** - the two API Gateway REST APIs (Search API and Suggest API) and
   their routes; outputs the base URLs.
6. **MonitoringStack** - CloudWatch alarms for each function.
7. **IndexingStack** - the indexing Lambdas + Step Functions state machines +
   EventBridge schedules. These are only created when their ECR image URIs are
   configured, so the runtime path can deploy independently of the data pipeline.

**AWS services in Half B:** CDK/CloudFormation, Lambda, API Gateway, ECR (image
reference), S3, IAM, CloudWatch, Step Functions, EventBridge.

### End-to-end: from code edit to live

```
edit code (functions/ or shared/)
        │
        ├── zip Lambda?  ── cdk deploy ─────────────────▶ Lambda updated
        │
        └── container Lambda?
                 │
                 ▼
        CodeBuild runs buildspec.yml
                 │  docker build + push
                 ▼
        new image in ECR (:latest or a tag)
                 │
                 ▼
        cdk deploy  (LambdaStack references the ECR image URI)
                 │
                 ▼
        Lambda now runs the new image  ── API Gateway routes traffic to it
```

---

## 7. Background / Indexing Flow (how data gets into OpenSearch)

Search only works because products are indexed in OpenSearch first. That is a
separate, offline path:

- **MainIndexFunction** / **CategoryIndexFunction** (container Lambdas) read
  source data, embed documents using the **SageMaker** document-embedding
  endpoint, and write documents into **OpenSearch** indexes.
- These run under **Step Functions** state machines (defined in `workflows/`)
  because indexing can take hours; Step Functions handles the batching and
  long-running orchestration.
- **EventBridge** schedules recurring jobs, such as the term-dictionary refresh
  and the suggestion-index rebuild (default every 7 days).
- Source data and generated artifacts live in **S3**.

**AWS services in this flow:** Lambda, Step Functions, EventBridge, SageMaker,
OpenSearch, S3, IAM, CloudWatch.

---

## 8. Configuration & Feature Flags (at a glance)

All configuration is centralized in `infrastructure/deploy_config.py` and passed
to Lambdas as environment variables. Set values via environment variables or CDK
context (`cdk deploy -c key=value`). Key ones:

| Setting | Purpose | Default |
|---|---|---|
| `OPENSEARCH_HOST` / `OPENSEARCH_DOMAIN_NAME` | OpenSearch endpoint & domain | `oneture-search-dev` |
| `PRODUCT_INDEX_NAME` | main product index | `dmart_products_3stores_cathier_qwen1024_v2` |
| `QUERY_EMBEDDING_ENDPOINT` | SageMaker query embed endpoint | `qwen-query-embedding-endpoint-v6` |
| `DOCUMENT_EMBEDDING_ENDPOINT` | SageMaker document embed endpoint | `qwen-query-embedding-endpoint-v5` |
| `DICTIONARY_BUCKET_NAME` | S3 bucket for dictionaries | `dmart-search-dictionaries` |
| `LTR_ENABLED` | turn LTR re-ranking on/off | `true` |
| `LLM_CATEGORY_SELECT_ENABLED` | use Bedrock for category routing | `true` |
| `ENABLE_LLM_QUERY_PROCESSING` | use Bedrock for query verification | `false` |
| `ENFORCE_API_KEY` | require `X-Api-Key` on `/search` | `true` |
| `API_SECRET_NAME` | Secrets Manager secret holding the API key | `uat/dmart/api/auth` |
| `SEARCH_FUNCTION_IMAGE_URI` | ECR image the Lambda runs | `...ecr.../dmart-search-function:latest` |

---

## 9. Quick Start (deploy from scratch)

```bash
# 0. Prereqs: AWS credentials for account 234865294302 / region ap-south-1,
#    Docker (for the image build), Python + AWS CDK installed.

# 1. Build & push the search container image (via CodeBuild, or locally):
#    - copy LTR model artifacts into functions/search/ltr_model (see Dockerfile)
#    - CodeBuild runs buildspec.yml -> pushes to ECR

# 2. Build the Lambda Layers:
cd lambda_migration
bash scripts/build_layers.sh

# 3. Deploy the infrastructure:
cd infrastructure
cdk synth
cdk deploy --all

# 4. Grab the API base URL from the cdk deploy output (SearchApiBaseUrl /
#    SuggestApiBaseUrl), update frontend/index.html's API_BASE, and open the UI.
```

For deeper details see `lambda_migration/docs/` (architecture, API contracts,
deployment runbook, rollback runbook) and the docstrings at the top of each
file in `lambda_migration/infrastructure/stacks/`.