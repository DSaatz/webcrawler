from fastapi import FastAPI, BackgroundTasks, HTTPException
from webcrawler.crawler import crawl
import uuid
import threading

app = FastAPI()

job_status = {}
crawl_lock = threading.Lock()
current_job_id = None

def run_crawl(job_id: str, seed_url: str, page_limit: int, token_limit: int):
    global current_job_id
    try:
        crawl(seed_url, page_limit, token_limit)
        job_status[job_id] = "completed"
    except Exception as e:
        job_status[job_id] = f"failed: {e}"
    finally:
        # Release lock after crawl finishes
        crawl_lock.release()
        current_job_id = None

@app.post("/crawl")
def crawl_endpoint(seed_url: str, page_limit: int = 1000, token_limit: int = 500, background_tasks: BackgroundTasks = None):
    global current_job_id

    if crawl_lock.locked():
        raise HTTPException(status_code=409, detail="A crawl is already running")

    crawl_lock.acquire()
    job_id = str(uuid.uuid4())
    job_status[job_id] = "running"
    current_job_id = job_id
    background_tasks.add_task(run_crawl, job_id, seed_url, page_limit, token_limit)
    return {"status": "started", "job_id": job_id}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    status = job_status.get(job_id, "not found")
    return {"job_id": job_id, "status": status}

@app.get("/current")
def get_current_job():
    return {"current_job_id": current_job_id, "status": job_status.get(current_job_id) if current_job_id else None}
