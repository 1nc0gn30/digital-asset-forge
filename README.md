# digital-asset-forge

See `public/` for the web cockpit and `src/` for the CLI, HTTP and MCP servers.

## Test

```bash
python3 -m pytest -q tests/
```

## Safety

- The browser API only accepts cross-origin requests from `localhost` / `127.0.0.1` pages. POSTs from any other website get `403`, and CORS echoes only local origins (never `*`), so a site you visit can't drive or read this local server. CLI and agent clients (no `Origin` header) are unaffected.
- No store credentials; everything is generated locally.
