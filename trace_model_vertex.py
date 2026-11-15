
import numpy as np

from objio import load_obj
from transforms import (
    translate, rot_y, scale,
    look_at, perspective, viewport
)

np.set_printoptions(precision=3, suppress=True)

# 1. Membaca model candi
mesh = load_obj("data/pusaka_model.obj")

# Menggunakan vertex pertama dari model
vertex_index = 0
p = np.append(mesh.positions[vertex_index], 1.0)

# 2. Menentukan matriks Model
M = (
    translate((0, 0, 0))
    @ rot_y(35)
    @ scale((1.4, 1.4, 1.4))
)

# 3. Menentukan matriks View
V = look_at(
    eye=(2.6, 2.0, 3.4),
    center=(0, 0.7, 0)
)

# 4. Menentukan matriks Projection
P = perspective(
    fovy_deg=45,
    aspect=1.0,
    near=1.0,
    far=14.0
)

# 5. Menghitung perjalanan vertex
world = M @ p
view = V @ world
clip = P @ view
ndc = clip[:3] / clip[3]

# Ukuran layar 512 x 512
screen = viewport(ndc[None, :], 512, 512)[0]

print("===== A1: VERTEX TRACE =====")
print("Jumlah vertex :", len(mesh.positions))
print("Jumlah segitiga:", mesh.n_tris)
print("Vertex index  :", vertex_index)

print("\n1. OBJECT SPACE")
print("Object =", p)

print("\n2. WORLD SPACE")
print("World  =", world)

print("\n3. VIEW SPACE")
print("View   =", view)

print("\n4. CLIP SPACE")
print("Clip   =", clip)

print("\n5. NDC SPACE")
print("NDC    =", ndc)

print("\n6. SCREEN SPACE")
print("Screen =", screen)

# 6. Analisis matriks M dan V
axes = {
    "Origin": [0, 0, 0, 1],
    "+X": [1, 0, 0, 1],
    "+Y": [0, 1, 0, 1],
    "+Z": [0, 0, 1, 1]
}

print("\n===== MODEL MATRIX (M) =====")
print(M)

for name, point in axes.items():
    print(name, "->", M @ np.array(point, dtype=float))

print("\n===== VIEW MATRIX (V) =====")
print(V)

for name, point in axes.items():
    print(name, "->", V @ np.array(point, dtype=float))
