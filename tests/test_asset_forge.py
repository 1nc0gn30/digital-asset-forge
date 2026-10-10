"""Unit Tests for Digital Asset Forge.

100% Python Standard Library (unittest).
Zero external test framework dependencies.
"""

import unittest
from digital_asset_forge.ratios import RatioCalculator, RATIO_FAMILIES
from digital_asset_forge.pack_generator import ArtPackGenerator
from digital_asset_forge.printing_guide import PrintingGuideGenerator
from digital_asset_forge.etsy_copywriter import EtsyCopywriter

class TestDigitalAssetForge(unittest.TestCase):

    def test_ratio_families_completeness(self):
        """Verify all 5 standard ratio families exist with proper 300 DPI resolutions."""
        expected_keys = {"2x3", "3x4", "4x5", "11x14", "iso"}
        self.assertEqual(set(RATIO_FAMILIES.keys()), expected_keys)

        for key, spec in RATIO_FAMILIES.items():
            self.assertGreater(spec.max_pixel_dimensions_300dpi[0], 0)
            self.assertGreater(spec.max_pixel_dimensions_300dpi[1], 0)
            self.assertGreater(len(spec.supported_sizes_inches), 0)
            self.assertGreater(len(spec.supported_sizes_cm), 0)

    def test_dpi_validation_quality(self):
        """Test DPI validation thresholds."""
        # 7200x10800 on 24x36" = 300 DPI -> MUSEUM_GRADE
        m_rep = RatioCalculator.validate_dpi_quality(7200, 10800, 24, 36)
        self.assertEqual(m_rep["rating"], "MUSEUM_GRADE")
        self.assertEqual(m_rep["effective_dpi"], 300.0)

        # 4800x7200 on 24x36" = 200 DPI -> ACCEPTABLE
        a_rep = RatioCalculator.validate_dpi_quality(4800, 7200, 24, 36)
        self.assertEqual(a_rep["rating"], "ACCEPTABLE")
        self.assertEqual(a_rep["effective_dpi"], 200.0)

        # 1200x1800 on 24x36" = 50 DPI -> DEFICIENT
        d_rep = RatioCalculator.validate_dpi_quality(1200, 1800, 24, 36)
        self.assertEqual(d_rep["rating"], "DEFICIENT")
        self.assertEqual(d_rep["effective_dpi"], 50.0)

    def test_centered_crop_calculation(self):
        """Test aspect ratio crop box coordinates calculation."""
        # Source 6000x4000 (3:2 landscape) cropped to 4:5 vertical
        crop = RatioCalculator.calculate_centered_crop(6000, 4000, 4, 5)
        self.assertEqual(crop["crop_height"], 4000)
        self.assertEqual(crop["crop_width"], 3200)
        self.assertEqual(crop["crop_x"], 1400)
        self.assertEqual(crop["crop_y"], 0)

    def test_art_pack_manifest_and_zip_split(self):
        """Verify manifest generation and Etsy 20MB ZIP splitting logic."""
        manifest = ArtPackGenerator.generate_manifest(
            artwork_title="Bauhaus Midnight Horizon",
            artist_name="Neal Frazier"
        )
        self.assertEqual(manifest["artwork_title"], "Bauhaus Midnight Horizon")
        self.assertEqual(manifest["total_files"], 6)  # 5 image ratios + 1 guide
        self.assertEqual(len(manifest["files"]), 5)

        # Check Etsy bundle plan
        plan = manifest["etsy_delivery_plan"]
        self.assertTrue(plan["etsy_direct_upload_viable"])
        self.assertLessEqual(plan["total_zip_archives"], 5)
        for bundle in plan["bundles"]:
            self.assertLessEqual(bundle["bundle_size_mb"], 20.0)
            self.assertGreater(len(bundle["contained_files"]), 0)

    def test_printing_guide_generator(self):
        """Verify markdown printing manual generation."""
        md = PrintingGuideGenerator.generate_guide_markdown("Horizon", "Test Shop")
        self.assertIn("PRINTING & FRAMING GUIDE", md)
        self.assertIn("2:3 Ratio", md)
        self.assertIn("ISO Series", md)
        self.assertIn("Heavyweight Matte Paper", md)
        self.assertIn("Gelato", md)

    def test_etsy_copywriter_tags_and_margins(self):
        """Verify Etsy tags strictly meet Etsy's 13-tag, <=20-char constraints."""
        listing = EtsyCopywriter.generate_listing(
            artwork_title="Mid Century Arch",
            niche="geometric",
            retail_price_usd=7.50
        )
        self.assertEqual(listing["tags_count"], 13)
        self.assertEqual(len(listing["tags"]), 13)
        for tag in listing["tags"]:
            self.assertLessEqual(len(tag), 20, f"Tag exceeds 20 characters: {tag}")

        eco = listing["economics"]
        self.assertEqual(eco["retail_price_usd"], 7.50)
        self.assertGreater(eco["net_profit_per_sale_usd"], 0)
        self.assertGreater(eco["profit_margin_percentage"], 80.0)

if __name__ == "__main__":
    unittest.main()
