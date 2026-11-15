
from pathlib import Path
import csv
import numpy as np

from broken_scene import (
    _load,
    bug_inside_out,
    bug_stretched,
    _zfight_scene,
    TRI_COLS
)

import raster3d
from metrics import psnr, ssim
from ppm_io import write_ppm


OUTPUT = Path("lampiran/A3")
OUTPUT.mkdir(parents=True, exist_ok=True)

# Membaca model dan texture proyek
mesh, tex = _load()

results = []


def evaluate_bug(name, bad, fixed, reference):
    """Membandingkan render sebelum dan sesudah dengan referensi."""

    write_ppm(
        OUTPUT / f"A3_{name}_reference.ppm",
        reference
    )

    before_ssim = ssim(bad, reference)
    before_psnr = psnr(bad, reference)

    after_ssim = ssim(fixed, reference)
    after_psnr = psnr(fixed, reference)

    results.append({
        "bug": name,
        "ssim_before": before_ssim,
        "psnr_before_db": before_psnr,
        "ssim_after": after_ssim,
        "psnr_after_db": after_psnr
    })

    print(f"\n===== {name.upper()} =====")

    print(
        f"Before vs reference: "
        f"SSIM={before_ssim:.3f}, "
        f"PSNR={before_psnr:.2f} dB"
    )

    print(
        f"After vs reference : "
        f"SSIM={after_ssim:.3f}, "
        f"PSNR={after_psnr:.2f} dB"
    )


# -------------------------------------------------
# 1. INSIDE-OUT
# Referensi = render dengan winding yang benar
# -------------------------------------------------

bad, fixed, evidence = bug_inside_out(mesh, tex)

evaluate_bug(
    "inside_out",
    bad,
    fixed,
    fixed
)


# -------------------------------------------------
# 2. STRETCHED
# Referensi = render dengan matriks model benar
# -------------------------------------------------

bad, fixed, evidence = bug_stretched(mesh, tex)

evaluate_bug(
    "stretched",
    bad,
    fixed,
    fixed
)


# -------------------------------------------------
# 3. Z-FIGHTING
# Referensi = float-depth, near = 1.0
# -------------------------------------------------

scene = _zfight_scene()

camera = {
    "eye": (0, 1, 6),
    "center": (0, 1, -1),
    "cull_back": False,
    "far": 200,
    "tri_colors": TRI_COLS,
    "light_dir": (0, 0.2, 1)
}

bad, _, _ = raster3d.render(
    scene,
    w=192,
    h=192,
    near=1e-3,
    depth_bits=16,
    **camera
)

fixed, _, _ = raster3d.render(
    scene,
    w=192,
    h=192,
    near=1.0,
    depth_bits=16,
    **camera
)

reference, _, _ = raster3d.render(
    scene,
    w=192,
    h=192,
    near=1.0,
    depth_bits=None,
    **camera
)

evaluate_bug(
    "z_fighting",
    bad,
    fixed,
    reference
)


# -------------------------------------------------
# SIMPAN HASIL METRIK KE CSV
# -------------------------------------------------

csv_path = OUTPUT / "A3_reference_metrics.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "bug",
            "ssim_before",
            "psnr_before_db",
            "ssim_after",
            "psnr_after_db"
        ]
    )

    writer.writeheader()
    writer.writerows(results)


print("\n===== RINGKASAN A3 =====")

for item in results:
    print(
        f"{item['bug']:12s} | "
        f"SSIM: {item['ssim_before']:.3f} "
        f"-> {item['ssim_after']:.3f}"
    )

print("\nFile berhasil disimpan:")
print(csv_path)
print("Tiga gambar referensi berhasil dibuat.")
