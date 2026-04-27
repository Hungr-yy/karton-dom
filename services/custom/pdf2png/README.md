# karton-pdf2png

Renders incoming PDFs to one PNG per page using `pdftoppm`, bundles the
pages into a single zip, and ships the zip as the outgoing resource.

## Underlying tool

`pdftoppm` ships in [poppler-utils](https://poppler.freedesktop.org/) and is
installed via apt — not pip. The system package places `pdftoppm` in
`/usr/bin`, so it's already on the systemd unit's `PATH`:

```bash
apt install poppler-utils
```

## Notes

- This is the one service in the repo that does not match the canonical
  `karton-strings.py` body line-for-line. `pdftoppm` writes its output to
  disk (one file per page), not to stdout, so the worker creates a temporary
  directory, runs `pdftoppm -png <sample> <tmpdir>/page`, then packages the
  resulting `page-1.png`, `page-2.png`, … files into a single zip held in
  memory and ships the zip bytes as `Resource("pdf2png", …)`.
- The zip uses `ZIP_STORED` (no compression) because PNGs are already
  DEFLATE-compressed; recompressing only burns CPU.
- **Tradeoff (per CLAUDE.md spec):** the alternative is to emit one karton
  task per page. That is more karton-idiomatic — downstream services could
  then operate per page — but it adds task-fanout logic and a more involved
  `process()` body. The single-zip choice keeps `process()` close to the
  reference shape and pushes any per-page work onto a future consumer that
  can unzip. Revisit if/when a per-page consumer service is introduced.

## Deploy

```bash
# On the Proxmox host:
pct enter 130

# Inside the workers LXC:
mkdir -p /opt/karton-custom/karton-pdf2png
# (copy karton-pdf2png.py into /opt/karton-custom/karton-pdf2png/)
# (copy karton-pdf2png.service to /etc/systemd/system/)
# (install the underlying tool:)
apt install poppler-utils

systemctl daemon-reload
systemctl enable --now karton-pdf2png
systemctl status karton-pdf2png
journalctl -u karton-pdf2png -n 20 --no-pager
```
