Summary of what’s in place:

---

1. Dockerfile

- Base: pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime-ubuntu22.04 (PyTorch + CUDA, no need to install torch).

- Installs deps from requirements.txt, copies only fast_prod_new.py and sql_conn.py.

- No changes to fast_prod_new.py.

- Exposes port 8001, runs:

python -m uvicorn fast_prod_new:app --host 0.0.0.0 --port 8001.

- Model is not in the image; set MODEL_PATH at runtime (e.g. mount or SageMaker /opt/ml/model).

2. requirements.txt

- Lists all pip dependencies inferred from fast_prod_new.py (fastapi, uvicorn, transformers, aiohttp, pandas, Pillow, pyaml, jsonschema, fuzzywuzzy, pytz, etc.).

- flash-attn is not included (needs a matching CUDA build). There’s a commented line in the Dockerfile; uncomment and fix if your model requires it.

3. sql_conn.py (stub)

- Provides insert_single_dict_simple and create_table_from_dict as no-op async functions so the app starts without a real DB.

- Replace this file with your real sql_conn in the build context (or mount it) when you have the actual DB.

4. .dockerignore

- Keeps model dirs, .git, venvs, and logs out of the build context.

---

Build and run (GPU):

cd /home/yash/Desktop/office/Xpressbees

docker build -t xpressbees-internvl:latest .

# Run with model mounted (replace /path/to/full_14_08_2025_ch_28k with your model dir)
```dockerfile
docker run --gpus all -p 8001:8001 -e MODEL_PATH=/app/model -v /path/to/full_14_08_2025_ch_28k:/app/model xpressbees-internvl:latest
```

If you already have your own sql_conn.py, put it in the same folder as fast_prod_new.py before docker build; the stub will be overwritten. No edits were made to fast_prod_new.py.