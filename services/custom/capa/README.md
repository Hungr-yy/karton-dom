# karton-capa

Runs Mandiant's [capa](https://github.com/mandiant/capa) on incoming runnable
samples to identify MITRE ATT&CK capabilities.

## Underlying tool

Two pieces are required: the `flare-capa` engine (installed via pip) and the
[`capa-rules`](https://github.com/mandiant/capa-rules) ruleset (cloned
separately). They version independently, so installing each from its own
upstream keeps the worker on the latest of both.

```bash
/opt/karton-workers-venv/bin/pip install flare-capa

git clone https://github.com/mandiant/capa-rules.git /opt/capa-rules
```

## Notes

- The service invokes `capa -j <sample_file>` (where `-j` requests JSON
  output). It relies on the `capa` console script being on `PATH` — the
  worker venv's `bin/` must be reachable, or `capa` must be symlinked into a
  system location.
- The capa-rules location is supplied via the `CAPA_RULES_PATH` environment
  variable set in the systemd unit. This is the **one deliberate deviation**
  from the canonical `.service` template (which otherwise allows only
  Description / WorkingDirectory / ExecStart to differ from the reference);
  it's necessary because the spec's `capa -j <sample_file>` subprocess line
  carries no `-r` flag.
- Keep both up to date with `pip install --upgrade flare-capa` and
  `git -C /opt/capa-rules pull`.

## Deploy

```bash
# On the Proxmox host:
pct enter 130

# Inside the workers LXC:
mkdir -p /opt/karton-custom/karton-capa
# (copy karton-capa.py into /opt/karton-custom/karton-capa/)
# (copy karton-capa.service to /etc/systemd/system/)
# (install the underlying tool and rules:)
/opt/karton-workers-venv/bin/pip install flare-capa
git clone https://github.com/mandiant/capa-rules.git /opt/capa-rules

systemctl daemon-reload
systemctl enable --now karton-capa
systemctl status karton-capa
journalctl -u karton-capa -n 20 --no-pager
```
