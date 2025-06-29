import cherrypy
from job import Job
from job_status import JobStatus
from data import Data
from typing import Union
import time

class Service(object):
    def __init__(self):
        self.data = Data()

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET', 'POST'])
    @cherrypy.tools.json_out()
    def submit_job(self, prompt: str, high_quality: bool = False) -> dict:
        submitted_at = int(time.time())
        job = Job(submitted_at, prompt, high_quality)
        self.data.create_job(job)
        self.data.enqueue_job(job)
        return job.get_details_with_job_id()

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    @cherrypy.tools.json_out()
    def get_job_status(self, job_id: str) -> dict:
        job_status = self.data.get_job_status(job_id)
        return {"job_id": job_id, "status": job_status.value}

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def list_jobs(self, start=0, limit=10) -> str:
        pass

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def get_output_file(self, job_id: str):
        pass

    def _list_jobs(self) -> list[Job]:
        pass

    def _get_job_output_file_id(self, job_id: str) -> Union[str, None]:
        pass

if __name__ == '__main__':
    cherrypy.quickstart(Service())
