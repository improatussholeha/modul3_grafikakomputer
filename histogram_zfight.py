
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt

from broken_scene import _zfight_scene, TRI_COLS
import raster3d

mesh = _zfight_scene()

camera = dict(
    eye=(0, 1, 6),
    center=(0, 1, -1),
    cull_back=False,
    far=200,
    tri_colors=TRI_COLS,
    light_dir=(0, 0.2, 1)
)

conditions = [
    ("Near 0.001 + 16-bit", 1e-3, 16),
    ("Near 1.0 + 16-bit", 1.0, 16),
    ("Float-depth reference", 1.0, None)
]

output = Path("lampiran/A3")
output.mkdir(parents=True, exist_ok=True)

results = {}

for name, near, bits in conditions:
    _, depth, _ = raster3d.render(
        mesh,
        w=192,
        h=192,
        near=near,
        depth_bits=bits,
        **camera
    )

    valid = depth[np.isfinite(depth)]

    # Konversi depth menjadi kode 16-bit
    codes = np.rint(
        (valid * 0.5 + 0.5) * 65536
    ).astype(np.int64)

    codes = np.clip(codes, 0, 65536)

    unique, counts = np.unique(
        codes,
        return_counts=True
    )

    results[name] = (unique, counts)

    print("\n", name)
    print("Pixel valid:", len(valid))
    print("Depth NDC:", valid.min(), "-", valid.max())
    print("Jumlah kode depth berbeda:", len(unique))


# Simpan data histogram ke CSV
csv_path = output / "A3_zfight_depth_histogram.csv"

with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Depth code"] + list(results.keys()))

    all_codes = sorted(set(
        int(v)
        for unique, _ in results.values()
        for v in unique
    ))

    maps = {
        name: dict(zip(unique, counts))
        for name, (unique, counts) in results.items()
    }

    for code in all_codes:
        writer.writerow(
            [code] + [
                int(maps[name].get(code, 0))
                for name in results
            ]
        )


# Buat grafik histogram
plt.figure(figsize=(12, 6))

for name, (unique, counts) in results.items():
    plt.plot(
        unique,
        counts,
        marker="o",
        label=name
    )

plt.title("Histogram Depth pada Z-Fighting")
plt.xlabel("Kode Depth 16-bit")
plt.ylabel("Jumlah Pixel")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

graph_path = output / "A3_zfight_depth_histogram.png"
plt.savefig(graph_path, dpi=150)
plt.close()

print("\nBerhasil membuat:")
print(graph_path)
print(csv_path)
