# digital-asset-forge

> ⚡ **Live Web Application**: [https://digital-asset-forge.netlify.app](https://digital-asset-forge.netlify.app)  
> 💳 **Unlock Pro Lifetime License ($19 One-Time, $0/mo)**: **[Instant Pro Unlock via Stripe](https://buy.stripe.com/4gMfZg9AheOsdhKbcAfw40L)** *(Use promo code `FOUNDER25` for 25% off)*  
> 🏆 **All-Access Sovereign Pro Bundle (All 44 Tools — $49 Lifetime)**: **[Get All 44 Studios via Stripe](https://buy.stripe.com/eVq14m5k16hW4Le0xWfw40M)**

See `public/` for the web cockpit and `src/` for the CLI, HTTP and MCP servers.

## Test

```bash
python3 -m pytest -q tests/
```

## Safety

- The browser API only accepts cross-origin requests from `localhost` / `127.0.0.1` pages. POSTs from any other website get `403`, and CORS echoes only local origins (never `*`), so a site you visit can't drive or read this local server. CLI and agent clients (no `Origin` header) are unaffected.
- No store credentials; everything is generated locally.
