"""Lab 2 A5: four-level gamma-correct mipmap experiment."""
from pathlib import Path
import csv
import numpy as np
from PIL import Image, ImageDraw

from objio import load_obj
from ppm_io import read_ppm, write_ppm
from transforms import translate, rot_y, scale
from raster3d import render, build_mip_pyramid

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "lampiran" / "A5"
OUT.mkdir(parents=True, exist_ok=True)

model_path = ROOT / "data" / "pusaka_model.obj"
tex_path = ROOT / "data" / "relief.ppm"
mesh = load_obj(model_path)
texture = read_ppm(str(tex_path))
model = translate((0, 0, 0)) @ rot_y(35) @ scale((1.4, 1.4, 1.4))

# Preserve the default camera direction, but move the camera five times
# farther from the target to create strong texture minification.
center = np.array((0.0, 0.7, 0.0))
base_eye = np.array((2.6, 2.0, 3.4))
eye_far = center + 5.0 * (base_eye - center)

mips = build_mip_pyramid(texture, levels=4)
print("Mipmap levels (width x height):")
for index, level in enumerate(mips):
    print(f"  Level {index}: {level.shape[1]} x {level.shape[0]}")

common = dict(
    w=512,
    h=512,
    tex_u8=texture,
    model=model,
    eye=tuple(eye_far),
    center=tuple(center),
    near=1.0,
    far=100.0,
)

img_no, depth_no, filled_no = render(mesh, **common)
img_mip, depth_mip, filled_mip = render(mesh, **common, mip_chain=mips)

p_no = OUT / "A5_temple_no_mipmap.ppm"
p_mip = OUT / "A5_temple_with_mipmap.ppm"
write_ppm(str(p_no), img_no)
write_ppm(str(p_mip), img_mip)

# Compare high-frequency energy inside the rendered surface only.
def high_frequency_energy(img, depth):
    gray = (
        0.2126 * img[..., 0].astype(np.float64)
        + 0.7152 * img[..., 1].astype(np.float64)
        + 0.0722 * img[..., 2].astype(np.float64)
    )
    valid = np.isfinite(depth)
    dx_mask = valid[:, 1:] & valid[:, :-1]
    dy_mask = valid[1:, :] & valid[:-1, :]
    dx = gray[:, 1:] - gray[:, :-1]
    dy = gray[1:, :] - gray[:-1, :]
    energies = []
    if np.any(dx_mask):
        energies.append(float(np.mean(dx[dx_mask] ** 2)))
    if np.any(dy_mask):
        energies.append(float(np.mean(dy[dy_mask] ** 2)))
    return float(np.mean(energies)) if energies else 0.0

energy_no = high_frequency_energy(img_no, depth_no)
energy_mip = high_frequency_energy(img_mip, depth_mip)
reduction = (1.0 - energy_mip / energy_no) * 100.0 if energy_no > 0 else 0.0

print("\nFar-camera render:")
print("  Eye:", tuple(np.round(eye_far, 3)))
print("  Model triangles:", mesh.n_tris)
print("  Filled fragments without mipmap:", filled_no)
print("  Filled fragments with mipmap:", filled_mip)
print(f"  High-frequency energy without mipmap: {energy_no:.4f}")
print(f"  High-frequency energy with mipmap:    {energy_mip:.4f}")
print(f"  Energy reduction: {reduction:.2f}%")

csv_path = OUT / "A5_mipmap_metrics.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Condition", "High-frequency energy", "Filled fragments"])
    writer.writerow(["Without mipmap", energy_no, filled_no])
    writer.writerow(["With 4-level mipmap", energy_mip, filled_mip])

# Create PNGs and a side-by-side visual comparison.
Image.fromarray(img_no, "RGB").save(OUT / "A5_temple_no_mipmap.png")
Image.fromarray(img_mip, "RGB").save(OUT / "A5_temple_with_mipmap.png")

panel = Image.new("RGB", (1024, 550), "#202020")
draw = ImageDraw.Draw(panel)
draw.text((12, 12), "Without mipmap", fill="white")
draw.text((524, 12), "With 4-level gamma-correct mipmap", fill="white")
panel.paste(Image.fromarray(img_no, "RGB"), (0, 38))
panel.paste(Image.fromarray(img_mip, "RGB"), (512, 38))
panel.save(OUT / "A5_mipmap_comparison.png")

print("\nFiles written:")
for path in [p_no, p_mip, csv_path, OUT / "A5_temple_no_mipmap.png", OUT / "A5_temple_with_mipmap.png", OUT / "A5_mipmap_comparison.png"]:
    print(" ", path.relative_to(ROOT))
