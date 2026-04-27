from karton.core import Karton, Task, Resource
import subprocess


class CapaKarton(Karton):
    """
    Runs capa on incoming runnable samples to identify MITRE ATT&CK capabilities
    """
    identity = "karton.capa"
    filters = [{"type": "sample", "stage": "recognized", "kind": "runnable"}]

    def process(self, task: Task) -> None:
        # Get the incoming sample
        sample_resource = task.get_resource("sample")

        # Log with self.log
        self.log.info(f"Hi {sample_resource.name}, let me analyse you!")

        # Download the resource to a temporary file
        with sample_resource.download_temporary_file() as sample_file:
            # And run `capa` on it
            capa = subprocess.check_output(["/opt/karton-workers-venv/bin/capa", "-j", sample_file.name])

        # Send our results for further processing or reporting
        task = Task(
            {"type": "sample", "stage": "analyzed"},
            payload={"parent": sample_resource, "sample": Resource("capa", capa)},
        )
        self.send_task(task)


if __name__ == "__main__":
    # Here comes the main
    CapaKarton.main()
