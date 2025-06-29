from job import Job
import json
import redis
import uuid
import config
from job_status import JobStatus

class Data:
    def __init__(self):
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)

    def create_job(self, job: Job) -> None:
        self.redis_client.hset(job.get_job_id(), mapping=self.prepare_mapping(job.get_details()))

    def enqueue_job(self, job: Job) -> None:
        job.update_status(JobStatus.PENDING)
        self.redis_client.rpush(config.PENDING_JOBS_QUEUE, json.dumps(job.get_details_with_job_id()))
        self.redis_client.hset(job.get_job_id(), key="status", value=JobStatus.PENDING.value)

    def get_job_status(self, job_id: str) -> JobStatus:
        return JobStatus(self.redis_client.hget(name=job_id, key="status").decode('utf-8'))

    @staticmethod
    def prepare_mapping(mapping) -> dict:
        # prepares for adding mapping to redis
        return {k: int(v) if isinstance(v, bool) else v for k, v in mapping.items()}
