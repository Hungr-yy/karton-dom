# karton-dotnetfile

Extracts .NET PE metadata from incoming Windows executables using
[dotnetfile](https://github.com/pan-unit42/dotnetfile) (Palo Alto Unit 42).

## Underlying tool

`dotnetfile` is a library, not a CLI. The upstream repo ships a dumper
script `dotnetfile_dump.py` under `tools/`, but it is **not** installed as a
console entry point by `pip install dotnetfile`. We vendor it onto the
worker the same way pdfid vendors `pdfid.py`:

```bash
/opt/karton-workers-venv/bin/pip install dotnetfile

mkdir -p /opt/dotnetfile
curl -L -o /opt/dotnetfile/dotnetfile_dump.py \
    https://raw.githubusercontent.com/pan-unit42/dotnetfile/master/tools/dotnetfile_dump.py
```

## Notes

- The service invokes `python /opt/dotnetfile/dotnetfile_dump.py -f <sample_file>`.
  The script takes the sample path via the `-f` flag (not a bare positional
  arg). The path is hardcoded in `karton-dotnetfile.py`.
- The "is this even a .NET binary" check is implicit in the filters — only
  PE samples reach this service. On a non-.NET PE, `dotnetfile_dump.py` will
  raise; the karton task will fail and not propagate, which is acceptable.
- Filters cover both `platform: win32` and `platform: win64` PE EXEs as
  emitted by the karton-classifier.

## Deploy

```bash
# On the Proxmox host:
pct enter 130

# Inside the workers LXC:
mkdir -p /opt/karton-custom/karton-dotnetfile
# (copy karton-dotnetfile.py into /opt/karton-custom/karton-dotnetfile/)
# (copy karton-dotnetfile.service to /etc/systemd/system/)
# (install the underlying tool:)
/opt/karton-workers-venv/bin/pip install dotnetfile
mkdir -p /opt/dotnetfile
curl -L -o /opt/dotnetfile/dotnetfile_dump.py \
    https://raw.githubusercontent.com/pan-unit42/dotnetfile/master/tools/dotnetfile_dump.py

systemctl daemon-reload
systemctl enable --now karton-dotnetfile
systemctl status karton-dotnetfile
journalctl -u karton-dotnetfile -n 20 --no-pager
```
