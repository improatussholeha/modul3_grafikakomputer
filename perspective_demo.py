"""A5 E4 demonstration: naive vs perspective-correct UV interpolation."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

OUT = Path("lampiran/A5")
OUT.mkdir(parents=True, exist_ok=True)
W = H = 420

# Screen-space triangle vertices: left, right, and top.
xy = np.array([[45.0, 340.0], [375.0, 340.0], [210.0, 45.0]])
uv = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, 1.0]])
w_eye = np.array([1.0, 9.0, 3.0])

# High-frequency checker texture makes interpolation distortion visible.
T = 128
checker = np.zeros((T, T, 3), dtype=np.uint8)
cell = 8
for y in range(T):
    for x in range(T):
        value = 235 if ((x // cell + y // cell) % 2 == 0) else 35
        checker[y, x] = (value, value, value)

# Pixel-centre barycentric interpolation.
A, B, C = xy
area = (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])
yy, xx = np.mgrid[0:H, 0:W]
px, py = xx + 0.5, yy + 0.5
lA = ((C[0]-B[0])*(py-B[1]) - (C[1]-B[1])*(px-B[0])) / area
lB = ((A[0]-C[0])*(py-C[1]) - (A[1]-C[1])*(px-C[0])) / area
lC = 1.0 - lA - lB
inside = (lA >= 0) & (lB >= 0) & (lC >= 0)
weights = np.stack([lA, lB, lC], axis=-1)

# Naive screen-linear UV.
uv_naive = weights @ uv

# Perspective-correct UV = (sum(lambda * uv/w)) / sum(lambda/w).
inv_w = 1.0 / w_eye
uv_over_w = uv * inv_w[:, None]
num = weights @ uv_over_w
den = weights @ inv_w
uv_pc = num / np.maximum(den[..., None], 1e-12)

# Bilinear sampler for the checkerboard, with repeat wrapping.
def sample(tex, coords):
    th, tw = tex.shape[:2]
    u = np.mod(coords[..., 0], 1.0) * (tw - 1)
    v = np.mod(coords[..., 1], 1.0) * (th - 1)
    x0 = np.floor(u).astype(int); y0 = np.floor(v).astype(int)
    x1 = np.clip(x0 + 1, 0, tw - 1); y1 = np.clip(y0 + 1, 0, th - 1)
    fx = (u - x0)[..., None]; fy = (v - y0)[..., None]
    a = tex[y0, x0] * (1-fx) + tex[y0, x1] * fx
    b = tex[y1, x0] * (1-fx) + tex[y1, x1] * fx
    return (a * (1-fy) + b * fy).astype(np.uint8)

images = []
for coords, label in [(uv_naive, "Naive UV"), (uv_pc, "Perspective-correct UV")]:
    img = np.zeros((H, W, 3), dtype=np.uint8)
    sampled = sample(checker, coords)
    img[inside] = sampled[inside]
    pil = Image.fromarray(img, "RGB")
    d = ImageDraw.Draw(pil)
    d.polygon([tuple(p) for p in xy.astype(int)], outline=(40, 180, 255), width=2)
    # Mark the midpoint of the L-R edge, where E4 is evaluated.
    d.ellipse((205, 333, 215, 343), fill=(255, 40, 40))
    d.text((12, 12), label, fill=(255, 255, 0))
    images.append(pil)

panel = Image.new("RGB", (W * 2, H + 42), "#202020")
d = ImageDraw.Draw(panel)
d.text((12, 12), "Naive UV interpolation", fill="white")
d.text((W + 12, 12), "Perspective-correct UV interpolation", fill="white")
panel.paste(images[0], (0, 42))
panel.paste(images[1], (W, 42))
panel.save(OUT / "A5_uv_naive_vs_perspective_correct.png")

# Exact Module 3 E4 midpoint values on the horizontal edge L-R.
u_naive_mid = 0.5
u_over_w_mid = 0.5 * (0.0 / 1.0 + 1.0 / 9.0)
one_over_w_mid = 0.5 * (1.0 / 1.0 + 1.0 / 9.0)
u_pc_mid = u_over_w_mid / one_over_w_mid

print("E4 -- midpoint of floor edge")
print(f"  Naive linear u: {u_naive_mid:.3f}")
print(f"  Perspective-correct u: {u_pc_mid:.3f}")
print("  Expected module values: 0.500 and 0.100")
print("Wrote lampiran/A5/A5_uv_naive_vs_perspective_correct.png")
