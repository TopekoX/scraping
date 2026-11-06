# !pip install twscrape

import asyncio
from twscrape import AccountsPool, API
from twscrape.logger import set_log_level


async def main():
    # 1. Inisialisasi pool akun (secara default akan tersimpan di file accounts.db)
    pool = AccountsPool()

    # 2. TAMBAHKAN AKUN ANDA DI SINI (Cukup 1 akun saja)
    # Hapus tanda pagar (#) di bawah ini pada baris add_account dan login_all
    # saat PERTAMA KALI dijalankan untuk mendaftarkan akun.
    # Setelah berhasil, baris ini bisa diberi pagar kembali (#) agar tidak login berulang.
    #
    # Format: add_account("username", "password", "email", "password_email")
    #

    # Masukkan nilai auth_token dan ct0 yang Anda dapatkan dari browser
    cookies = "auth_token=AUTH_TOKEN; ct0=CT0_VALUE"
    
    await pool.add_account("USERNAME_X", "PASSWORD_X", "username@mail.com", "password_email", cookies=cookies)
    await pool.login_all()

    api = API(pool)

    # 3. Daftar kata kunci yang ingin dicari
    keywords = ["banjir", "gempa", "kebakaran", "kecelakaan"]

    # 4. Tentukan rentang waktu pencarian (Format: Tahun-Bulan-Hari)
    start_date = "2026-10-29"  # Dari tanggal mulai
    end_date = "2026-10-31"  # Sampai tanggal selesai

    # Mengatur level log ke INFO agar prosesnya terlihat di terminal
    set_log_level("INFO")

    # 5. Proses pencarian berdasarkan setiap kata kunci
    for kw in keywords:
        # Menggabungkan kata kunci dengan filter rentang waktu Twitter (since & until)
        query = f"{kw} since:{start_date} until:{end_date}"

        print(
            f"\n--------------------------------------------------"
            f"\nMencari kata kunci: '{kw}' ({start_date} s.d. {end_date})"
            f"\n--------------------------------------------------"
        )

        try:
            # Mengambil maksimal 10 tweet per kata kunci (ubah nilai limit sesuai kebutuhan)
            async for tweet in api.search(query, limit=10):
                print(
                    f"[{tweet.date}] @{tweet.user.username}:\n{tweet.rawContent}\n"
                )
        except Exception as e:
            print(f"Terjadi kesalahan saat mencari kata kunci '{kw}': {e}")


if __name__ == "__main__":
    # Gunakan await main() jika di Jupyter, atau asyncio.run(main()) jika di file .py biasa
    await main()
