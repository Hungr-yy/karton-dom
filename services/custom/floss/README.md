# karton-floss

Runs Mandiant's [flare-floss](https://github.com/mandiant/flare-floss) on
incoming runnable samples to extract and deobfuscate strings.

## Underlying tool

flare-floss installs via pip and ships a `floss` console script. Install it
into the shared worker venv on the LXC:

```bash
/opt/karton-workers-venv/bin/pip install flare-floss
```

The service invokes the binary by absolute path
(`/opt/karton-workers-venv/bin/floss`) so it does not rely on the systemd
unit's `PATH`.

## Notes

- The classifier's `kind: runnable` covers PE/ELF/Mach-O, so this service
  picks up all executable samples regardless of platform/extension.
- floss prints results to stdout; we capture stdout verbatim and ship it as
  the outgoing resource.

## Deploy

```bash
# On the Proxmox host:
pct enter 130

# Inside the workers LXC:
mkdir -p /opt/karton-custom/services/custom/floss
# (copy karton-floss.py into /opt/karton-custom/services/custom/floss/)
# (copy karton-floss.service to /etc/systemd/system/)
# (install the underlying tool:)
/opt/karton-workers-venv/bin/pip install flare-floss

systemctl daemon-reload
systemctl enable --now karton-floss
systemctl status karton-floss
journalctl -u karton-floss -n 20 --no-pager
```
