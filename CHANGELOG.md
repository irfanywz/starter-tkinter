# CHANGELOG

Format: versi terbaru di atas. Setiap perubahan wajib dicatat di sini dan versi dinaikkan (`scripts/bump_version.py`).

## 0.2.0
- Struktur folder diubah jadi feature-based: `shell/` (kerangka), `shared/` (lintas fitur), `features/<nama>/` (satu folder per fitur) dengan registry manual di `features/__init__.py`.
- `meta.py` + `paths.py` digabung jadi `config.py`; tambah `feature_data()` untuk folder data per fitur.
- `logger.py` + `errors.py` digabung jadi `shared/log.py`.
- 3 script di `scripts/` digabung jadi satu `dev.py` (bump | rename | icon).
- Perbaikan kecil: dropdown tema di Pengaturan tidak lagi memakai `winfo_children()`.
- ARCHITECTURE dipersingkat dan ditulis ulang sesuai struktur baru.

## 0.1.0
- Versi awal starter: customtkinter, sidebar + halaman, tray, single instance, toast, simpan posisi window, tema, worker, error handler global.
- Build exe + zip dengan struktur `Nama.exe`, `Nama_Data/`, `Nama_System/`.
- Script: `make_icon.py`, `bump_version.py`, `rename_app.py`.
