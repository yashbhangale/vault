---
title: Hinglish_Code_walkthrough_fast_prod_new_py
---


# **fast_prod_new.py – Poora Code Hinglish Mein**

## **1. Service Kya Karta Hai (Overview)**

Ye ek **FastAPI service** hai jo **InternVL v2.5 1B** vision model use karke **reverse pickup verification** karta hai:

- **Vendor images** (product listing) aur **pickup images** (customer return) dono analyze karta hai  
- In dono ko compare karke batata hai: product match ho raha hai ya nahi, damage hai ya nahi, quantity/size/color sahi hai ya nahi  
- Response **structured JSON** mein aata hai (image_analysis, verification_results, pickup_confidence)  
- **Caching band** hai – har request fresh process hoti hai  
- Inference ke baad **turant response** bhejta hai, DB save **background** mein hota hai  

---

## **2. Imports & Setup**

- **sql_conn** – DB insert (e.g. `conn.insert_single_dict_simple`, `conn.create_table_from_dict`)  
- **asyncio, aiohttp** – async image download, prefetch workers  
- **FastAPI, Pydantic** – API, request/response models, validation  
- **torch, transformers** – model load, inference  
- **PIL, torchvision** – image resize, normalize, tensor banana  
- **jsonschema, fuzzywuzzy, pyaml, ast** – response validate karna, JSON/YAML parse, string matching  

---

## **3. Error Codes (Lines 49–60)**

`ErrorCodes` class mein sab jagah same code **1099** use ho raha hai (general/validation/image/model/timeout/etc.). Error **type** alag hai, **numeric code** same hai.

---

## **4. Config (Lines 63–96)**

- **MODEL_PATH** – `"full_14_08_2025_ch_28k"` (InternVL model folder)  
- **HOST/PORT** – `0.0.0.0:8001` (env se override)  
- **MAX_IMAGE_SIZE** – 10MB  
- **REQUEST_TIMEOUT** – 300s  
- **MAX_CONCURRENT_REQUESTS** – 10 (kitne requests ek saath inference kar sakte hain)  
- **IMAGE_SIZE** – 448 (preprocess size)  
- **PICKUP_PATCH** – 2 (pickup images ke liye patch count)  
- **generation_config** – max_new_tokens 2000, do_sample False  
- **MAX_IMAGES_PER_REQUEST** – 20  
- **THREAD_POOL_SIZE** – 16  
- **PREFETCH_FACTOR / PREFETCH_WORKERS / PIPELINE_QUEUE_SIZE** – prefetch pipeline ke liye (1, 2, 5)  
- Caching related config **remove** kar diya gaya hai  

---

## **5. JSON Schema (Lines 99–199)**

Response ka **exact structure** define hai:

- **image_analysis** – pickup_images, vendor_image, comparison (strings)  
- **verification_results** – array of objects: Type, Label, IsMandatory, ValueToCheck, Result, Evidence, Confidence, isRetakeImage  
- **pickup_confidence** – overall_score, confidence_factors (image_quality, attribute_visibility, matching_confidence), recommendation (Accept/Reject/Partial/Retry)  

`validate_json_schema()` isi schema se model output validate karta hai; fail hone par "Fail inference" return hota hai.

---

## **6. Logging (200–209)**

- Level = Config se (default INFO)  
- Logs console + `internvl_api.log` dono pe jaate hain  

---

## **7. Validation & Exception (211–239)**

- **validate_json_schema(data)** – jsonschema se validate, True/False + error message  
- **ProcessingError** – custom exception: message, error_code, status_code, request_uuid, processing_time  
- **create_error_response()** – standard error dict: errorMsg, code, processingTime, previousuuid  

---

## **8. Prefetching – PrefetchedData (243–254)**

`PrefetchedData` dataclass:

- request_id  
- vendor_images, pickup_images (PIL)  
- vendor_tensors, pickup_tensors (model input)  
- metadata, timestamp, processing_time  

Ye woh cheez hai jo **prefetch worker** prepare karke **processed_queue** mein daalta hai.

---

## **9. ModelState (258–328)**

Model + prefetch pipeline ka **single state**:

- **model, tokenizer, is_loaded, load_error**  
- **Semaphore** – max 10 concurrent requests  
- **Thread pools** – general (16 workers), prefetch (2 workers)  
- **aiohttp session** – image download (get_session)  
- **prefetch_queue** – incoming requests (max 5)  
- **processed_queue** – preprocessed PrefetchedData (max 5)  
- **prefetch_tasks** – background worker tasks  

Methods:

- **get_semaphore()** – concurrency limit  
- **get_thread_pool() / get_prefetch_pool()** – thread pools  
- **start_prefetch_pipeline()** – PREFETCH_FACTOR (1) workers start karta hai  
- **_prefetch_worker(worker_id)** – queue se request leta hai, **_preprocess_request** call karta hai, result processed_queue mein daalta hai  
- **_preprocess_request(request_data)** – vendor URLs se async download, pickup base64/URL decode, dono ko **load_image** se tensor banata hai, PrefetchedData return  
- **submit_for_prefetch(request, request_id)** – request ko prefetch_queue mein daalna (non-blocking, queue full ho to skip)  
- **get_prefetched_data(timeout)** – processed_queue se data lena (short timeout)  

**Caching bilkul nahi** – sirf prefetch + queue, koi cache store nahi.

---

## **10. Request/Response Models (330–608)**

**RequestItem (Pydantic):**

- **pickupproductimage** – 1–10 URLs (vendor/reference images)  
- **skupickdone** – 1–10 items (base64 ya https URL – pickup images)  
- **productname**, **question**, **shippingid** – required  
- **productid**, **uuid**, **previousuuid** – optional  
- Validators: URLs http/https, base64/S3 valid, productname/question/shippingid non-empty/length check; **uuid** na ho to auto UUID generate  

**ProcessingResponse:**

- shippingid, uuid, product_id, processing_time_ai, Question (list), ai_decision, finalAction, ai_match_score, analysis, status, StatusCode, total_time, timestamp  

---

## **11. Image Processing (612–693)**

- **IMAGENET_MEAN / STD** – normalization  
- **build_transform()** – RGB, resize (input_size x input_size), ToTensor, Normalize  
- **find_closest_aspect_ratio()** – aspect ratio ko predefined ratios se match karke best (width, height) choose karta hai  
- **dynamic_preprocess()** – image ko patches mein split (min_num, max_num, image_size), thumbnail option; model ke expected grid ke hisaab se crop  
- **load_image(image_file, input_size, max_num)** – transform + dynamic_preprocess se list of tensors, phir **torch.stack**  
- **rewrite_s3_to_cloudfront()** – `xbeestest.s3.amazonaws.com` ko CloudFront domain se replace  

Vendor images **max_num=1**, pickup **max_num=config.PICKUP_PATCH (2)** use karte hain.

---

## **12. Async Image Download & Decode (598–733)**

- **download_image_async(session, url, uuid)** – aiohttp se GET, size check (MAX_IMAGE_SIZE), PIL RGB; fail pe ProcessingError  
- **decode_base64_image_batch(b64_strings, uuid)** – har item: agar **https** URL hai to CloudFront rewrite + requests.get (max 2 retries), warna **base64.b64decode**; size check; PIL RGB; koi bhi fail pe ProcessingError  

---

## **13. Data Processing – Question & JSON (836–893)**

- **process_verification_data(json_string)** – `request.question` ko parse karke **Question** list nikalta hai; try: json.loads double/ single / ast.literal_eval; fail pe ProcessingError  
- **number_to_word(total)** – 1–59 number ko "one", "two", … "fifty-nine" mein convert (prompt mein "one image", "two images" ke liye)  
- **extract_json_regex_fields()** – string se regex se image_analysis, verification_results, pickup_confidence nikal ke dict  
- **extract_json(input_string)** – pehle pyaml.safe_load, phir json.loads, phir regex se `{...}` dhundh ke json/ast/pyaml/regex try; model ke text response se JSON nikalne ke liye  

---

## **14. Prompt & Verification Fixing (895–1170)**

- **prompt_filter** – question type categorize: category_verification, design_matching, quantity_verification, brand_verification, packaging_verification, size_verification, color_verification, price_verification, seal_verification, label_verification, sku_verification, product_matching (keywords se)  
- **convert_to_regex()** – in keywords ka word-boundary regex  
- **contains_patterns(val)** – label/question text se type decide (e.g. "category" → category_verification)  
- **type_check, opposite_boolean, fix_bool** – boolean/numeric values aur unke opposite (y/n, true/false, etc.)  
- **damage_keywords, usage_keywords, neg_value** – damage/usage labels aur negative values ke liye  
- **std_prompt** – har verification type ke liye Result + Evidence template ("Based on pickup images, vendor images… Set Result to …")  
- **clean_string()** – special chars, extra spaces clean  
- **fix_verification_questions(questions_list)** – har question ke liye Type/ValueToCheck/Label dekh ke Result + Evidence instruction set karta hai (boolean/numeric/text/category + damage/usage special case); Confidence "0-100 percentage…", isRetakeImage "True if… False if…"  
- **generate_question_template(...)** – vendor/pickup image count, product description, question list use karke **full prompt** banata hai: image placeholders (Image-1 … Image-N), vendor vs pickup ranges, strict instructions, aur **fix_verification_questions** ka output + JSON schema jaisa format (qt) embed karta hai  

Yahi prompt model ko diya jata hai.

---

## **15. Model Load & Inference (1172–1396)**

- **load_model()** – CUDA check; AutoModel.from_pretrained (bfloat16, flash_attention_2, low_cpu_mem_usage); torch.compile(mode="reduce-overhead"); tokenizer; model_state mein set; fail pe ProcessingError 503  
- **run_model_inference(pixel_values, questions, num_patches)** – generation_config use karke **model.chat(tokenizer, pixel_values, questions, num_patches_list=num_patches, ...)**; inference_mode + cuda stream; sync; responses return  
- **save_to_database(data_dict, table_name)** – async; `rvpxbverification_fail` ho to drop_if_exists=True, else simple insert; conn.insert_single_dict_simple  
- **save_to_database_error()** – create_table_from_dict + insert (error/fail table ke liye)  
- **lifespan(app)** – startup: load_model, start_prefetch_pipeline; shutdown: stop prefetch, session close, thread pools shutdown, model delete, cuda cache clear  

---

## **16. String Match & Time (1398–1426)**

- **find_most_similar_string(main_string, list_of_strings, threshold=90)** – fuzzywuzzy (token_set_ratio) se list mein se sabse similar string; score >= threshold pe return (string, score), warna (None, 0). Use: vendor question labels vs model response labels match karne ke liye.  
- **get_current_time()** – UTC → IST (Asia/Kolkata), format "YYYY-MM-DD HH:MM:SS"  

---

## **17. Main Processing – process_request_with_prefetch (1428–1736)**

Ye **main flow** hai:

1. **Start** – start_time, request_id, data_to_save = request.model_dump(), timestamp; **background_tasks.add_task(save_to_database, data_to_save, 'rvpxbverification_request_data')** – request pehle hi DB mein save ho jati hai.  
2. **Model check** – model loaded nahi to ProcessingError 503.  
3. **Semaphore** – async with get_semaphore() se concurrency limit.  
4. **Prefetch try** – `get_prefetched_data(timeout=0.05)` se dekhta hai koi pehle se preprocessed data processed_queue mein hai.  
   - **Mil gaya** – vendor_tensors, pickup_tensors wahi use; counts set.  
   - **Nahi mila** – same request ke liye: session se vendor URLs download (rewrite_s3_to_cloudfront), pickup decode (base64/URL), dono ko load_image se tensors; phir **submit_for_prefetch(request, request_id)** se agla koi isko prefetch use kar sake (optional).  
5. **Validation** – vendor_img_count ya sr_images_count 0 ho to ProcessingError 400.  
6. **Model input** – img_tensors = vendor + pickup; num_patches list; **process_verification_data(request.question)** se question_data; **generate_question_template(...)** se questions string; pixel_values = sab tensors concat, bfloat16, cuda.  
7. **First inference** – run_model_inference(pixel_values, questions, num_patches); **extract_json(responses)** se result; **validate_json_schema(result)**.  
8. **First inference data** – uuid, shippingid, previous_request, Question (prompt), First_inference (result), First_response (raw), Second_* empty, timestamp.  
9. **Agar validation fail** – retry with extra line in prompt (confidence numeric, JSON schema); second inference; result again validate.  
   - **Dobara fail** – second_inference_data save in **rvpxbverification_fail**, phir ProcessingError 500.  
   - **Pass** – first_inference_data ko **rvpxbverification_fail** mein background save (retry success record).  
10. **Recommendation nikalna** – result se pickup_confidence.recommendation (Accept/Reject/Partial/Retry) → ai_recommendation (Pick / Not Pick) aur StatusCode (200/202). Unknown to ProcessingError.  
11. **Question matching** – verification_results se response labels vs question_data_copy (vendor labels). Agar sab labels match + sab ValueToCheck response mein hai to force **Pick**.  
12. **Missed questions** – agar response labels != vendor labels: **find_most_similar_string** se har vendor label ka best match response label; match mila to Result/Evidence/Confidence/isRetakeImage copy; nahi mila to missed_question, type ke hisaab se Result="" ya opposite_boolean, Confidence=0, isRetakeImage="true".  
13. **Question2** – question_data_copy ko response format mein: Result → answer, boolean fix (fix_bool), IsMandatory string, isRetakeImage lower.  
14. **analysis** – result.image_analysis se modified_analysis_data (test_product_description, reference_product_description, comparison).  
15. **Pick/Not Pick logic** – Agar ai_recommendation 'Pick': sab answer ko ValueToCheck se set; 'Not Pick': text/number type mein ValueToCheck != answer ho to answer ''.  
16. **Response dict** – shippingid, uuid, product_id, processing_time_ai, Question (Question2), ai_decision, finalAction, analysis, ai_match_score, status, StatusCode, timestamp, total_time.  
17. **DB save** – db_dict = response + key rename (Question→question, etc.) + result, prompt, vendorquestion, validation_status, is_latest, created_date, performance_metrics; **background_tasks.add_task(save_to_database, db_dict, 'rvpxbverification')**.  
18. **Return** – response_dict turant return (immediate response).  
19. **Errors** – ProcessingError re-raise; koi aur exception → create_error_response jaisa ProcessingError 500.  

---

## **18. Middleware (1738–1764)**

**RawRequestLoggingMiddleware** – har request ka body read karke log (path, method, body); body ko `receive()` se wapas attach karta hai taaki FastAPI dubara parse kar sake. Debugging ke liye.

---

## **19. FastAPI App & Endpoints (1766–1898)**

- **app** – FastAPI(lifespan=lifespan), title "InternVL v2.5", version 3.1.0.  
- **Middlewares** – RawRequestLoggingMiddleware, CORS (config se), TrustedHostMiddleware.  
- **GET /** – service name, status, version, features, max_concurrent_requests, prefetch_workers, caching_enabled=False.  
- **GET /health** – model_loaded, cuda, GPU memory, concurrency (active/max), prefetch pipeline (running, workers, queue sizes), cache_enabled=False.  
- **POST /process_request** – RequestItem leta hai, BackgroundTasks; **process_request_with_prefetch** call; result return; ProcessingError → create_error_response + HTTPException; koi aur exception → 500 + same error format.  
- **GET /metrics** – model, cuda, concurrency, prefetch stats, cache_size=0, performance flags, timestamp.  

---

## **20. Exception Handlers (1900–1940)**

- **ProcessingError** – create_error_response, JSONResponse with exc.status_code.  
- **HTTPException** – agar detail mein pehle se errorMsg wala dict hai to wahi, warna create_error_response se standard format.  
- **Exception** – generic "Internal server error", 500, same format.  

---

## **21. Main Entry (1942–2058)**

- `if __name__ == "__main__"`: uvicorn.run(app, host, port, log_level, access_log=True, reload=False, **workers=1**).  
- Logs: immediate response, max concurrent, thread pool, caching disabled.  

---

## **Flow Ek Line Mein**

Request aati hai → raw body log → validate (Pydantic) → request DB mein save (background) → semaphore acquire → prefetch se ya sync images download/decode → tensors + question template → model inference → JSON extract + schema validate → retry if invalid → recommendation (Pick/Not Pick) + question matching + missed questions handle → Question2 + analysis → response dict + result DB save (background) → response return → errors standardized format mein.

Agar kisi specific function ya block (e.g. fix_verification_questions, prefetch worker, DB tables) ka aur detail chahiye ho to bata dena, usi hisaab se aur Hinglish mein break-down kar dunga.