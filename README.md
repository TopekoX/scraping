# Repository untuk Scraping Data Twitter/X

Repository ini berisi source code untuk eksperimen dan pengembangan proses scraping data dari Twitter/X. Pada tahap saat ini, fokus utama repository ini adalah penggunaan library `twscrape` untuk mengambil data tweet berdasarkan kata kunci dan rentang waktu tertentu.

Tujuan awal repository ini adalah sebagai wadah pembelajaran dan prototyping scraping data Twitter/X. Ke depannya, repository ini dapat berkembang untuk menampung berbagai pendekatan dan tools scraping lain sesuai kebutuhan, namun untuk saat ini dokumentasi dan implementasi yang ada difokuskan pada `twscrape`.

## Struktur Project

```text
scraping/
├── .env
├── .gitignore
├── accounts.db
├── hasil_tweet_bersih.csv
├── README.md
└── src/
    ├── scraping_twscrape.py
    └── scraping_twscrape_tocsv.py
```

## Fitur

- Mencari tweet berdasarkan kata kunci
- Filter berdasarkan rentang tanggal (`since` dan `until`)
- Login akun Twitter menggunakan cookies dan akun yang valid
- Menyimpan hasil ke file CSV

## Persyaratan

Pastikan sudah terinstall:

- Python 3.9+
- pip
- Git

## Instalasi

1. Clone project

```bash
git clone <url-repository>
cd scraping
```

2. Buat virtual environment (opsional tapi disarankan)

```bash
python -m venv .venv
```

3. Aktivasi virtual environment

Windows Powershell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
.venv\Scriptsctivate.bat
```

Linux/macOS:

```bash
source .venv/bin/activate
```

4. Verifikasi interpreter Python dari venv

```bash
python --version
```

5. Install dependency

```bash
pip install --upgrade pip
pip install twscrape python-dotenv
```

6. Jika ingin memastikan package terinstall di environment yang aktif

```bash
pip list
```

7. Jalankan script dari dalam venv

```bash
python src/scraping_twscrape_tocsv.py
```

## Menonaktifkan venv

```bash
deactivate
```

## Konfigurasi `.env`

Buat file `.env` di root project dengan isi berikut:

```env
AUTH_TOKEN=your_auth_token
CT0=your_ct0_value
USERNAME=your_twitter_username
PASSWORD=your_twitter_password
EMAIL=your_email
EMAIL_PASSWORD=your_email_password
START_DATE=2026-10-01
END_DATE=2026-10-31
KEYWORDS=banjir,gempa,kebakaran,kecelakaan
```

Penjelasan:
- `AUTH_TOKEN` dan `CT0` adalah cookie yang dibutuhkan untuk login akun Twitter/X.
- `USERNAME`, `PASSWORD`, `EMAIL`, dan `EMAIL_PASSWORD` digunakan pada proses `add_account()`.
- `START_DATE` dan `END_DATE` menentukan rentang pencarian tweet.
- `KEYWORDS` berisi daftar kata kunci yang dipisahkan dengan koma.
- Jika `KEYWORDS` tidak diisi, script akan memakai default keyword berikut: `banjir, gempa, kebakaran, kecelakaan`.

Catatan:
- File `.env` berisi data sensitif, jangan di-commit ke repository public.
- Pastikan `AUTH_TOKEN` dan `CT0` valid sebelum menjalankan scraping.
- Pastikan folder `data/` sudah ada sebelum menjalankan script, atau buat secara manual.

## Menjalankan Script

### 1. Scraping tanpa CSV

```bash
python src/scraping_twscrape.py
```

Script ini akan menampilkan hasil tweet di terminal.

### 2. Scraping lalu simpan ke CSV

```bash
python src/scraping_twscrape_tocsv.py
```

Hasil akan disimpan ke file:

```text
hasil_tweet_bersih.csv
```

Pada script terbaru, hasil file CSV akan disimpan ke folder `data/` dengan format nama file seperti:

```text
data/hasil_tweet_twscrape_2026-10-01_2026-10-31.csv
```

## Contoh Query

Script menggunakan query seperti:

```python
query = f"{kw} since:{start_date} until:{end_date}"
```

Contoh:

```text
banjir since:2026-10-01 until:2026-10-31
```

## Catatan Penting

- Gunakan akun yang valid dan masih bisa login.
- Pastikan token cookies tidak kedaluwarsa.
- Jika terjadi error login atau token invalid, perbarui `AUTH_TOKEN` dan `CT0` di file `.env`.
- `accounts.db` akan dibuat otomatis oleh `twscrape` untuk menyimpan akun yang sudah terdaftar.
- Untuk keyword, Anda bisa mengisi nilai di `KEYWORDS` seperti: `banjir,gempa,kebakaran,kecelakaan`.

## Troubleshooting

### Error login akun

Periksa kembali:
- `USERNAME`
- `PASSWORD`
- `EMAIL`
- `EMAIL_PASSWORD`
- `AUTH_TOKEN`
- `CT0`

### Tidak ada tweet yang muncul

Cek:
- tanggal `START_DATE` dan `END_DATE`
- keyword yang digunakan
- apakah akun Twitter masih aktif

## Lisensi

Project ini digunakan untuk kebutuhan pembelajaran dan scraping data secara etis.

Gunakan sesuai dengan ketentuan platform dan kebijakan API yang berlaku.
