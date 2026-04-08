---
title: Code walkthrough fast_prod_new_py
---

## 1. What the service does (business + tech)

- Business: Reverse-pickup inspection: compare vendor reference images (S3/CloudFront) with pickup/return images (base64 or URLs), answer vendor-defined verification questions, and output Pick / Not Pick with evidence and confidence.

- Tech: FastAPI app that loads InternVL v2.5 1B (vision–language), runs inference on GPU, validates output against a JSON schema, optionally retries once, and saves requests/results to a DB. No image/output caching.

From the Readme: target is ~20K images/day, 14–17s response, peak concurrency 15, 6:00–24:00 uptime, and eventually SageMaker + MLOps (scale, CI/CD, monitoring).

---

## 2. High-level architecture

Client → POST /process_request (RequestItem)

    → Validate request (Pydantic)
    → [Optional] Use prefetched images from pipeline
    → Else: download vendor images (async) + decode pickup images
    → Preprocess to tensors (dynamic_preprocess, load_image)
    → Parse "question" JSON → build prompt (generate_question_template)
    → run_model_inference (InternVL chat)
    → extract_json + validate_json_schema
    → [If invalid] Retry once with enhanced prompt
    → Map recommendation (Accept→Pick, Reject/Partial/Retry→Not Pick)
    → Match question labels (fuzzy), build Question2, analysis
    → Return ProcessingResponse immediately
    → Background: save to DB (rvpxbverification_request_data, rvpxbverification, rvpxbverification_fail)

So the code is a single FastAPI process (one worker) with:

- Prefetch pipeline: background workers pull from a queue, download/decode images, turn them into tensors, and put results in processed_queue so the main request can sometimes skip I/O and preprocessing.

- Concurrency: semaphore MAX_CONCURRENT_REQUESTS (default 10), thread pools for CPU-bound work (image decode, preprocessing).

- DB: sql_conn used only for inserts (request payload, result, and failure records).

---

## 3. Configuration (Config class, ~lines 63–97)

- Model: MODEL_PATH = "full_14_08_2025_ch_28k" (local dir; no HuggingFace ID in code).
- Server: HOST, PORT (default 8001), LOG_LEVEL, CORS_ORIGINS, TRUSTED_HOSTS.
- Limits: MAX_IMAGE_SIZE (10MB), REQUEST_TIMEOUT (300s), MAX_IMAGES_PER_REQUEST (20), MAX_CONCURRENT_REQUESTS (10).
- Image: IMAGE_SIZE (448), PICKUP_PATCH (2), generation_config (e.g. max_new_tokens 2000, no sampling).
- Performance: THREAD_POOL_SIZE, PREFETCH_WORKERS, PREFETCH_FACTOR, PIPELINE_QUEUE_SIZE, IMAGE_DOWNLOAD_TIMEOUT, USE_MIXED_PRECISION.

For SageMaker you’ll typically drive these via environment variables (and keep MODEL_PATH pointing to the artifact SageMaker provides).

---

## 4. Request and response contracts

Request (RequestItem, ~445–598)

- pickupproductimage: list of URLs (vendor reference images), 1–10.

- skupickdone: list of base64 strings or HTTPS URLs (pickup/return images), 1–10.

- productname, question, shippingid (required).

- Optional: productid, uuid, previousuuid.

- Validators enforce URL/image format and lengths.

Response (ProcessingResponse, ~600–612)

- shippingid, uuid, product_id, processing_time_ai, Question (list of per-question answers), ai_decision (e.g. "Pick"/"Not Pick"), finalAction, ai_match_score, analysis, status, StatusCode, total_time, timestamp.

So for SageMaker you’ll expose an endpoint that accepts this JSON body and returns this shape (or wrap it in SageMaker’s request/response envelope if you use the default inference format).

---

## 5. JSON schema and validation (~99–219, 212–221)

RESPONSE_SCHEMA defines the expected model output:

- image_analysis: pickup_images, vendor_image, comparison (strings).

- verification_results: array of objects with Type, Label, IsMandatory, ValueToCheck, Result, Evidence, Confidence, isRetakeImage.

- pickup_confidence: overall_score, confidence_factors (image_quality, attribute_visibility, matching_confidence), recommendation (Accept/Reject/Partial/Retry).

validate_json_schema(data) runs jsonschema validation. If it fails, the code retries inference once with an extra instruction to fix confidence types and structure.

---

## 6. Model loading and inference

- Load (load_model, ~1137–1300):

- AutoModel.from_pretrained(MODEL_PATH, torch_dtype=torch.bfloat16, attn_implementation="flash_attention_2", ...) and AutoTokenizer.from_pretrained(MODEL_PATH).

- Model is .eval().cuda(), then torch.compile(..., mode="reduce-overhead").

- Requires CUDA; on failure sets model_state.load_error and raises ProcessingError.

- Inference (run_model_inference, ~1355–1372):

- model_state.model.chat(tokenizer, pixel_values, questions, num_patches_list=num_patches, generation_config=..., history=None) under torch.inference_mode() and a dedicated CUDA stream, then torch.cuda.synchronize().

For SageMaker you’ll load the same way inside the container, with MODEL_PATH set to the path where the model artifact is extracted (e.g. /opt/ml/model or a subfolder).

---

## 7. Image pipeline (vendor vs pickup)

- Vendor images: URLs in pickupproductimage.

- rewrite_s3_to_cloudfront replaces xbeestest.s3.amazonaws.com with a CloudFront domain.

- download_image_async (aiohttp) downloads and opens as PIL RGB; enforces MAX_IMAGE_SIZE.

- Pickup images: in skupickdone — either base64 or https:// URLs.

- decode_base64_image_batch: if URL, fetches (with retry); else base64-decode; same size limit.

- Preprocessing:

- build_transform (resize to input_size, normalize ImageNet stats).

- dynamic_preprocess splits by aspect ratio into patches (e.g. 1–12 patches).

- load_image(image_file, input_size, max_num) returns a tensor; vendor uses max_num=1, pickup uses config.PICKUP_PATCH (2).

Prefetch workers do the same download/decode/load in a thread pool and put PrefetchedData (vendor/pickup tensors + metadata) in processed_queue.

---

## 8. Question and prompt flow

- Input: request.question is a JSON string. process_verification_data parses it and extracts a list of questions (e.g. data['Question']), with fields like Type, Label, ValueToCheck, etc.

- Prompt: generate_question_template(vendor_img_count, sr_images_count, productname, question_data) builds the text prompt and injects a structured JSON template (fix_verification_questions adjusts Result/Evidence instructions per question type and labels). The template describes vendor vs pickup image indices and the required output format.

- Output parsing: extract_json(responses) (regex/pyaml/json/ast) turns the model text into a dict; then validate_json_schema(result) checks it. On failure, one retry with an “IMPORTANT: … validation errors …” suffix.

---

## 9. Main processing and response (process_request_with_prefetch, ~1417–1833)

- Acquires semaphore, then tries to get prefetched data (short timeout).

- If none: downloads vendor images, decodes pickup images, builds tensors, and may submit the request for prefetch for future calls.

- Builds img_tensors, num_patches, questions, pixel_values; runs run_model_inference; extracts and validates JSON; optionally retries once.

- Maps pickup_confidence.recommendation to ai_decision (Pick/Not Pick) and StatusCode (200 vs 202).

- Aligns model verification_results to input question labels (including fuzzy match via find_most_similar_string), fills missed questions with defaults, then builds Question2 (with answer, ValueToCheck, isRetakeImage, etc.).

- Builds response_dict and returns it.

- Background tasks:

- Save request to rvpxbverification_request_data.

- Save success/fail payload to rvpxbverification or rvpxbverification_fail (including first/second inference and validation status).

So the “ML” part is: download/decode → preprocess → one (or two) inference(s) → validate → business logic (recommendation + label matching) → response + DB.

---

## 10. Database usage

- sql_conn (imported as conn):

- conn.insert_single_dict_simple(data_dict, table_name, drop_if_exists=True) for rvpxbverification_fail.

- conn.insert_single_dict_simple(data_dict, table_name) for rvpxbverification_request_data and rvpxbverification.

- conn.create_table_from_dict(data_dict, table_name) in save_to_database_error.

The project only references sql_conn; the actual module is not in the repo. For SageMaker you’ll need to either bundle it or replace it with a client that works in the container (e.g. RDS, Redshift, or another DB with proper networking from the SageMaker VPC).

---

## 11. API surface

- GET /

- Service name, version, feature flags, max_concurrent_requests, prefetch_workers, caching_enabled: false.

- GET /health

- Model loaded, CUDA, GPU memory, semaphore “current active”, prefetch pipeline status (running, workers, queue sizes). Used by load balancers/ SageMaker for health checks.

- POST /process_request

- Body: RequestItem. Returns ProcessingResponse. All core logic runs here (via process_request_with_prefetch).

- GET /metrics

- Concurrency, prefetch queue sizes, performance flags. Useful for monitoring and autoscaling.

- Exception handlers

- ProcessingError, HTTPException, and generic Exception return a consistent { "errorMsg", "code", "processingTime", "previousuuid" } style.

---

## 12. Lifespan and entrypoint (~1324–1352, 2045–2057)

- Startup: load_model() then model_state.start_prefetch_pipeline() (starts prefetch workers).

- Shutdown: stop prefetch pipeline, close aiohttp session, shutdown thread pools, delete model/tokenizer, torch.cuda.empty_cache().

- Run: uvicorn.run(app, host=..., port=..., workers=1) — single worker so the same process holds the GPU model.

For SageMaker you’ll run the same app in the container (e.g. uvicorn or gunicorn with 1 worker) and let SageMaker send HTTP requests to /process_request (or to a custom path you wire in the container).

---

## 13. What you need for AWS SageMaker deployment

- Container:

- Base image with CUDA, PyTorch, transformers, and dependencies (fastapi, uvicorn, aiohttp, PIL, pyaml, jsonschema, fuzzywuzzy, pandas, etc.).

- Copy fast_prod_new.py and sql_conn (or replacement).

- Set MODEL_PATH to the SageMaker model artifact path (e.g. /opt/ml/model).

- Serve the FastAPI app (e.g. CMD ["uvicorn", "fast_prod_new:app", "--host", "0.0.0.0", "--port", "8000"]).

- Implement SageMaker’s invocation contract in the container: read request body from stdin or HTTP (depending on mode), call your existing logic (e.g. build RequestItem from the body, call process_request_with_prefetch), write response to stdout or HTTP. Alternatively, use a SageMaker custom container that just runs your FastAPI server and use “multi-model” or “bring your own container” and call POST /process_request from the client.

- Model artifact:

- Upload full_14_08_2025_ch_28k (or the same weights in the format the code expects) to S3 and register it as a SageMaker model; the container reads from the path SageMaker provides.

- Instance:

- GPU instance (e.g. g5/g6) to match current G6.2x Large usage; multi-instance + autoscaling for “peak concurrency 15” and queueing.

- DB and networking:

- Run the container in a VPC that can reach your DB (or use RDS/Redshift and adapt sql_conn to that). Ensure S3/CloudFront and any external URLs used for images are reachable (no need to change rewrite_s3_to_cloudfront unless domain changes).

- Env and config:

- Pass all Config overrides (concurrency, timeouts, model path, etc.) via environment variables in the SageMaker model/endpoint configuration.

- CI/CD and MLOps:

- Use SageMaker Pipelines or CodePipeline to build the container, run tests, and deploy to dev/prod endpoints; use SageMaker Model Monitor for drift/infra and your own metrics (e.g. from /metrics and DB) for “inspections done” and performance.

If you tell me your next step (e.g. “container Dockerfile”, “SageMaker invocation handler”, or “replace sql_conn with RDS”), I can outline the exact code changes and file layout next (still in Ask mode — no edits, only guidance).