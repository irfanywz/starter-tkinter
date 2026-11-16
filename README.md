# Starter (Tkinter / customtkinter)

Base utama untuk aplikasi GUI Tkinter supaya struktur folder **selalu seragam** antar aplikasi.
Untuk penjelasan arsitektur (terutama bagi AI agent), baca [ARCHITECTURE.md](ARCHITECTURE.md). Riwayat perubahan ada di [CHANGELOG.md](CHANGELOG.md).

## Isi
- customtkinter, sidebar + halaman (tinggal tambah file di `ui/pages/`)
- Tray icon (tutup window = sembunyi ke tray), single instance, toast di tengah bawah
- Simpan posisi window & status maximized, tema System/Light/Dark
- Helper background worker, penangkap error global, log rotasi
- Build exe + zip otomatis dengan struktur folder tetap

## Menjalankan
```
uv sync
uv run python main.py
```

## Membuat aplikasi baru dari starter
1. Salin folder ini, ganti nama foldernya.
2. `uv run python scripts/rename_app.py "Nama Aplikasi"`
3. Ganti `assets/icon.ico` dan `assets/icon.png` dengan icon asli (nama file tetap).
4. Tambah halaman di `src/app/ui/pages/`, daftarkan di `pages/__init__.py`.

## Build
```
uv run python build.py
```
Hasil di `dist/`:
```
Nama Aplikasi/
  NamaAplikasi.exe
  NamaAplikasi_System/     <- _internal milik PyInstaller (sudah di-rename)
  NamaAplikasi_Data/       <- dibuat otomatis saat pertama jalan; semua data tersimpan di sini
Nama Aplikasi 0.1.0.zip    <- root folder di dalam zip: "Nama Aplikasi" (tanpa versi)
```

## Setiap perubahan
Catat di `CHANGELOG.md` dan naikkan versi: `uv run python scripts/bump_version.py patch|minor|major`.
