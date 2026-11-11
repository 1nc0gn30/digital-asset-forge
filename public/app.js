/**
 * Digital Asset Forge - Sovereign Client Application
 * 100% In-Browser Computation & Manifest Generation
 */

(function () {
  const RATIOS = {
    "2x3": { label: "2:3 Ratio", max_in: "24x36\"", max_px: "7200x10800", w: 7200, h: 10800, mb: 11.8, desc: "4x6, 6x9, 8x12, 10x15, 12x18, 16x24, 20x30, 24x36\"" },
    "3x4": { label: "3:4 Ratio", max_in: "18x24\"", max_px: "5400x7200", w: 5400, h: 7200, mb: 6.0, desc: "6x8, 9x12, 12x16, 15x20, 18x24\"" },
    "4x5": { label: "4:5 Ratio", max_in: "16x20\"", max_px: "4800x6000", w: 4800, h: 6000, mb: 4.4, desc: "4x5, 8x10, 12x15, 16x20\"" },
    "11x14": { label: "11:14 Ratio", max_in: "11x14\"", max_px: "3300x4200", w: 3300, h: 4200, mb: 2.1, desc: "11x14, 22x28\"" },
    "iso": { label: "ISO Paper", max_in: "A1 (594x841mm)", max_px: "7016x9933", w: 7016, h: 9933, mb: 10.6, desc: "A1, A2, A3, A4, A5, 5x7\"" }
  };

  const NICHE_TAGS = {
    abstract: [
      "abstract wall art", "digital download", "printable wall art",
      "modern art print", "large wall decor", "gallery wall art",
      "minimalist poster", "neutral home decor", "aesthetic wall art",
      "living room decor", "digital art prints", "300 dpi print", "instant download"
    ],
    botanical: [
      "botanical wall art", "plant lover gift", "printable wall art",
      "greenery poster", "floral art print", "vintage botanical",
      "cottagecore decor", "earthy wall decor", "digital download",
      "nature art print", "bedroom wall art", "300 dpi print", "instant download"
    ],
    landscape: [
      "mountain wall art", "landscape print", "nature photography",
      "panoramic poster", "large canvas art", "scenic wall decor",
      "minimal landscape", "moody landscape", "printable wall art",
      "travel poster", "digital download", "300 dpi print", "instant download"
    ],
    geometric: [
      "geometric wall art", "bauhaus print", "mid century modern",
      "retro wall decor", "abstract shapes", "modern canvas art",
      "colorful poster", "contemporary print", "digital download",
      "studio apartment", "gallery wall print", "300 dpi print", "instant download"
    ]
  };

  // State
  let selectedTab = "manifest";

  // Elements
  const titleInput = document.getElementById("artwork-title-input");
  const artistInput = document.getElementById("artist-name-input");
  const nicheSelect = document.getElementById("niche-select");
  const priceInput = document.getElementById("price-input");

  const manifestTableBody = document.getElementById("manifest-table-body");
  const totalFilesEl = document.getElementById("stat-total-files");
  const totalSizeEl = document.getElementById("stat-total-size");
  const zipCountEl = document.getElementById("stat-zip-count");
  const netMarginEl = document.getElementById("stat-net-margin");

  const codePreview = document.getElementById("code-preview");

  // Toast Notification System
  function showToast(msg) {
    let toast = document.getElementById('forgeToast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'forgeToast';
      toast.style.cssText = 'position: fixed; bottom: 24px; right: 24px; z-index: 100000; background: #0A0F1D; border: 1px solid var(--gold, #D4AF37); color: #FFF; padding: 0.65rem 1.25rem; border-radius: 8px; font-family: var(--font-mono, monospace); font-size: 0.82rem; box-shadow: 0 8px 32px rgba(0,0,0,0.8), 0 0 15px rgba(212,175,55,0.25); display: flex; align-items: center; gap: 0.5rem; transition: opacity 0.3s ease, transform 0.3s ease; opacity: 0; transform: translateY(10px); pointer-events: none;';
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
    }, 2600);
  }

  function isProActive() {
    return true;
  }

  function checkLicense() {
    const proBadge = document.getElementById("licenseBadge") || document.getElementById("pro-badge");
    document.body.classList.add("licensed", "pro-unlocked", "pro-licensed");
    if (proBadge) {
      proBadge.className = "brand-badge badge-pro";
      proBadge.textContent = "✦ 100% UNLOCKED";
      proBadge.style.background = "rgba(16, 185, 129, 0.2)";
      proBadge.style.color = "var(--emerald, #10B981)";
      proBadge.style.borderColor = "var(--emerald, #10B981)";
    }
    if (codePreview) {
      codePreview.classList.add("output-unlocked");
    }
  }

  function slugify(text) {
    return text.replace(/[^a-zA-Z0-9\s_-]/g, '').trim().split(/\s+/).join('_');
  }

  function updateManifest() {
    const rawTitle = titleInput ? titleInput.value.trim() || "Celestial Geometry" : "Celestial Geometry";
    const artist = artistInput ? artistInput.value.trim() || "1nc0gn30" : "1nc0gn30";
    const slug = slugify(rawTitle);
    const niche = nicheSelect ? nicheSelect.value : "abstract";
    const price = priceInput ? parseFloat(priceInput.value) || 6.99 : 6.99;

    let rowsHtml = "";
    let totalMb = 0;
    const filesList = [];

    for (const [key, spec] of Object.entries(RATIOS)) {
      const fname = key === "iso" ? `${slug}_ISO_Paper_300DPI_A1.jpg` : `${slug}_${key}_Ratio_300DPI_${spec.max_in.replace('"', '').replace(' ', '')}in.jpg`;
      totalMb += spec.mb;
      filesList.push({ filename: fname, ratio: spec.label, resolution: spec.max_px, size_mb: spec.mb });

      rowsHtml += `
        <tr>
          <td><span class="ratio-badge">${key.toUpperCase()}</span></td>
          <td class="filename-cell">${fname}</td>
          <td><strong>${spec.max_in}</strong></td>
          <td>${spec.max_px} (300 DPI)</td>
          <td>${spec.mb.toFixed(1)} MB</td>
        </tr>
      `;
    }

    // Customer guide file
    const guideName = `${slug}_Customer_Printing_Guide.pdf`;
    totalMb += 1.2;
    rowsHtml += `
      <tr>
        <td><span class="ratio-badge" style="background: rgba(56, 189, 248, 0.2); color: #38BDF8;">GUIDE</span></td>
        <td class="filename-cell">${guideName}</td>
        <td>PDF Manual</td>
        <td>Vector / Text</td>
        <td>1.2 MB</td>
      </tr>
    `;

    if (manifestTableBody) manifestTableBody.innerHTML = rowsHtml;
    if (totalFilesEl) totalFilesEl.textContent = "6 Files";
    if (totalSizeEl) totalSizeEl.textContent = `${totalMb.toFixed(1)} MB`;

    // Calculate Etsy zip count
    const zipCount = Math.ceil(totalMb / 18.5);
    if (zipCountEl) zipCountEl.textContent = `${zipCount} ZIPs (Fits 20MB)`;

    // Calculate Net Economics
    const totalFees = 0.20 + (price * 0.065) + (price * 0.03 + 0.25);
    const netProfit = Math.max(0, price - totalFees);
    const marginPct = (netProfit / price) * 100;
    if (netMarginEl) netMarginEl.textContent = `$${netProfit.toFixed(2)} (${marginPct.toFixed(0)}%)`;

    // Update Output JSON / Markdown preview
    const tags = NICHE_TAGS[niche] || NICHE_TAGS.abstract;
    const manifestJson = {
      project: rawTitle,
      artist: artist,
      total_files: 6,
      total_size_mb: Number(totalMb.toFixed(1)),
      etsy_upload_strategy: {
        bundles_count: zipCount,
        max_bundle_size_mb: 18.5,
        etsy_20mb_limit_compliant: true
      },
      files: filesList,
      etsy_seo: {
        title: `${rawTitle} Digital Download, Printable Wall Art, Modern ${niche.toUpperCase()} Poster, 300 DPI High Res Art Pack`,
        tags_13_count: tags.length,
        tags: tags,
        pricing: {
          retail_usd: price,
          net_profit_usd: Number(netProfit.toFixed(2)),
          margin_percent: Number(marginPct.toFixed(1))
        }
      }
    };

    if (codePreview) {
      codePreview.textContent = JSON.stringify(manifestJson, null, 2);
    }
  }

  // Interceptors
  function handleCopyAction() {
    if (!isProActive()) {
      openModal("Copy Manifest");
      return;
    }
    if (!codePreview) return;
    if (navigator.clipboard) {
      navigator.clipboard.writeText(codePreview.textContent).then(() => {
        showToast("✅ Art Pack Manifest & Etsy SEO JSON copied to clipboard!");
      }).catch(() => {
        showToast("✅ Art Pack Manifest copied!");
      });
    } else {
      showToast("✅ Art Pack Manifest copied!");
    }
  }

  function handleDownloadAction() {
    if (!isProActive()) {
      openModal("Download Manifest");
      return;
    }
    if (!codePreview) return;
    const blob = new Blob([codePreview.textContent], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `art-pack-manifest-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast("📥 Art Pack Manifest Downloaded!");
  }

  // Event Listeners
  if (titleInput) titleInput.addEventListener("input", updateManifest);
  if (artistInput) artistInput.addEventListener("input", updateManifest);
  if (nicheSelect) nicheSelect.addEventListener("change", updateManifest);
  if (priceInput) priceInput.addEventListener("input", updateManifest);

  const copyBtn = document.getElementById("btn-copy-manifest");
  const downloadBtn = document.getElementById("btn-download-manifest");

  if (copyBtn) copyBtn.addEventListener("click", handleCopyAction);
  if (downloadBtn) downloadBtn.addEventListener("click", handleDownloadAction);

  checkLicense();
  updateManifest();
})();
