"""Digital Asset Forge - High-Performance Threaded HTTP Server (Port 8118)
Zero-dependency Python 3.10+ Standard Library HTTP & Static Server
"""

from typing import Optional
import http.server
import json
import os
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Dict, Any

from .ratios import RatioCalculator
from .pack_generator import ArtPackGenerator
from .printing_guide import PrintingGuideGenerator
from .etsy_copywriter import EtsyCopywriter


def _default_bind_host() -> str:
    """Bind address: localhost unless explicitly opted in via $ZOTH_BIND_HOST or
    $HOST (IP literal only; zsh sets HOST to the hostname) or --host."""
    import ipaddress, os
    for var in ("ZOTH_BIND_HOST", "HOST"):
        val = os.environ.get(var, "").strip()
        if val == "localhost":
            return "127.0.0.1"
        if val:
            try:
                ipaddress.ip_address(val)
                return val
            except ValueError:
                pass
    return "127.0.0.1"


PORT = int(os.environ.get("ASSET_FORGE_PORT", 8118))
START_TIME = time.time()

TELEMETRY = {
    "packs_generated": 0,
    "dpi_audits_performed": 0,
    "etsy_listings_optimized": 0,
    "cumulative_potential_revenue_usd": 0.0
}

PUBLIC_DIR = Path(__file__).resolve().parent.parent.parent / "public"

class AssetForgeHandler(http.server.SimpleHTTPRequestHandler):
    """Zero-dependency HTTP Handler for Digital Asset Forge API and Web UI."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def _send_json(self, data: Any, status: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/health":
            self._send_json({
                "status": "healthy",
                "service": "digital-asset-forge",
                "version": "1.0.0",
                "port": PORT,
                "uptime_seconds": round(time.time() - START_TIME, 1)
            })
            return

        if path == "/api/stats":
            self._send_json({
                "telemetry": TELEMETRY,
                "uptime_seconds": round(time.time() - START_TIME, 1)
            })
            return

        if path == "/api/ratios":
            families = RatioCalculator.get_all_families()
            self._send_json({
                "count": len(families),
                "ratio_families": families
            })
            return

        # Fallback to static files
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length)
            payload = json.loads(post_body.decode("utf-8")) if post_body else {}
        except Exception as e:
            self._send_json({"error": f"Invalid JSON payload: {str(e)}"}, status=400)
            return

        if path == "/api/generate_pack":
            title = payload.get("artwork_title", "Abstract Horizon")
            artist = payload.get("artist_name", "Neal Frazier")
            manifest = ArtPackGenerator.generate_manifest(artwork_title=title, artist_name=artist)

            TELEMETRY["packs_generated"] += 1
            TELEMETRY["cumulative_potential_revenue_usd"] += 6.99 * 50  # Avg pack sales value

            self._send_json({
                "manifest": manifest,
                "status": "success"
            })
            return

        if path == "/api/printing_guide":
            title = payload.get("artwork_title", "Celestial Geometry")
            shop = payload.get("shop_name", "NullAI Studio")
            guide = PrintingGuideGenerator.generate_guide_payload(artwork_title=title, shop_name=shop)
            self._send_json({
                "printing_guide": guide,
                "status": "success"
            })
            return

        if path == "/api/etsy_copy":
            title = payload.get("artwork_title", "Celestial Obsidian")
            niche = payload.get("niche", "abstract")
            price = float(payload.get("retail_price_usd", 6.99))
            listing = EtsyCopywriter.generate_listing(artwork_title=title, niche=niche, retail_price_usd=price)

            TELEMETRY["etsy_listings_optimized"] += 1

            self._send_json({
                "listing": listing,
                "status": "success"
            })
            return

        if path == "/api/validate_dpi":
            w_px = int(payload.get("pixel_width", 7200))
            h_px = int(payload.get("pixel_height", 10800))
            w_in = float(payload.get("target_width_inches", 24))
            h_in = float(payload.get("target_height_inches", 36))

            report = RatioCalculator.validate_dpi_quality(w_px, h_px, w_in, h_in)
            TELEMETRY["dpi_audits_performed"] += 1

            self._send_json({
                "dpi_report": report,
                "status": "success"
            })
            return

        self._send_json({"error": f"Endpoint not found: {path}"}, status=404)

def run_server(port: int = PORT, host: Optional[str] = None):
    host = host or _default_bind_host()
    server_address = (host, port)
    httpd = http.server.ThreadingHTTPServer(server_address, AssetForgeHandler)
    print(f"🚀 Digital Asset Forge listening on http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Digital Asset Forge gracefully...")
        httpd.server_close()

if __name__ == "__main__":
    import argparse
    _ap = argparse.ArgumentParser(description="Run the HTTP server and web UI")
    _ap.add_argument("--host", default=None, help="Host interface (default: 127.0.0.1 or $ZOTH_BIND_HOST; use 0.0.0.0 only on trusted networks)")
    _ap.add_argument("--port", type=int, default=PORT)
    _a = _ap.parse_args()
    run_server(port=_a.port, host=_a.host)
