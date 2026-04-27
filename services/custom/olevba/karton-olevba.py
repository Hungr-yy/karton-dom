from karton.core import Karton, Task, Resource
import subprocess


class OlevbaKarton(Karton):
    """
    Runs olevba on incoming Office documents to extract and analyze VBA macros
    """
    identity = "karton.olevba"
    filters = [
        {"type": "sample", "stage": "recognized", "kind": "document", "platform": "win32", "extension": "doc"},
        {"type": "sample", "stage": "recognized", "kind": "document", "platform": "win32", "extension": "docm"},
        {"type": "sample", "stage": "recognized", "kind": "document", "platform": "win32", "extension": "xls"},
        {"type": "sample", "stage": "recognized", "kind": "document", "platform": "win32", "extension": "xlsm"},
    ]

    def process(self, task: Task) -> None:
        # Get the incoming sample
        sample_resource = task.get_resource("sample")

        # Log with self.log
        self.log.info(f"Hi {sample_resource.name}, let me analyse you!")

        # Download the resource to a temporary file
        with sample_resource.download_temporary_file() as sample_file:
            # And run `olevba` on it
            olevba = subprocess.check_output(["olevba", sample_file.name])

        # Send our results for further processing or reporting
        task = Task(
            {"type": "sample", "stage": "analyzed"},
            payload={"parent": sample_resource, "sample": Resource("olevba", olevba)},
        )
        self.send_task(task)


if __name__ == "__main__":
    # Here comes the main
    OlevbaKarton.main()
