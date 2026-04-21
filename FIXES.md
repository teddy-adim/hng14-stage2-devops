# FIXES.md

Every bug found in the application, documented with file, line, problem, and fix.

---

## 1. api/main.py — Hardcoded Redis host

**File:** `api/main.py` | **Line:** 8  
**Problem:** `host="localhost"` was hardcoded. Docker containers are isolated — they cannot reach each other via localhost. Each container needs to reference other services by their docker-compose service name.  
**Fix:** Changed to `host=os.getenv("REDIS_HOST", "redis")` so the host is read from an environment variable at runtime.

---

## 2. api/main.py — Hardcoded Redis port

**File:** `api/main.py` | **Line:** 8  
**Problem:** `port=6379` was hardcoded directly in the code. Hardcoded configuration makes the app inflexible and hard to change across environments.  
**Fix:** Changed to `port=int(os.getenv("REDIS_PORT", 6379))` to read from environment variable.

---

## 3. api/main.py — Wrong HTTP status for missing job

**File:** `api/main.py` | **Line:** 20  
**Problem:** When a job ID was not found the API returned HTTP 200 (success) with an error message in the body. This is incorrect — HTTP 200 means everything is fine. A missing resource must return HTTP 404.  
**Fix:** Changed to `JSONResponse(status_code=404, content={"error": "not found"})`.

---

## 4. api/main.py — Missing /health endpoint

**File:** `api/main.py`  
**Problem:** No health check endpoint existed. Docker needs a dedicated endpoint to periodically check if the container is alive and ready to serve traffic. Without it Docker cannot detect a broken container.  
**Fix:** Added `GET /health` endpoint that returns `{"status": "healthy"}` with HTTP 200.

---

## 5. worker/worker.py — Hardcoded Redis host

**File:** `worker/worker.py` | **Line:** 6  
**Problem:** Same as api/main.py — `host="localhost"` fails inside Docker because containers are isolated and cannot reach each other via localhost.  
**Fix:** Changed to `host=os.getenv("REDIS_HOST", "redis")`.

---

## 6. worker/worker.py — Hardcoded Redis port

**File:** `worker/worker.py` | **Line:** 6  
**Problem:** `port=6379` hardcoded. Should be configurable via environment variable.  
**Fix:** Changed to `port=int(os.getenv("REDIS_PORT", 6379))`.

---

## 7. worker/worker.py — signal module imported but never used

**File:** `worker/worker.py` | **Line:** 4  
**Problem:** The `signal` module was imported but no signal handlers were registered. When Docker stops a container it sends a SIGTERM signal giving the process a chance to finish cleanly. Without a handler the worker gets killed immediately mid-job — the job stays stuck as `queued` forever and the frontend polls endlessly.  
**Fix:** Registered SIGTERM and SIGINT handlers that set a `running` flag to False. The worker finishes its current job then exits cleanly.

---

## 8. worker/worker.py — No error handling around job processing

**File:** `worker/worker.py` | **Lines:** 8-12  
**Problem:** No error handling existed around job processing. If Redis went down or any exception occurred the worker would crash entirely — all remaining jobs in the queue would never be processed and their status would stay `queued` forever.  
**Fix:** Wrapped job processing in a try/except block. On success status updates to `completed`. On failure status updates to `failed` and the worker continues to the next job.

---

## 9. frontend/app.js — Hardcoded API URL

**File:** `frontend/app.js` | **Line:** 6  
**Problem:** `API_URL = "http://localhost:8000"` was hardcoded. Inside Docker the frontend container cannot reach the API container via localhost — it must use the API's docker-compose service name.  
**Fix:** Changed to `process.env.API_URL || "http://api:8000"` to read from environment variable.

---

## 10. frontend/app.js — Vague error messages

**File:** `frontend/app.js` | **Lines:** 14, 21  
**Problem:** Both error handlers returned the generic message `"something went wrong"`. This completely hides the real error making it impossible to debug failures in production.  
**Fix:** Changed to return `err.message` so the actual error is visible in the response.

---

## 11. frontend/app.js — Missing /health endpoint

**File:** `frontend/app.js`  
**Problem:** No health check endpoint for Docker HEALTHCHECK. Without this Docker cannot verify the frontend container is actually serving traffic.  
**Fix:** Added `GET /health` endpoint returning `{"status": "healthy"}` with HTTP 200.

---

## 12. frontend/views/index.html — Infinite polling on failed jobs

**File:** `frontend/views/index.html` | **Line:** 20  
**Problem:** The polling function only stopped when job status was `completed`. If a job failed the status would never become `completed` — the frontend would poll the API endlessly, wasting resources and never showing the user what happened.  
**Fix:** Added `&& data.status !== 'failed'` condition so polling stops on both `completed` and `failed`.

---

## 13. api/requirements.txt — Unpinned package versions

**File:** `api/requirements.txt`  
**Problem:** No version numbers were specified for any package. Every Docker build would download the latest version — meaning two builds of the same code could produce different results if a package released a breaking update.  
**Fix:** Pinned all versions to what is currently installed and tested: `fastapi==0.136.0`, `uvicorn==0.44.0`, `redis==7.4.0`.

---

## 14. worker/requirements.txt — Unpinned package versions

**File:** `worker/requirements.txt`  
**Problem:** Same issue — `redis` had no version pinned.  
**Fix:** Pinned to `redis==7.4.0`.