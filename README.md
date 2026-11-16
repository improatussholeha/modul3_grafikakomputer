# Praktikum Grafika Komputer – Modul 3

## Transformasi 3D, Proyeksi, Texture Mapping, dan Real-Time Rendering

Repository ini berisi implementasi dan pengujian praktikum Grafika Komputer Modul 3 yang membahas transformasi objek 3D, sistem koordinat, proyeksi perspektif, rasterization, ray tracing, texture mapping, mipmap, dan real-time rendering menggunakan Three.js.

## Repository

- **GitHub:** https://github.com/improatussholeha/modul3_grafikakomputer
- **Viewer lokal:** http://localhost:3001/web/
- **GitHub Pages:** https://improatussholeha.github.io/modul3_grafikakomputer/web/ (setelah deployment Pages aktif).

## Teknologi yang Digunakan

- Python 3.14.x (64-bit)
- NumPy 2.5.5
- Pillow 13.0.0
- Matplotlib 3.11.2
- JavaScript
- Three.js 0.160.0
- HTML dan CSS

## Struktur Repository

```text
modul3_grafikakomputer/
├── data/
│   ├── pusaka_model.obj
│   └── relief.ppm
├── lampiran/
│   ├── A1/
│   ├── A2/
│   ├── A3/
│   ├── A4/
│   ├── A5/
│   └── A6/
├── ref/
├── web/
│   ├── index.html
│   └── viewer.js
├── make_model.py
├── transforms.py
├── raster3d.py
├── raytrace.py
├── tests.py
├── requirements.txt
└── README.md
```

## Instalasi dan Menjalankan Program

### 1. Clone Repository

```bash
git clone https://github.com/improatussholeha/modul3_grafikakomputer.git
cd modul3_grafikakomputer
```

### 2. Membuat Virtual Environment

```bash
python -m venv .venv
```

Aktifkan pada Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalasi Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Membuat Model 3D

```bash
python make_model.py
```

### 5. Menjalankan Pengujian

```bash
python tests.py
```

Hasil pengujian yang diharapkan:

```text
ALL CHECKS PASSED
```

### 6. Menjalankan Viewer 3D

Jalankan server dari direktori utama repository:

```bash
python -m http.server 3001
```

Buka browser dan akses:

http://localhost:3001/web/

Viewer menggunakan Three.js untuk menampilkan model 3D bertekstur secara real-time.

## Implementasi Praktikum

### A1. Transformasi dan Coordinate Space
Membahas object space, world space, view space, clip space, NDC, dan screen space.

### A2. Pipeline Rendering
Implementasi pipeline rendering dari transformasi koordinat, projection, rasterization, z-buffer, hingga ray tracing.

### A3. Diagnosis dan Perbaikan Bug
Pengujian dan perbaikan tiga masalah:
- Inside-out geometry.
- Z-fighting.
- Stretched transformation.

### A4. Rasterization vs Ray Tracing
Perbandingan performa kedua metode rendering berdasarkan frame-time dan FPS.

### A5. Texture Sampling dan Mipmap
Pengujian perspective-correct texture mapping dan pengaruh mipmap terhadap detail tekstur.

### A6. Reproducibility
Pengujian ulang proyek menggunakan clean clone, virtual environment baru, instalasi dependencies, dan pengujian otomatis.

## Hasil Verifikasi

Pengujian clean clone berhasil dilakukan dengan hasil:

- Dependencies berhasil diinstal.
- Model 3D berhasil dibuat.
- Pengujian otomatis menghasilkan `ALL CHECKS PASSED`.
- Viewer Three.js berhasil dijalankan melalui server lokal.
- File model OBJ dan texture PPM berhasil dimuat oleh browser.

## Keterbatasan

Model Pusaka3D yang digunakan merupakan model fallback bawaan dengan 180 segitiga. Jumlah ini belum mencapai target model mandiri minimal 200 segitiga.

## Dokumentasi dan Lampiran

Bukti pelaksanaan praktikum tersedia pada folder `lampiran/A1` sampai `lampiran/A6`, meliputi screenshot pengujian, hasil rendering, analisis bug, benchmark, texture mapping, dan reproducibility.

---

**Praktikum Grafika Komputer – Modul 3**  
S1 Informatika | Universitas Muhammadiyah Surabaya