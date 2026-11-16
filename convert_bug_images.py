"""Convert the six broken-scene PPM renders to PNG for the A3 appendix."""
from pathlib import Path
from PIL import Image

source = Path("out")
destination = Path("lampiran/A3")
destination.mkdir(parents=True, exist_ok=True)

for filename in sorted(source.glob("bug_*_*.ppm")):
    target = destination / f"{filename.stem}.png"
    Image.open(filename).convert("RGB").save(target)
    print("OK:", target)
