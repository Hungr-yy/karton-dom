# karton-olevba

Runs [olevba](https://github.com/decalage2/oletools) on incoming Office
documents to extract and analyze VBA macros.

## Underlying tool

`olevba` is part of the `oletools` package and ships as a console script.
Install it into the shared worker venv on the LXC:

```bash
/opt/karton-workers-venv/bin/pip install oletools
```

The service invokes `olevba` from `PATH`; the worker venv's `bin/` must be
reachable, or `olevba` must otherwise be resolvable on the unit's `PATH`.

## Notes

- The four filters cover the Office document types the karton-classifier
  emits with `kind: document, platform: win32`: `doc`, `docm`, `xls`,
  `xlsm`. Bare `docx`/`xlsx`/`pptx`/`pptm` are intentionally not included
  per the spec; add them later if/when the pipeline starts producing
  matching tasks.
- olevba prints a multi-section text report to stdout; we capture stdout
  verbatim and ship it as the outgoing resource.

## Deploy

```bash
# On the Proxmox host:
pct enter 130

# Inside the workers LXC:
mkdir -p /opt/karton-custom/karton-olevba
# (copy karton-olevba.py into /opt/karton-custom/karton-olevba/)
# (copy karton-olevba.service to /etc/systemd/system/)
# (install the underlying tool:)
/opt/karton-workers-venv/bin/pip install oletools

systemctl daemon-reload
systemctl enable --now karton-olevba
systemctl status karton-olevba
journalctl -u karton-olevba -n 20 --no-pager
```
