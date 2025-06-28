import cherrypy
from job import Job
from job_status import JobStatus

class Service(object):
    def __init__(self):
        pass

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET', 'POST'])
    def submit_job(self, prompt: str) -> str:
        job = Job(prompt)
        success = self._submit_job(job)
        if not success:
            # handle failure
            pass
        #handle success

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    @cherrypy.tools.json_out()
    def get_job_status(self, job_id: str) -> dict:
        job_status = self._get_job_status(job_id)
        cherrypy.response.status = 200
        return {"job_id": job_id, "status": job_status.value}

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def list_jobs(self, job_id: str) -> str:
        pass

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def get_output_file(self, job_id: str):
        pass

    def _submit_job(self, job: Job) -> bool:
        pass

    def _get_job_status(self, job_id: str) -> JobStatus:
        pass

    def _list_jobs(self) -> list[Job]:
        pass

    def _get_job_output_file_id(self, job_id: str) -> str | None:
        pass

if __name__ == '__main__':
    cherrypy.quickstart(Service())
