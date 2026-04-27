from karton.core import Karton, Task, Resource
import subprocess
import tempfile
import os
import io
import zipfile


class Pdf2pngKarton(Karton):
    """
    Renders incoming PDFs to one PNG per page using pdftoppm and ships them as a zip
    """
    identity = "karton.pdf2png"
    filters = [{"type": "sample", "stage": "recognized", "kind": "document", "extension": "pdf"}]

    def process(self, task: Task) -> None:
        # Get the incoming sample
        sample_resource = task.get_resource("sample")

        # Log with self.log
        self.log.info(f"Hi {sample_resource.name}, let me analyse you!")

        # Download the resource to a temporary file
        with sample_resource.download_temporary_file() as sample_file:
            # And run `pdftoppm` on it, then zip the produced pages
            with tempfile.TemporaryDirectory() as tmpdir:
                subprocess.check_output(["pdftoppm", "-png", sample_file.name, os.path.join(tmpdir, "page")])
                buf = io.BytesIO()
                with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_STORED) as zf:
                    for fname in sorted(os.listdir(tmpdir)):
                        zf.write(os.path.join(tmpdir, fname), arcname=fname)
                pdf2png = buf.getvalue()

        # Send our results for further processing or reporting
        task = Task(
            {"type": "sample", "stage": "analyzed"},
            payload={"parent": sample_resource, "sample": Resource("pdf2png", pdf2png)},
        )
        self.send_task(task)


if __name__ == "__main__":
    # Here comes the main
    Pdf2pngKarton.main()
