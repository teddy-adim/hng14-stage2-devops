import redis
import time
import os
import signal


r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379))
)

running = True


def handle_shutdown(signum, frame):
    global running
    print("Shutdown signal received, finishing current job...")
    running = False


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


def process_job(job_id):
    try:
        print(f"Processing job {job_id}")
        time.sleep(2)
        r.hset(f"job:{job_id}", "status", "completed")
        print(f"Done: {job_id}")
    except Exception as e:
        print(f"Error processing job {job_id}: {e}")
        r.hset(f"job:{job_id}", "status", "failed")


while running:
    job = r.brpop("job", timeout=5)
    if job:
        _, job_id = job
        process_job(job_id.decode())

print("Worker stopped cleanly")
