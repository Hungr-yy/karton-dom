from karton.core import Karton, Task, Resource
import subprocess


class DotnetfileKarton(Karton):
    """
    Runs dotnetfile_dump.py on incoming Windows PE samples to extract .NET metadata
    """
    identity = "karton.dotnetfile"
    filters = [
        {"type": "sample", "stage": "recognized", "kind": "runnable", "platform": "win32", "extension": "exe"},
        {"type": "sample", "stage": "recognized", "kind": "runnable", "platform": "win64", "extension": "exe"},
    ]

    def process(self, task: Task) -> None:
        # Get the incoming sample
        sample_resource = task.get_resource("sample")

        # Log with self.log
        self.log.info(f"Hi {sample_resource.name}, let me analyse you!")

        # Download the resource to a temporary file
        with sample_resource.download_temporary_file() as sample_file:
            # And run `dotnetfile_dump.py` on it
            dotnetfile = subprocess.check_output(["python3", "/opt/dotnetfile/dotnetfile_dump.py", "-f", sample_file.name])

        # Send our results for further processing or reporting
        task = Task(
            {"type": "sample", "stage": "analyzed"},
            payload={"parent": sample_resource, "sample": Resource("dotnetfile", dotnetfile)},
        )
        self.send_task(task)


if __name__ == "__main__":
    # Here comes the main
    DotnetfileKarton.main()
