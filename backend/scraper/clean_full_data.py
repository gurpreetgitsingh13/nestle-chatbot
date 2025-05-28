import json
import pandas as pd

# === Step 1: Load raw scraped data ===
with open("scraper/nestle_full_scraped.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# === Step 2: Drop entries with too little text ===
df = df[df['text'].str.len() > 100].reset_index(drop=True)

# === Step 3: Save cleaned file ===
df.to_json("scraper/nestle_cleaned_full.json", orient="records", indent=2)

print(f"✅ Cleaned {len(df)} pages. Saved to nestle_cleaned_full.json")
