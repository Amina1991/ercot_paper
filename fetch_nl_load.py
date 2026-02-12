#!/usr/bin/env python3
"""
Fetch NL actual total load and generation per type from ENTSO-E for 2020–2024 and save to CSV.
"""

import pandas as pd
from entsoe import EntsoePandasClient

def fetch_nl_load(start, end, client):
    return client.query_load(
        country_code="NL",
        start=start,
        end=end
    )

def fetch_nl_generation(start, end, client):
    return client.query_generation(
        country_code="NL",
        start=start,
        end=end,
        psr_type=None  # None = all generation types
    )

def main():
    api_key = 'fa334080-5be9-4612-993b-3b6d1e90b1f8'
    client = EntsoePandasClient(api_key=api_key)
    tz = "Europe/Amsterdam"

    # --- Load ---
    all_load = []
    for year in range(2020, 2025):
        start = pd.Timestamp(f"{year}-01-01 00:00", tz=tz)
        end = pd.Timestamp(f"{year+1}-01-01 00:00", tz=tz) if year < 2024 else pd.Timestamp("2025-01-01 00:00", tz=tz)
        print(f"Querying load: {start} → {end} …")
        series = fetch_nl_load(start, end, client)
        all_load.append(series)

    load_df = pd.concat(all_load).sort_index()
    load_df = load_df[~load_df.index.duplicated(keep='first')]
    load_df.to_csv("NL_load_actual_2020_2024.csv", header=["Load_MW"])
    print(f"✅ Saved {len(load_df)} hourly records to NL_load_actual_2020_2024.csv")

    # --- Generation ---
    all_gen = []
    for year in range(2020, 2025):
        start = pd.Timestamp(f"{year}-01-01 00:00", tz=tz)
        end = pd.Timestamp(f"{year+1}-01-01 00:00", tz=tz) if year < 2024 else pd.Timestamp("2025-01-01 00:00", tz=tz)
        print(f"Querying generation: {start} → {end} …")
        df_gen = fetch_nl_generation(start, end, client)
        all_gen.append(df_gen)

    generation_df = pd.concat(all_gen).sort_index()
    generation_df = generation_df[~generation_df.index.duplicated(keep='first')]
    generation_df.to_csv("NL_generation_by_type_2020_2024.csv")
    print(f"✅ Saved generation data by type to NL_generation_by_type_2020_2024.csv")

if __name__ == "__main__":
    main()
