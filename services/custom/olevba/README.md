# karton-olevba

Runs [olevba](https://github.com/decalage2/oletools) on incoming Office
documents to extract and analyze VBA macros.

## Underlying tool

`olevba` is part of the `oletools` package and ships as a console script.
Install it into the shared worker venv on the LXC:

```bash
/opt/karton-workers-venv/bin/pip install oletools
```

The service invokes the binary by absolute path
(`/opt/karton-workers-venv/bin/olevba`) so it does not rely on the
systemd unit's `PATH`.

## Notes

- The filter list covers the Office document extensions the
  karton-classifier emits with `kind: document, platform: win32`:
  `doc`, `docm`, `docx`, `xls`, `xlsm`, `xlsx`, `ppt`, `pptm`, `pptx`.
  This is broader than the original spec in `CLAUDE.md` (which only
  listed the four legacy / macro-enabled extensions) — olevba itself
  handles all nine, so we let it see all nine.
- olevba prints a multi-section text report to stdout; we capture stdout
  verbatim and ship it as the outgoing resource.

## Deploy

```bash
# On the Proxmox host:
pct enter 130

# Inside the workers LXC:
mkdir -p /opt/karton-custom/services/custom/olevba
# (copy karton-olevba.py into /opt/karton-custom/services/custom/olevba/)
# (copy karton-olevba.service to /etc/systemd/system/)
# (install the underlying tool:)
/opt/karton-workers-venv/bin/pip install oletools

systemctl daemon-reload
systemctl enable --now karton-olevba
systemctl status karton-olevba
journalctl -u karton-olevba -n 20 --no-pager
```
