from karton.core import Karton, Task, Resource
import subprocess


class PdfidKarton(Karton):
    """
    Runs Didier Stevens' pdfid.py on incoming PDF samples
    """
    identity = "karton.pdfid"
    filters = [{"type": "sample", "stage": "recognized", "kind": "document", "extension": "pdf"}]

    def process(self, task: Task) -> None:
        # Get the incoming sample
        sample_resource = task.get_resource("sample")

        # Log with self.log
        self.log.info(f"Hi {sample_resource.name}, let me analyse you!")

        # Download the resource to a temporary file
        with sample_resource.download_temporary_file() as sample_file:
            # And run `pdfid.py` on it
            pdfid = subprocess.check_output(["python3", "/opt/pdfid/pdfid.py", sample_file.name])

        # Send our results for further processing or reporting
        task = Task(
            {"type": "sample", "stage": "analyzed"},
            payload={"parent": sample_resource, "sample": Resource("pdfid", pdfid)},
        )
        self.send_task(task)


if __name__ == "__main__":
    # Here comes the main
    PdfidKarton.main()
