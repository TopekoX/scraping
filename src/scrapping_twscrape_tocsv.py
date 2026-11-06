import asyncio
import csv
from twscrape import AccountsPool, API
from twscrape.logger import set_log_level


async def main():
    pool = AccountsPool()

    # Masukkan cookies akun yang valid
    cookies = "auth_token=AUTH_TOKEN; ct0=CT0_VALUE"
    
    await pool.add_account("USERNAME_X", "PASSWORD_X", "username@mail.com", "password_email", cookies=cookies)
    await pool.login_all()

    api = API(pool)

    keywords = ["banjir", "gempa", "kebakaran", "kecelakaan"]
    start_date = "2026-10-31"
    end_date = "2026-10-31"

    set_log_level("INFO")
    filename = "hasil_tweet_bersih.csv"

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
                # Mengambil data dengan limit 10 per kata kunci untuk uji coba
                async for tweet in api.search(query, limit=10):
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

            except Exception as e:
                print(f"Terjadi kesalahan saat mencari '{kw}': {e}")

    print(f"\n[SELESAI] Proses selesai. Periksa file: **{filename}**")


if __name__ == "__main__":
    # Gunakan await main() jika di Jupyter, atau asyncio.run(main()) jika di file .py biasa
    asyncio.run(main())
