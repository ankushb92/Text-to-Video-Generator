from typing import Optional
from job_status import JobStatus
import uuid
import random

class Job:
    def __init__(self, submitted_at: int, prompt: str, enhances_job_id: Optional[str] = None, status: JobStatus = JobStatus.CREATED, parent_seed: Optional[str] = None):
        self._job_id = str(uuid.uuid4())
        self._enhances_job_id = enhances_job_id
        self.seed = parent_seed if (enhances_job_id is True) else random.randint(1, 1000_000_000)
        self.submitted_at = submitted_at
        self.prompt = prompt
        self.status = status

    def update_status(self, status: JobStatus) -> None:
        self.status = status

    def get_job_id(self) -> str:
        return self._job_id
    
    def get_enhances_job_id(self) -> Optional[str]:
        return self._enhances_job_id
    
    def is_enhanced(self):
        return (self.get_enhances_job_id() is not None)

    def get_details(self) -> dict:
        return {
            "submitted_at": self.submitted_at,
            "prompt": self.prompt,
            "enhanced": self.is_enhanced(),
            "seed": self.seed,
            "status": self.status.value
        }

    def get_details_with_job_id(self) -> dict:
        return dict({"job_id": self.get_job_id()}, **self.get_details())
