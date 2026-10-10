"""Digital Asset Forge - Sovereign Command-Line Interface.

Zero-dependency Python standard library CLI.
"""

import argparse
import json
import sys
from .ratios import RatioCalculator
from .pack_generator import ArtPackGenerator
from .printing_guide import PrintingGuideGenerator
from .etsy_copywriter import EtsyCopywriter
from .server import run_server

def main():
    parser = argparse.ArgumentParser(
        prog="digital-asset-forge",
        description="High-Res 300 DPI Multi-Ratio Wall Art Pack Generator (Etsy & Shopify 98% Margin)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Subcommand: manifest
    p_manifest = subparsers.add_parser("manifest", help="Generate multi-ratio digital product pack manifest")
    p_manifest.add_argument("--title", default="Celestial Geometry", help="Artwork title")
    p_manifest.add_argument("--artist", default="Neal Frazier", help="Artist name")
    p_manifest.add_argument("--json", action="store_true", help="Output raw JSON")

    # Subcommand: guide
    p_guide = subparsers.add_parser("guide", help="Generate customer printing instructions manual")
    p_guide.add_argument("--title", default="Celestial Geometry", help="Artwork title")
    p_guide.add_argument("--shop", default="NullAI Studio", help="Shop brand name")

    # Subcommand: etsy
    p_etsy = subparsers.add_parser("etsy", help="Generate Etsy listing copy, 13 tags, and margin economics")
    p_etsy.add_argument("--title", default="Celestial Geometry", help="Artwork title")
    p_etsy.add_argument("--niche", default="abstract", choices=["abstract", "botanical", "landscape", "geometric"])
    p_etsy.add_argument("--price", type=float, default=6.99, help="Retail price USD")
    p_etsy.add_argument("--json", action="store_true", help="Output raw JSON")

    # Subcommand: dpi
    p_dpi = subparsers.add_parser("dpi", help="Validate pixel resolution against target physical print size")
    p_dpi.add_argument("--width", type=int, default=7200, help="Source image pixel width")
    p_dpi.add_argument("--height", type=int, default=10800, help="Source image pixel height")
    p_dpi.add_argument("--target-w", type=float, default=24.0, help="Physical print width in inches")
    p_dpi.add_argument("--target-h", type=float, default=36.0, help="Physical print height in inches")

    # Subcommand: server
    p_server = subparsers.add_parser("server", help="Launch HTTP server and Web UI")
    p_server.add_argument("--port", type=int, default=8118, help="Server port (default: 8118)")

    args = parser.parse_args()

    if args.command == "manifest":
        manifest = ArtPackGenerator.generate_manifest(args.title, args.artist)
        if args.json:
            print(json.dumps(manifest, indent=2))
        else:
            print("=" * 70)
            print(f"📦 DIGITAL ASSET FORGE PACK: {manifest['artwork_title']}")
            print(f"Artist: {manifest['artist']} | Total Files: {manifest['total_files']} | Est. Size: {manifest['total_estimated_size_mb']} MB")
            print("=" * 70)
            for f in manifest["files"]:
                print(f"• [{f['ratio']}] {f['filename']}")
                print(f"   Max Size: {f['max_print_size']} | Resolution: {f['resolution']} (300 DPI)")
            print("-" * 70)
            plan = manifest["etsy_delivery_plan"]
            print(f"Etsy Upload Viable: {'YES' if plan['etsy_direct_upload_viable'] else 'NO'} ({plan['total_zip_archives']} ZIP archives)")
            for b in plan["bundles"]:
                print(f"   - {b['zip_filename']} ({b['bundle_size_mb']} MB, {len(b['contained_files'])} files)")
            print("=" * 70)

    elif args.command == "guide":
        print(PrintingGuideGenerator.generate_guide_markdown(args.title, args.shop))

    elif args.command == "etsy":
        listing = EtsyCopywriter.generate_listing(args.title, args.niche, args.price)
        if args.json:
            print(json.dumps(listing, indent=2))
        else:
            print("=" * 70)
            print(f"🏷️  ETSY LISTING: {listing['title']}")
            print("=" * 70)
            print("13 SEARCH TAGS (<= 20 chars each):")
            for i, tag in enumerate(listing["tags"], 1):
                print(f"  {i}. {tag} ({len(tag)} chars)")
            print("-" * 70)
            eco = listing["economics"]
            print(f"Retail Price: ${eco['retail_price_usd']:.2f}")
            print(f"Etsy Fees:    ${eco['total_platform_fees_usd']:.2f} (Listing $0.20 + Tx 6.5% + Proc 3%+$0.25)")
            print(f"Net Margin:   ${eco['net_profit_per_sale_usd']:.2f} ({eco['profit_margin_percentage']}%)")
            print(f"Monthly Net (100 sales): ${eco['monthly_net_at_100_sales_usd']:.2f}")
            print(f"Monthly Net (500 sales): ${eco['monthly_net_at_500_sales_usd']:.2f}")
            print("=" * 70)

    elif args.command == "dpi":
        report = RatioCalculator.validate_dpi_quality(args.width, args.height, args.target_w, args.target_h)
        print("=" * 60)
        print(f"📐 DPI AUDIT REPORT: {report['rating']}")
        print(f"Pixel Dimensions:    {report['pixel_dimensions']}")
        print(f"Physical Target:     {report['physical_dimensions']}")
        print(f"Effective DPI:       {report['effective_dpi']} DPI ({report['label']})")
        print(f"Status:              {report['status'].upper()}")
        print("=" * 60)

    elif args.command == "server":
        run_server(args.port)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
