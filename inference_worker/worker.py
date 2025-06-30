import redis.asyncio as redis
import asyncio
import json
import config
from job_status import JobStatus
import httpx
import time

class Worker:
    mochi_inference_url = config.MOCHI_SERVICE_URL + ":" + config.MOCHI_SERVICE_PORT + "/predictions"

    def __init__(self):
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
        # self.redis_client = redis.Redis(host="localhost", port='31000', db=0)

    async def __aexit__(self, *excinfo):
        await self.redis_client.aclose()

    @classmethod
    async def fetch(cls, post_data: dict) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(Worker.mochi_inference_url, json=json.dumps(post_data))
            return response.text

    async def process_job(self, job_data) -> str:
        started_processing_at = int(time.time())
        """Define the task to perform with each job."""
        print(f"Processing job: {job_data}")
        data = {
            "input": {
                "fps": config.FPS,
                "prompt": job_data["prompt"],
                "num_frames": config.NUM_FRAMES,
                "guidance_scale": config.GUIDANCE_SCALE,
                "num_inference_steps": (config.HIGH_INFERENCE_COUNT if (job_data["enhanced"]) is True else config.LOW_INFERENCE_COUNT)
            }
        }
        job_data["started_processing_at"] = started_processing_at
        job_data["status"] = JobStatus.PROCESSING.value
        await self.redis_client.hset(job_data["job_id"], mapping=job_data)
        await self.redis_client.rpush(config.PROCESSING_JOBS_QUEUE, json.dumps(job_data))
        result = await self.fetch(data)
        return json.loads(result)["path"]

    async def worker_loop(self):
        print("Worker started. Waiting for jobs...")
        while True:
            processing_queue_length: int = await self.redis_client.llen(config.PROCESSING_JOBS_QUEUE)
            if processing_queue_length >= config.PROCESSING_JOBS_QUEUE_LENGTH_THRESHOLD:
                asyncio.sleep(10)
                continue
            job = await self.redis_client.blpop([config.PENDING_JOBS_QUEUE])
            if job:
                _, data = job
                try:
                    print("Processing new job.")
                    job_data = json.loads(data)
                    await self.process_job(job_data)
                except json.JSONDecodeError:
                    print("Invalid job data received. Skipping.")
            else:
                print("No job found. Retrying...")

async def main():
    worker = Worker()
    workers = [
        asyncio.create_task(worker.worker_loop())
        for i in range(config.NUM_WORKERS)
    ]
    try:
        await asyncio.gather(*workers)
    except Exception as e:
        print(f"Error in worker loop: {e}")

if __name__ == "__main__":
    asyncio.run(main())
