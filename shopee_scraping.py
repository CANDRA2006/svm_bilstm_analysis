"""
scraping.py
Mengambil data review aplikasi Shopee dari Google PlayStore
menggunakan library google-play-scraper.

"""

import time
import pandas as pd
from tqdm import tqdm
from google_play_scraper import Sort, reviews

# ID aplikasi Shopee di Play Store
APP_ID = "com.shopee.id"
TARGET_TOTAL = 15000            
BATCH_SIZE = 200
# Kode bahasa 
LANG = "id"
COUNTRY = "id"
OUTPUT_PATH = "dataset/shopee_reviews_indonesia_raw.csv"


def scrape_reviews():
    all_reviews = []
    continuation_token = None

    # Mengubah deskripsi progress bar
    with tqdm(total=TARGET_TOTAL, desc="Scraping Shopee reviews") as pbar:
        while len(all_reviews) < TARGET_TOTAL:
            result, continuation_token = reviews(
                APP_ID,
                lang=LANG,
                country=COUNTRY,
                sort=Sort.NEWEST,
                count=BATCH_SIZE,
                continuation_token=continuation_token,
            )

            if not result:
                break

            all_reviews.extend(result)
            pbar.update(len(result))

            # Menghindari rate limit
            time.sleep(1)

            if continuation_token is None:
                break

    df = pd.DataFrame(all_reviews)
    df = df[[
        "reviewId", "userName", "content", "score",
        "thumbsUpCount", "reviewCreatedVersion", "at"
    ]]
    df.rename(columns={"content": "text", "score": "rating"}, inplace=True)
    
    # Membersihkan data duplikat dan kosong
    df.drop_duplicates(subset="text", inplace=True)
    df.dropna(subset=["text"], inplace=True)

    # Pastikan folder 'dataset' sudah dibuat sebelumnya atau berada di direktori yang sama
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSelesai. Total review tersimpan: {len(df)} -> {OUTPUT_PATH}")


if __name__ == "__main__":
    scrape_reviews()
