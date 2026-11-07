# !pip install apify-client pandas python-dotenv

import os
from pathlib import Path
import pandas as pd

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

# Initialize the ApifyClient with your API token
client = ApifyClient(os.getenv("APIFY_TOKEN"))

# Kata kunci dari .env, dipisah koma (contoh: banjir,gempa)
KATA_KUNCI = [k.strip() for k in os.getenv("KEYWORDS", "").split(",") if k.strip()]

# Rentang waktu dari .env (format: YYYY-MM-DD)
START = os.getenv("START_DATE")
END = os.getenv("END_DATE")

# Prepare the Actor input
run_input = {
    "searchTerms": [f"{kata} since:{START} until:{END}" for kata in KATA_KUNCI],
    "maxItems": 10000,
    "queryType": "Latest",
    "lang": "in",  # kode Twitter untuk bahasa Indonesia (bukan "id")
    "include:nativeretweets": False,  # tanpa retweet
}

# Run the Actor and wait for it to finish
run = client.actor("CJdippxWmn9uRfooo").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
items = []
for item in client.dataset(run.default_dataset_id).iterate_items():
    items.append(item)
    print(item)

df = pd.DataFrame(items)

# Hanya tweet, tanpa duplikat (satu tweet bisa cocok dengan beberapa kata kunci)
df = df[df["type"] == "tweet"].drop_duplicates(subset="id")

# Pilih & ubah nama kolom
df = df[["type", "id", "text", "createdAt", "lang"]].rename(
    columns={"id": "tweet_ref", "createdAt": "dibuat_pada"}
)

# Kode bahasa Twitter "in" -> "id" (Indonesia)
df["lang"] = df["lang"].replace({"in": "id"})

# Satu tweet = satu baris & satu cell: bersihkan karakter yang bisa memecah
# baris/cell di Excel atau editor CSV
df["text"] = (
    df["text"]
    .str.replace(r"[\r\n\t\v\f\u0085]+", " ", regex=True)  # pemisah baris
    .str.replace(r"[​‎‏﻿]", "", regex=True)  # karakter tak terlihat
    .str.replace(r"[,;]", " ", regex=True)  # pemisah kolom CSV
    .str.replace('"', "'", regex=False)  # tanda kutip
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

df.to_csv(
    f"data/scraped_tweets_apify_{START}_{END}.csv",
    index=False,
    encoding="utf-8-sig",
)