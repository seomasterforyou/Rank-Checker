import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Keyword Rank Checker", layout="wide")
st.title("📊 Google Keyword Rank Checker")

keywords_input = st.text_area("🔑 Enter Keywords (one per line):", placeholder="Best Seo Company in Delhi", height=150)
domain = st.text_input("🌐 Your Website Domain (without https://):", placeholder="abc.com")

if st.button("🚀 Check Google Rankings"):
    keywords = [kw.strip() for kw in keywords_input.strip().splitlines() if kw.strip()]
    if not keywords or not domain:
        st.warning("Please enter both keywords and domain.")
    else:
        with st.spinner("🛰️ Checking rankings via SearchAPI.io..."):
            results = []
            API_KEY = "YOUR_SEARCHAPI_KEY"
            for kw in keywords:
                rank, page = None, None
                max_results = 100
                page_size = 10

                for offset in range(0, max_results, page_size):
                    params = {
                        "engine": "google",
                        "q": kw,
                        "api_key": API_KEY,
                        "num": page_size,
                        "start": offset
                    }
                    r = requests.get("https://www.searchapi.io/api/v1/search", params=params)
                    data = r.json()

                    if "organic_results" not in data:
                        break

                    for idx, result in enumerate(data["organic_results"], start=1):
                        global_rank = offset + idx
                        link = result.get("link", "")
                        if domain in link:
                            rank = global_rank
                            page = (global_rank - 1) // page_size + 1
                            break
                    if rank is not None:
                        break
                    time.sleep(1)  # avoid rate-limits

                results.append({
                    "Keyword": kw,
                    "Rank": rank if rank else "–",
                    "Ranking Page": f"Page {page}" if page else "Not in Top 100"
                })
        df = pd.DataFrame(results)
        st.success("✅ Done checking rankings!")
        st.dataframe(df)
