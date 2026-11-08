# !pip install twscrape
# !pip install python-dotenv

import os
import asyncio
import csv
from pathlib import Path
from dotenv import load_dotenv
from twscrape import AccountsPool, API
from twscrape.logger import set_log_level


# load .env dari folder root project
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)

async def main():
    pool = AccountsPool()

    # Masukkan cookies akun yang valid 
    cookies = f"auth_token={os.getenv('AUTH_TOKEN')}; ct0={os.getenv('CT0')}"
    
    await pool.add_account(
        os.getenv('TWITTER_USERNAME'), 
        os.getenv('PASSWORD'), 
        os.getenv('EMAIL'), 
        os.getenv('EMAIL_PASSWORD'), 
        cookies=cookies
    )
    await pool.login_all()

    api = API(pool)

    keywords_raw = os.getenv("KEYWORDS", "")
    keywords = [kw.strip() for kw in keywords_raw.split(",")] if keywords_raw else ["banjir", "gempa", "kebakaran", "kecelakaan"]
    start_date = os.getenv('START_DATE')
    end_date = os.getenv('END_DATE')

    set_log_level("INFO")
    filename = f"data/hasil_tweet_twscrape_{start_date}_{end_date}.csv"

    with open(
        filename, mode="w", newline="", encoding="utf-8-sig"
    ) as f:
        writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_MINIMAL)

        # Menulis Judul Kolom
        writer.writerow(["ID tweet", "Teks tweet", "Waktu dibuat (created_at)"])

        for kw in keywords:
            query = f"{kw} since:{start_date} until:{end_date}"
            print(f"\nMencari kata kunci: '{kw}' ({start_date} s.d. {end_date})")

            try:
                # Mengambil data dengan limit 50 per kata kunci untuk uji coba
                async for tweet in api.search(query, limit=50):
                    # Membersihkan teks tweet dari enter agar rapi di CSV
                    teks_bersih = tweet.rawContent.replace("\n", " ").replace("\r", " ")

                    # Menulis baris data ke CSV
                    writer.writerow(
                        [
                            str(tweet.id),
                            teks_bersih,
                            str(tweet.date),
                        ]
                    )
                    print(f"[Berhasil Disimpan] ID: {tweet.id}")

                    # BERIKAN JEDA (DELAY) 3 SAMPAI 5 DETIK ANTAR KATA KUNCI
                    print("Menunggu sebentar agar aman...")
                    await asyncio.sleep(4)

            except Exception as e:
                print(f"Terjadi kesalahan saat mencari '{kw}': {e}")

    print(f"\n[SELESAI] Proses selesai. Periksa file: **{filename}**")


if __name__ == "__main__":
    # Gunakan await main() jika di Jupyter, atau asyncio.run(main()) jika di file .py biasa
    asyncio.run(main())
