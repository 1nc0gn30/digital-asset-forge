"""Digital Asset Forge - Antigravity MCP Stdio Server.

Exposes 6 JSON-RPC 2.0 Tools for Autonomous Agent Digital Product Generation
Zero external dependencies (100% Python standard library).
"""

import sys
import json
import traceback
from typing import Dict, Any, List

from .ratios import RatioCalculator
from .pack_generator import ArtPackGenerator
from .printing_guide import PrintingGuideGenerator
from .etsy_copywriter import EtsyCopywriter

TOOLS_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "name": "forge_calculate_ratios",
        "description": "Calculates exact 300 DPI pixel dimensions and maximum print sizes for all 5 core wall art aspect ratio families (2:3, 3:4, 4:5, 11:14, and ISO paper).",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "forge_generate_art_pack_manifest",
        "description": "Generates a complete multi-ratio digital wall art pack manifest with exact file naming, pixel dimensions at 300 DPI, and Etsy ZIP bundle layout.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "artwork_title": {
                    "type": "string",
                    "description": "Title of the artwork (e.g. 'Emerald Obsidian Horizon', 'Bauhaus Kinetic Sphere')",
                    "default": "Emerald Obsidian Horizon"
                },
                "artist_name": {
                    "type": "string",
                    "description": "Artist or shop name",
                    "default": "Neal Frazier"
                }
            },
            "required": ["artwork_title"]
        }
    },
    {
        "name": "forge_create_printing_guide",
        "description": "Generates a ready-to-deliver customer printing instruction manual with frame sizing tables, fine art paper recommendations, and online print lab options.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "artwork_title": {
                    "type": "string",
                    "description": "Artwork title",
                    "default": "Celestial Geometry"
                },
                "shop_name": {
                    "type": "string",
                    "description": "Etsy or Shopify store brand name",
                    "default": "NullAI Art Studio"
                }
            }
        }
    },
    {
        "name": "forge_generate_etsy_listing",
        "description": "Generates high-converting Etsy listing copy: search-optimized title, exactly 13 ranking tags (all <= 20 chars), description, and fee margin analysis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "artwork_title": {
                    "type": "string",
                    "description": "Artwork title",
                    "default": "Moody Emerald Abstract"
                },
                "niche": {
                    "type": "string",
                    "description": "Art category: 'abstract', 'botanical', 'landscape', 'geometric'",
                    "enum": ["abstract", "botanical", "landscape", "geometric"],
                    "default": "abstract"
                },
                "retail_price_usd": {
                    "type": "number",
                    "description": "Retail digital download price in USD",
                    "default": 6.99
                }
            },
            "required": ["artwork_title"]
        }
    },
    {
        "name": "forge_validate_image_dpi",
        "description": "Evaluates source pixel resolution against physical frame dimensions in inches to guarantee 300 DPI museum-grade print fidelity.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pixel_width": {"type": "integer", "description": "Image width in pixels", "default": 7200},
                "pixel_height": {"type": "integer", "description": "Image height in pixels", "default": 10800},
                "target_width_inches": {"type": "number", "description": "Physical frame width in inches", "default": 24},
                "target_height_inches": {"type": "number", "description": "Physical frame height in inches", "default": 36}
            },
            "required": ["pixel_width", "pixel_height", "target_width_inches", "target_height_inches"]
        }
    },
    {
        "name": "forge_optimize_zip_split",
        "description": "Calculates optimal multi-archive bundle split ensuring all uploaded files fit strictly under Etsy's 20MB file limit.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "artwork_title": {"type": "string", "default": "Abstract Collection"}
            }
        }
    }
]

def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute MCP tool invocation."""
    if name == "forge_calculate_ratios":
        families = RatioCalculator.get_all_families()
        return {
            "content": [{"type": "text", "text": json.dumps(families, indent=2)}]
        }

    elif name == "forge_generate_art_pack_manifest":
        title = arguments.get("artwork_title", "Emerald Obsidian Horizon")
        artist = arguments.get("artist_name", "Neal Frazier")
        manifest = ArtPackGenerator.generate_manifest(title, artist)
        return {
            "content": [{"type": "text", "text": json.dumps(manifest, indent=2)}]
        }

    elif name == "forge_create_printing_guide":
        title = arguments.get("artwork_title", "Celestial Geometry")
        shop = arguments.get("shop_name", "NullAI Art Studio")
        guide = PrintingGuideGenerator.generate_guide_payload(title, shop)
        return {
            "content": [{"type": "text", "text": json.dumps(guide, indent=2)}]
        }

    elif name == "forge_generate_etsy_listing":
        title = arguments.get("artwork_title", "Moody Emerald Abstract")
        niche = arguments.get("niche", "abstract")
        price = float(arguments.get("retail_price_usd", 6.99))
        listing = EtsyCopywriter.generate_listing(title, niche, price)
        return {
            "content": [{"type": "text", "text": json.dumps(listing, indent=2)}]
        }

    elif name == "forge_validate_image_dpi":
        w_px = int(arguments.get("pixel_width", 7200))
        h_px = int(arguments.get("pixel_height", 10800))
        w_in = float(arguments.get("target_width_inches", 24))
        h_in = float(arguments.get("target_height_inches", 36))
        report = RatioCalculator.validate_dpi_quality(w_px, h_px, w_in, h_in)
        return {
            "content": [{"type": "text", "text": json.dumps(report, indent=2)}]
        }

    elif name == "forge_optimize_zip_split":
        title = arguments.get("artwork_title", "Abstract Collection")
        manifest = ArtPackGenerator.generate_manifest(title)
        return {
            "content": [{"type": "text", "text": json.dumps(manifest.get("etsy_delivery_plan", {}), indent=2)}]
        }

    else:
        raise ValueError(f"Unknown tool name: {name}")

def run_mcp_stdio():
    """Stdio JSON-RPC 2.0 loop."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS_DEFINITIONS}
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                result = handle_call_tool(tool_name, tool_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": result
                }
            elif method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "digital-asset-forge",
                            "version": "1.0.0"
                        }
                    }
                }
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": str(e),
                    "data": traceback.format_exc()
                }
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run_mcp_stdio()
