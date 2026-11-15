
from pathlib import Path
from time import perf_counter
from statistics import median, mean
import csv
import platform
import sys

import numpy as np

from objio import load_obj
from ppm_io import read_ppm
from transforms import translate, rot_y, scale
import raster3d
import raytrace


# Konfigurasi pengujian
MODEL_PATH = "data/pusaka_model.obj"
TEXTURE_PATH = "data/relief.ppm"

WIDTH = 256
HEIGHT = 256
WARMUP = 1
REPEATS = 5

output = Path("lampiran/A4")
output.mkdir(parents=True, exist_ok=True)

# Membaca model dan texture sebelum pengukuran
mesh = load_obj(MODEL_PATH)
texture = read_ppm(TEXTURE_PATH)

model = (
    translate((0, 0, 0))
    @ rot_y(35)
    @ scale((1.4, 1.4, 1.4))
)

# Kedua renderer memakai model, texture, kamera,
# dan resolusi yang sama.
def render_raster():
    return raster3d.render(
        mesh,
        w=WIDTH,
        h=HEIGHT,
        tex_u8=texture,
        model=model
    )


def render_raytrace():
    return raytrace.render(
        mesh,
        w=WIDTH,
        h=HEIGHT,
        tex_u8=texture,
        model=model
    )


def measure(function, name):
    print(f"\nMengukur {name}...")

    # Warm-up tidak dimasukkan ke hasil pengukuran.
    function()

    times = []

    for i in range(REPEATS):
        start = perf_counter()
        function()
        elapsed = perf_counter() - start

        times.append(elapsed)

        print(
            f"  Percobaan {i + 1}: "
            f"{elapsed * 1000:.3f} ms"
        )

    return {
        "times": times,
        "median": median(times),
        "mean": mean(times),
        "fps": 1.0 / median(times)
    }


print("===== A4: RASTERIZER VS RAY TRACER =====")
print("OS       :", platform.platform())
print("Python   :", sys.version.split()[0])
print("NumPy    :", np.__version__)
print("Model    :", MODEL_PATH)
print("Triangles:", mesh.n_tris)
print("Resolution:", f"{WIDTH} x {HEIGHT}")
print("Warm-up  :", WARMUP)
print("Repeats  :", REPEATS)

raster_result = measure(render_raster, "Rasterizer")
ray_result = measure(render_raytrace, "Ray tracer")

ratio = ray_result["median"] / raster_result["median"]

print("\n===== HASIL PENGUKURAN =====")

print(
    f"Rasterizer median : "
    f"{raster_result['median'] * 1000:.3f} ms"
)

print(
    f"Ray tracer median : "
    f"{ray_result['median'] * 1000:.3f} ms"
)

print(f"Rasio RT / Raster : {ratio:.2f}x")

print(
    f"Rasterizer FPS    : "
    f"{raster_result['fps']:.2f}"
)

print(
    f"Ray tracer FPS    : "
    f"{ray_result['fps']:.2f}"
)

# Simpan data hasil pengukuran ke CSV
csv_path = output / "A4_benchmark.csv"

with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "Renderer",
        "Median_ms",
        "Mean_ms",
        "FPS"
    ])

    writer.writerow([
        "Rasterizer",
        raster_result["median"] * 1000,
        raster_result["mean"] * 1000,
        raster_result["fps"]
    ])

    writer.writerow([
        "Ray tracer",
        ray_result["median"] * 1000,
        ray_result["mean"] * 1000,
        ray_result["fps"]
    ])

# Simpan ringkasan untuk laporan
summary_path = output / "A4_benchmark_summary.txt"

with open(summary_path, "w", encoding="utf-8") as f:
    f.write("A4 - BENCHMARK RENDERER\n")
    f.write(f"Model: {MODEL_PATH}\n")
    f.write(f"Triangles: {mesh.n_tris}\n")
    f.write(f"Resolution: {WIDTH}x{HEIGHT}\n")
    f.write(f"Rasterizer median: {raster_result['median']*1000:.3f} ms\n")
    f.write(f"Ray tracer median: {ray_result['median']*1000:.3f} ms\n")
    f.write(f"Ratio RT/Raster: {ratio:.2f}x\n")

print("\nFile berhasil disimpan:")
print(csv_path)
print(summary_path)
