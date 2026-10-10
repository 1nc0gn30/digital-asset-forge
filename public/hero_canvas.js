/**
 * Digital Asset Forge - Kinetic Hero Canvas ("The Sovereign Tessellation Matrix")
 * Pure HTML5 Canvas 60fps interactive visualizer with zero external dependencies.
 */

(function () {
  const canvas = document.getElementById("hero-canvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  let width, height;
  let mouse = { x: -1000, y: -1000, active: false };

  // Aspect ratio geometries to render
  const FRAMES = [
    { id: "2:3", ratio: 2 / 3, color: "#FFDF70", strokeWidth: 2, scale: 0.92, label: "2:3 Ratio (24x36\")" },
    { id: "3:4", ratio: 3 / 4, color: "#38BDF8", strokeWidth: 1.8, scale: 0.82, label: "3:4 Ratio (18x24\")" },
    { id: "4:5", ratio: 4 / 5, color: "#10B981", strokeWidth: 1.6, scale: 0.72, label: "4:5 Ratio (16x20\")" },
    { id: "11:14", ratio: 11 / 14, color: "#F59E0B", strokeWidth: 1.4, scale: 0.62, label: "11:14 Ratio (11x14\")" },
    { id: "ISO", ratio: 1 / 1.414, color: "#A855F7", strokeWidth: 1.2, scale: 0.52, label: "ISO A1-A5" },
  ];

  // Floating pixel particles
  const PARTICLES = [];
  const PARTICLE_COUNT = 24;

  function resize() {
    const rect = canvas.parentElement.getBoundingClientRect();
    width = canvas.width = rect.width;
    height = canvas.height = Math.max(280, rect.height || 360);
  }

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    PARTICLES.push({
      x: Math.random(),
      y: Math.random(),
      size: 1.5 + Math.random() * 2,
      vx: (Math.random() - 0.5) * 0.001,
      vy: (Math.random() - 0.5) * 0.001,
      color: Math.random() > 0.5 ? "#FFDF70" : "#38BDF8"
    });
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);

    const time = performance.now() * 0.001;
    const centerX = width * 0.65; // Place toward right side so overlay text has breathing room
    const centerY = height * 0.5;
    const baseH = Math.min(height * 0.75, 240);

    // Subtle background grid
    ctx.save();
    ctx.strokeStyle = "rgba(255, 255, 255, 0.03)";
    ctx.lineWidth = 1;
    const gridSize = 40;
    for (let x = 0; x < width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    for (let y = 0; y < height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }
    ctx.restore();

    // Floating particles
    ctx.save();
    for (let p of PARTICLES) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0) p.x = 1;
      if (p.x > 1) p.x = 0;
      if (p.y < 0) p.y = 1;
      if (p.y > 1) p.y = 0;

      ctx.fillStyle = p.color;
      ctx.globalAlpha = 0.35;
      ctx.beginPath();
      ctx.arc(p.x * width, p.y * height, p.size, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();

    // Draw Nested Aspect Ratio Frames
    ctx.save();
    ctx.translate(centerX, centerY);

    // Mouse tilt interaction
    if (mouse.active) {
      const tiltX = (mouse.x - centerX) * 0.0003;
      const tiltY = (mouse.y - centerY) * 0.0003;
      ctx.rotate(tiltX);
    }

    for (let i = 0; i < FRAMES.length; i++) {
      const f = FRAMES[i];
      const h = baseH * f.scale;
      const w = h * f.ratio;
      const x = -w / 2;
      const y = -h / 2;

      const pulse = Math.sin(time * 2 + i * 0.8) * 2;

      ctx.save();
      ctx.strokeStyle = f.color;
      ctx.lineWidth = f.strokeWidth;
      ctx.shadowColor = f.color;
      ctx.shadowBlur = 8;
      ctx.globalAlpha = 0.85;

      // Rounded rectangle frame
      ctx.beginPath();
      ctx.roundRect(x - pulse * 0.5, y - pulse * 0.5, w + pulse, h + pulse, 4);
      ctx.stroke();

      // Corner crop tick marks
      const tick = 8;
      ctx.lineWidth = 2;
      // Top-Left
      ctx.beginPath();
      ctx.moveTo(x - 4, y + tick);
      ctx.lineTo(x - 4, y - 4);
      ctx.lineTo(x + tick, y - 4);
      ctx.stroke();
      // Bottom-Right
      ctx.beginPath();
      ctx.moveTo(x + w + 4, y + h - tick);
      ctx.lineTo(x + w + 4, y + h + 4);
      ctx.lineTo(x + w - tick, y + h + 4);
      ctx.stroke();

      // Micro Label
      ctx.font = "9px 'Space Grotesk', sans-serif";
      ctx.fillStyle = f.color;
      ctx.fillText(f.id, x + 6, y + 14);

      ctx.restore();
    }

    // Central 300 DPI Crosshair
    ctx.strokeStyle = "#FFDF70";
    ctx.lineWidth = 1;
    ctx.setLineDash([2, 4]);
    ctx.beginPath();
    ctx.moveTo(-baseH * 0.4, 0);
    ctx.lineTo(baseH * 0.4, 0);
    ctx.moveTo(0, -baseH * 0.4);
    ctx.lineTo(0, baseH * 0.4);
    ctx.stroke();

    ctx.restore();

    requestAnimationFrame(draw);
  }

  window.addEventListener("resize", resize);
  canvas.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
    mouse.active = true;
  });
  canvas.addEventListener("mouseleave", () => {
    mouse.active = false;
  });

  resize();
  draw();
})();
