# ARCHITECTURE

Baca ini dulu sebelum mengubah kode. Dokumen ini ditulis agar developer maupun AI agent cepat paham.

## Stack
Python >= 3.11, uv, customtkinter (UI), pystray + Pillow (tray), PyInstaller (build).
Dependency lain sudah terpasang untuk aplikasi turunan: pillow-avif-plugin (auto-register di `main.py`), tkinterdnd2, pywebview.

## Peta folder
```
main.py            entry point (menambah src/ ke sys.path, memanggil app.main.run)
build.py           build exe + zip
dev.py             bump | rename | icon
assets/            icon.ico, icon.png (ikut dibundle)
src/app/
  config.py        nama, versi, SEMUA path, feature_data()
  main.py          alur start
  shell/           kerangka aplikasi (jarang diubah): window.py, tray.py, single_instance.py
  shared/          dipakai lintas fitur: settings.py, log.py, worker.py, toast.py, page.py (BasePage)
  features/        SEMUA fitur: 1 folder = 1 fitur
    __init__.py    registry FEATURES (urutan = urutan sidebar)
    home/  settings/  about/     masing-masing berisi page.py
```

## Aturan
1. **Satu fitur = satu folder** `features/<nama>/`: `page.py` (UI), opsional `service.py` (logika) dan `models.py`.
2. **Fitur tidak boleh import fitur lain.** Yang dipakai bersama dipindah ke `shared/`.
3. `shell/` dan `shared/` tidak berisi logika fitur.
4. **Fitur baru**: buat `features/<nama>/page.py` (turunan `BasePage`, isi `build()`), tambah 1 baris di `FEATURES`. Registry sengaja manual (bukan auto-scan) agar PyInstaller pasti membundle modulnya.
5. **Nama & versi hanya di `config.py`**, diubah lewat `dev.py`. **Path hanya dari `config.py`.**
6. **Semua data masuk `<APP_ID>_Data/`.** Data milik fitur: `feature_data("<nama>")` -> `<APP_ID>_Data/<nama>/`. Settings global: `shared/settings.py` (tambah key di `DEFAULTS`).
7. **UI hanya disentuh dari thread UI.** Dari thread lain: `window.run_on_ui(fn)`. Tugas berat: `run_in_background(fn, window.run_on_ui, on_done, on_error)`.
8. Halaman punya `self.win` (AppWindow): `settings`, `toast()`, `run_on_ui()`.

## Alur start (`app/main.py`)
`ensure_dirs` -> `setup_logging` -> `SingleInstance.acquire` (gagal = instance lama disuruh tampil, lalu keluar) -> `AppWindow(Settings)` -> handler error global -> `mainloop`.

## Tray & lifecycle
Tray jalan di thread sendiri; callback-nya dilempar ke UI lewat `run_on_ui`. Tombol X: bila `close_to_tray` aktif dan tray hidup, window disembunyikan; selain itu keluar. Posisi window & status maximized disimpan ke settings saat ditutup. Error tak tertangani masuk `Data/logs/app.log` dan tampil di dialog.

## Build (`build.py`)
PyInstaller onedir, windowed, `--contents-directory <APP_ID>_System` (pengganti `_internal`), icon `assets/icon.ico`, `assets/` dibundle lewat `--add-data`. Setelah build, `dist/<APP_ID>` di-rename ke `dist/<APP_NAME>` lalu di-zip menjadi `dist/<APP_NAME> <VERSI>.zip` (root folder `<APP_NAME>`, tanpa versi). Library baru yang butuh hidden import: tambahkan di `build.py`.

## Alur kerja perubahan
Kerjakan -> catat di `CHANGELOG.md` -> `python dev.py bump ...` -> perbarui dokumen ini bila arsitektur berubah.

## Catatan
- Window pakai frame native (frameless Tkinter rawan bug di Windows).
- Tanpa `assets/icon.png`, tray gagal dibuat; aplikasi tetap jalan dan tombol X langsung keluar.
