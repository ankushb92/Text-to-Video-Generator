from job_status import JobStatus
import uuid

class Job:
    def __init__(self, submitted_at: int, prompt: str, high_quality=False, status: JobStatus = JobStatus.CREATED):
        self._job_id = str(uuid.uuid4())
        self.submitted_at = submitted_at
        self.prompt = prompt
        self.high_quality = high_quality
        self.status = status

    def update_status(self, status: JobStatus) -> None:
        self.status = status

    def get_job_id(self) -> str:
        return self._job_id

    def get_details(self) -> dict:
        return {
            "submitted_at": self.submitted_at,
            "prompt": self.prompt,
            "high_quality": self.high_quality,
            "status": self.status.value
        }

    def get_details_with_job_id(self) -> dict:
        return dict({"job_id": self.get_job_id()}, **self.get_details())
