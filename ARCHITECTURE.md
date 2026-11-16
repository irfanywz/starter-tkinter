# ARCHITECTURE

Dokumen ini ditulis agar AI agent / developer lain bisa cepat paham. Baca ini dulu sebelum mengubah kode.

## Stack
Python >= 3.11, uv, customtkinter (UI), pystray + Pillow (tray), PyInstaller (build).
Dependency lain terpasang untuk dipakai aplikasi turunan bila perlu: pillow-avif-plugin (AVIF, auto-register di `main.py`), tkinterdnd2 (drag & drop), pywebview.

## Struktur folder
```
main.py                  entry point (tambah src/ ke sys.path lalu panggil app.main.run)
build.py                 build exe + zip (PyInstaller)
pyproject.toml           dependency & versi
assets/                  icon.ico, icon.png (ikut dibundle ke exe)
scripts/                 make_icon.py, bump_version.py, rename_app.py
src/app/
  meta.py                APP_NAME, APP_VERSION, APP_ID  <- satu-satunya sumber nama & versi
  paths.py               SEMUA path (BASE_DIR, DATA_DIR, ASSETS_DIR, ...)
  main.py                alur start
  core/                  logika tanpa UI: logger, settings, single_instance, worker, errors, tray
  ui/
    app_window.py        window utama (sidebar, toast, tray, simpan posisi window)
    pages/               satu file = satu halaman; registry di pages/__init__.py (PAGES)
    widgets/             komponen UI reusable (toast.py)
```

## Aturan penting
1. **Nama & versi hanya di `meta.py`** (diubah lewat script). `pyproject.toml` disinkronkan oleh `bump_version.py`.
2. **Path hanya dari `paths.py`.** Saat frozen: `BASE_DIR` = folder exe, `RESOURCE_DIR` = `<APP_ID>_System`. Saat dev: root proyek.
3. **Semua data yang disimpan masuk `<APP_ID>_Data/`** (`settings.json`, `logs/`, dan data aplikasi turunan). Jangan tulis ke tempat lain.
4. **UI hanya disentuh dari thread UI.** Dari thread lain gunakan `window.run_on_ui(fn)`. Tugas berat: `core.worker.run_in_background(fn, window.run_on_ui, on_done, on_error)`.
5. **Halaman baru**: salin `pages/home.py`, turunkan `BasePage`, isi `build()`, daftarkan di `PAGES`. Halaman punya akses `self.win` (settings, `toast()`, `run_on_ui()`).
6. **Pengaturan baru**: tambah key di `DEFAULTS` pada `core/settings.py`, baca/tulis lewat `settings.get/set`.
7. Error tak tertangani otomatis masuk log (`Data/logs/app.log`) dan tampil di dialog.

## Alur start (`app/main.py`)
`ensure_dirs` -> `setup_logging` -> `SingleInstance.acquire` (jika gagal, instance lama disuruh tampil lalu keluar) -> `AppWindow(Settings)` -> pasang handler error global -> `mainloop`.

## Tray & lifecycle
Tray berjalan di thread sendiri (`run_detached`); callback-nya dilempar ke UI lewat `run_on_ui`. Tombol X: jika `close_to_tray` aktif dan tray hidup, window disembunyikan; selain itu keluar. Menu tray "Keluar" memanggil `quit_app`. Posisi window & status maximized disimpan ke settings saat ditutup.

## Build (`build.py`)
PyInstaller onedir, windowed, `--contents-directory <APP_ID>_System` (menggantikan `_internal`), icon dari `assets/icon.ico`, `assets/` dibundle via `--add-data`.
Setelah build, folder `dist/<APP_ID>` di-rename ke `dist/<APP_NAME>`, lalu di-zip menjadi `dist/<APP_NAME> <VERSI>.zip` dengan root folder `<APP_NAME>` (tanpa versi).
Bila aplikasi turunan memakai library lain yang butuh hidden import, tambahkan di `build.py`.

## Alur kerja perubahan
Setiap perubahan: (1) kerjakan, (2) catat di `CHANGELOG.md`, (3) `scripts/bump_version.py`, (4) perbarui dokumen ini jika arsitektur berubah.

## Catatan
- Window memakai frame native (frameless Tkinter rawan bug di Windows), bukan custom titlebar.
- Tray butuh `assets/icon.png`; kalau gagal dibuat, aplikasi tetap jalan dan tombol X langsung keluar.
