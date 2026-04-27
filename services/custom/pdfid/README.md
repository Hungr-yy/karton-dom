# karton-pdfid

Runs Didier Stevens' `pdfid.py` for static triage of incoming PDF samples.

## Underlying tool

[pdfid.py](https://github.com/DidierStevens/DidierStevensSuite/blob/master/pdfid.py)
is a single-file Python script. It is not installed via pip — download it
once onto the worker LXC:

```bash
mkdir -p /opt/pdfid
curl -L -o /opt/pdfid/pdfid.py \
    https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/pdfid.py
```

## Notes

- The service invokes `python /opt/pdfid/pdfid.py <sample_file>`. The path
  `/opt/pdfid/pdfid.py` is hardcoded in `karton-pdfid.py`; if the script
  lives elsewhere on a given worker, update the path there.
- The classifier emits `kind: document`, `extension: pdf` for PDFs; the
  service's filter matches that.

## Deploy

```bash
# On the Proxmox host:
pct enter 130

# Inside the workers LXC:
mkdir -p /opt/karton-custom/services/custom/pdfid
# (copy karton-pdfid.py into /opt/karton-custom/services/custom/pdfid/)
# (copy karton-pdfid.service to /etc/systemd/system/)
# (install the underlying tool:)
mkdir -p /opt/pdfid
curl -L -o /opt/pdfid/pdfid.py \
    https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/pdfid.py

systemctl daemon-reload
systemctl enable --now karton-pdfid
systemctl status karton-pdfid
journalctl -u karton-pdfid -n 20 --no-pager
```
