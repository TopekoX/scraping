# Repository untuk Scraping Data Twitter/X

Repository ini berisi source code untuk eksperimen dan pengembangan proses scraping data dari Twitter/X berdasarkan kata kunci dan rentang waktu tertentu. Saat ini tersedia dua metode:

| Metode | Script | Keterangan |
|---|---|---|
| [`twscrape`](#metode-1-twscrape) | `scraping_twscrape.py`, `scraping_twscrape_tocsv.py` | Login memakai akun/cookies Twitter/X sendiri. Gratis, tetapi akun bisa terkena limit. |
| [`Apify`](#metode-2-apify) | `scraping_tweet_apify.py` | Memakai Actor di platform Apify dengan `APIFY_TOKEN`. Tanpa akun Twitter, tetapi memakai kuota/kredit Apify. |

Tujuan awal repository ini adalah sebagai wadah pembelajaran dan prototyping scraping data Twitter/X, dan dapat berkembang untuk menampung pendekatan lain sesuai kebutuhan.

## Struktur Project

```text
scraping/
├── .env
├── .gitignore
├── accounts.db
├── data/
├── README.md
└── src/
    ├── scraping_tweet_apify.py
    ├── scraping_twscrape.py
    └── scraping_twscrape_tocsv.py
```

---

# Persiapan Umum

Bagian ini berlaku untuk kedua metode.

## Persyaratan

- Python 3.9+
- pip
- Git

## Setup Environment

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
.venv\Scripts\activate.bat
```

Linux/macOS:

```bash
source .venv/bin/activate
```

4. Verifikasi interpreter Python dari venv

```bash
python --version
```

5. Install dependency sesuai metode yang dipakai (lihat bagian masing-masing metode)

6. Jika ingin memastikan package terinstall di environment yang aktif

```bash
pip list
```

Untuk menonaktifkan venv:

```bash
deactivate
```

## File `.env`

Buat file `.env` di root project. Variabel `START_DATE`, `END_DATE`, dan `KEYWORDS` dipakai oleh kedua metode, sedangkan variabel lainnya khusus per metode.

```env
# Umum (twscrape dan Apify)
START_DATE=2026-10-01
END_DATE=2026-10-31
KEYWORDS=banjir,gempa,kebakaran,kecelakaan

# Khusus twscrape
AUTH_TOKEN=your_auth_token
CT0=your_ct0_value
USERNAME=your_twitter_username
PASSWORD=your_twitter_password
EMAIL=your_email
EMAIL_PASSWORD=your_email_password

# Khusus Apify
APIFY_TOKEN=your_apify_api_token
```

Penjelasan variabel umum:
- `START_DATE` dan `END_DATE` menentukan rentang pencarian tweet (format `YYYY-MM-DD`).
- `KEYWORDS` berisi daftar kata kunci yang dipisahkan dengan koma.

Catatan:
- File `.env` berisi data sensitif, jangan di-commit ke repository public.
- Pastikan folder `data/` sudah ada sebelum menjalankan script, atau buat secara manual.

## Contoh Query

Kedua metode memakai pola pencarian yang sama:

```python
query = f"{kw} since:{start_date} until:{end_date}"
```

Contoh:

```text
banjir since:2026-10-01 until:2026-10-31
```

---

# Metode 1: twscrape

Mengambil tweet memakai library `twscrape` dengan akun Twitter/X yang valid.

## Dependency

```bash
pip install --upgrade pip
pip install twscrape python-dotenv
```

## Konfigurasi `.env` (twscrape)

Variabel yang dipakai selain variabel umum:

- `AUTH_TOKEN` dan `CT0` adalah cookie yang dibutuhkan untuk login akun Twitter/X.
- `USERNAME`, `PASSWORD`, `EMAIL`, dan `EMAIL_PASSWORD` digunakan pada proses `add_account()`.
- Jika `KEYWORDS` tidak diisi, script akan memakai default keyword berikut: `banjir, gempa, kebakaran, kecelakaan`.

Catatan:
- Pastikan `AUTH_TOKEN` dan `CT0` valid sebelum menjalankan scraping.
- Gunakan akun yang valid dan masih bisa login.
- `accounts.db` akan dibuat otomatis oleh `twscrape` untuk menyimpan akun yang sudah terdaftar.

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

Hasil disimpan ke folder `data/` dengan format nama file:

```text
data/hasil_tweet_twscrape_2026-10-01_2026-10-31.csv
```

## Troubleshooting (twscrape)

### Error login akun

Periksa kembali:
- `USERNAME`
- `PASSWORD`
- `EMAIL`
- `EMAIL_PASSWORD`
- `AUTH_TOKEN`
- `CT0`

Jika terjadi error login atau token invalid, perbarui `AUTH_TOKEN` dan `CT0` di file `.env`.

---

# Metode 2: Apify

Mengambil tweet lewat Actor `CJdippxWmn9uRfooo` di platform Apify, tanpa akun Twitter. Setiap run memakai kuota/kredit Apify.

## Dependency

```bash
pip install --upgrade pip
pip install apify-client pandas python-dotenv
```

## Konfigurasi `.env` (Apify)

Variabel yang dipakai selain variabel umum:

- `APIFY_TOKEN` adalah API token Apify (Apify Console > Settings > API & Integrations).

## Menjalankan Script

```bash
python src/scraping_tweet_apify.py
```

Ketentuan script:
- Kata kunci dari `KEYWORDS`, rentang tanggal dari `START_DATE` dan `END_DATE`.
- Hanya tweet bahasa Indonesia (`lang` = `in`, kode Twitter untuk Indonesia) dan tanpa retweet.
- `maxItems` = 10000 untuk seluruh run, bukan per kata kunci.
- Nilai di `.env` selalu dipakai walau terminal sudah punya variabel dengan nama sama.

Hasil disimpan ke:

```text
data/scraped_tweets_apify_2026-10-01_2026-10-31.csv
```

## Kolom CSV

| Kolom | Keterangan |
|---|---|
| `type` | Jenis data (hanya `tweet`) |
| `tweet_ref` | ID tweet |
| `text` | Isi tweet |
| `dibuat_pada` | Waktu tweet dibuat (format bawaan Twitter, UTC) |
| `lang` | Bahasa tweet (`id` untuk Indonesia) |

Agar satu tweet tetap satu baris dan satu cell, teks dibersihkan: enter dan karakter tak terlihat dihapus, koma/titik koma diganti spasi, dan tanda kutip `"` diganti `'`. Tweet yang duplikat dihapus.

## Troubleshooting (Apify)

- `Field input.lang must be equal to one of the allowed values`: gunakan `in` untuk bahasa Indonesia, bukan `id`.
- `PermissionError` saat menyimpan CSV: tutup file CSV yang sedang terbuka di Excel/editor, lalu jalankan ulang.
- Error dari `client.actor(...).call(...)`: periksa `APIFY_TOKEN` dan sisa kredit Apify.

---

# Troubleshooting Umum

### Tidak ada tweet yang muncul

Cek:
- tanggal `START_DATE` dan `END_DATE` (`until` tidak ikut dihitung, jadi untuk satu hari isi `END_DATE` dengan hari berikutnya)
- keyword yang digunakan
- metode twscrape: apakah akun Twitter masih aktif
- metode Apify: apakah kredit Apify masih tersedia

## Lisensi

Project ini digunakan untuk kebutuhan pembelajaran dan scraping data secara etis.

Gunakan sesuai dengan ketentuan platform dan kebijakan API yang berlaku.
