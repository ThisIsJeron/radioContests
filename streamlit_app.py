import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import pytz

st.set_page_config(
    page_title="alice.fm",
    page_icon="📡",
    layout="wide",
)

STATIONS = {
    "https://981thebreeze.iheart.com/promotions/": {
        "name": "98.1 The Breeze",
        "region": "Bay Area",
    },
    "https://1013.iheart.com/promotions/": {
        "name": "101.3 KIOI",
        "region": "Bay Area",
    },
    "https://kmel.iheart.com/promotions/": {
        "name": "106.1 KMEL",
        "region": "Bay Area",
    },
    "https://wild949.iheart.com/promotions/": {
        "name": "Wild 94.9",
        "region": "Bay Area",
    },
    "https://mega100fm.iheart.com/promotions/": {
        "name": "Mega 100 FM",
        "region": "Bay Area",
    },
    "https://kfbk.iheart.com/promotions/": {
        "name": "KFBK NewsTalk 93.1",
        "region": "Sacramento",
    },
    "https://925thebreeze.iheart.com/promotions/": {
        "name": "92.5 The Breeze",
        "region": "Sacramento",
    },
    "https://v1011sacramento.iheart.com/promotions/": {
        "name": "V101.1",
        "region": "Sacramento",
    },
    "https://kste.iheart.com/promotions/": {
        "name": "KSTE 650 AM",
        "region": "Sacramento",
    },
    "https://thebullsacramento.iheart.com/promotions/": {
        "name": "The Bull Sacramento",
        "region": "Sacramento",
    },
    "https://1027thewolf.iheart.com/promotions/": {
        "name": "102.7 The Wolf",
        "region": "Sacramento",
    },
    "https://kiss1079.iheart.com/promotions/": {
        "name": "KISS 107.9",
        "region": "Central Valley",
    },
    "https://sunny102fm.iheart.com/promotions/": {
        "name": "Sunny 102 FM",
        "region": "Central Valley",
    },
    "https://rock967.iheart.com/promotions/": {
        "name": "Rock 96.7",
        "region": "Central Valley",
    },
    "https://929thebigdog.iheart.com/promotions/": {
        "name": "92.9 The Big Dog",
        "region": "Central Valley",
    },
    "https://powertalk1360.iheart.com/promotions/": {
        "name": "Power Talk 1360",
        "region": "Central Valley",
    },
    "https://b95forlife.iheart.com/promotions/": {
        "name": "B95",
        "region": "Central Valley",
    },
    "https://softrock989.iheart.com/promotions/": {
        "name": "Soft Rock 98.9",
        "region": "Central Valley",
    },
    "https://thebeat1037.iheart.com/promotions/": {
        "name": "The Beat 103.7",
        "region": "Central Valley",
    },
    "https://kdon.iheart.com/promotions/": {
        "name": "KDON 102.5",
        "region": "Monterey",
    },
    "https://1051kocean.iheart.com/promotions/": {
        "name": "105.1 K-Ocean",
        "region": "Monterey",
    },
    "https://ktom.iheart.com/promotions/": {
        "name": "KTOM 100.7",
        "region": "Monterey",
    },
    "https://foxsportsam1280.iheart.com/promotions/": {
        "name": "Fox Sports AM 1280",
        "region": "Monterey",
    },
}

TYPE_ICONS = {
    "Movie": "🎬",
    "Music": "🎵",
    "Travel": "✈️",
    "Virtual Event": "💻",
    "Other": "🎁",
}

REGION_COLORS = {
    "Bay Area": "#4A90D9",
    "Sacramento": "#D4A843",
    "Central Valley": "#6BBF6A",
    "Monterey": "#D97B4A",
}

CARD_CSS = """
<style>
.hero-banner {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    color: white;
}
.hero-banner h1 {
    margin: 0 0 0.3rem 0;
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.5px;
}
.hero-banner .subtitle {
    margin: 0;
    font-size: 1.05rem;
    opacity: 0.8;
    font-weight: 400;
}
.hero-banner .timestamp {
    margin-top: 0.7rem;
    font-size: 0.82rem;
    opacity: 0.55;
}
.contest-card {
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 14px;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    background: var(--background-color, #ffffff);
    height: 100%;
    display: flex;
    flex-direction: column;
}
.contest-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}
.contest-card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
}
.card-body {
    padding: 1rem 1.1rem;
    flex: 1;
    display: flex;
    flex-direction: column;
}
.card-body .card-title {
    font-size: 0.95rem;
    font-weight: 600;
    line-height: 1.4;
    margin-bottom: 0.7rem;
    flex: 1;
}
.card-body .card-title a {
    text-decoration: none;
    color: inherit;
}
.card-body .card-title a:hover {
    text-decoration: underline;
}
.badge-row {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
    margin-top: auto;
}
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.badge-station {
    background: rgba(74, 144, 217, 0.15);
    color: #4A90D9;
}
.badge-type {
    background: rgba(128, 128, 128, 0.12);
    color: inherit;
    opacity: 0.8;
}
.badge-region {
    color: white;
    font-size: 0.68rem;
}
.no-image-placeholder {
    width: 100%;
    height: 180px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
}
</style>
"""


def classify_contest(title):
    title_lower = title.lower()
    if "advance screening passes" in title_lower or "screening" in title_lower:
        return "Movie"
    elif "ticket" in title_lower or "concert" in title_lower:
        return "Music"
    elif "trip" in title_lower or "tour" in title_lower or "getaway" in title_lower:
        return "Travel"
    elif "virtual" in title_lower or "watch" in title_lower or "stream" in title_lower:
        return "Virtual Event"
    else:
        return "Other"


@st.cache_data(ttl=1800)
def fetch_and_classify_contests(urls):
    all_contests = []
    for url in urls:
        meta = STATIONS.get(url, {})
        station_name = meta.get("name", url.split("//")[1].split(".")[0])
        region = meta.get("region", "Unknown")
        try:
            response = requests.get(url, timeout=10)
        except requests.RequestException:
            continue
        if response.status_code != 200:
            continue
        soup = BeautifulSoup(response.content, "lxml")
        tiles = soup.find_all(class_="component-content-tile")
        for tile in tiles:
            link_tag = tile.find("a", class_="card-title") or tile.find("a")
            if not link_tag or not link_tag.get("href"):
                continue
            contest_text = link_tag.get_text(strip=True)
            full_url = urljoin(url, link_tag["href"])

            img_tag = tile.find("img")
            image_url = ""
            if img_tag:
                image_url = img_tag.get("data-src") or img_tag.get("src", "")

            contest_type = classify_contest(contest_text)
            all_contests.append({
                "Title": contest_text,
                "Link": full_url,
                "Type": contest_type,
                "Station": station_name,
                "Region": region,
                "Image": image_url,
            })

    return pd.DataFrame(all_contests)


def render_card(row):
    title = row["Title"]
    link = row["Link"]
    station = row["Station"]
    contest_type = row["Type"]
    region = row["Region"]
    image_url = row.get("Image", "")
    type_icon = TYPE_ICONS.get(contest_type, "🎁")
    region_color = REGION_COLORS.get(region, "#888888")

    if image_url:
        img_html = f'<img src="{image_url}" alt="{title}" loading="lazy">'
    else:
        img_html = f'<div class="no-image-placeholder">{type_icon}</div>'

    return f"""
    <div class="contest-card">
        {img_html}
        <div class="card-body">
            <div class="card-title">
                <a href="{link}" target="_blank" rel="noopener">{title}</a>
            </div>
            <div class="badge-row">
                <span class="badge badge-station">{station}</span>
                <span class="badge badge-type">{type_icon} {contest_type}</span>
                <span class="badge badge-region" style="background:{region_color};">{region}</span>
            </div>
        </div>
    </div>
    """


# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(CARD_CSS, unsafe_allow_html=True)

# ── Hero banner ──────────────────────────────────────────────────────────────
pst = pytz.timezone("US/Pacific")
current_time = datetime.now(pst).strftime("%B %d, %Y at %I:%M %p")
st.markdown(
    f"""
    <div class="hero-banner">
        <h1>📡 alice.fm</h1>
        <p class="subtitle">Contest listings from iHeartRadio stations across Northern California</p>
        <p class="timestamp">Last refreshed {current_time} PST</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📡 alice.fm")
    st.caption("Your NorCal radio contest dashboard")
    st.divider()

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.toast("Cache cleared — fetching fresh data!", icon="✅")

    st.divider()
    st.markdown("**Filters**")
    keyword = st.text_input("🔍 Search contests", placeholder="e.g. tickets, trip, win")

    all_regions = sorted(STATIONS[u]["region"] for u in STATIONS)
    unique_regions = sorted(set(all_regions))
    selected_regions = st.multiselect("🗺️ Region", unique_regions)

    station_names = sorted(set(STATIONS[u]["name"] for u in STATIONS))
    if selected_regions:
        station_names = sorted(
            s["name"]
            for s in STATIONS.values()
            if s["region"] in selected_regions
        )
    selected_stations = st.multiselect("📻 Station", station_names)

    all_types = list(TYPE_ICONS.keys())
    selected_types = st.multiselect("🏷️ Contest type", all_types)

# ── Fetch data ───────────────────────────────────────────────────────────────
with st.spinner("Fetching contest listings from 23 stations..."):
    df = fetch_and_classify_contests(tuple(STATIONS.keys()))

if df.empty:
    st.info("No contests found right now. Try refreshing later.")
    st.stop()

# ── Apply filters ────────────────────────────────────────────────────────────
filtered = df.copy()
if keyword:
    filtered = filtered[filtered["Title"].str.contains(keyword, case=False, na=False)]
if selected_regions:
    filtered = filtered[filtered["Region"].isin(selected_regions)]
if selected_stations:
    filtered = filtered[filtered["Station"].isin(selected_stations)]
if selected_types:
    filtered = filtered[filtered["Type"].isin(selected_types)]

# ── Metrics row ──────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("Contests", len(filtered))
m2.metric("Stations", filtered["Station"].nunique())
m3.metric("Regions", filtered["Region"].nunique())
top_type = filtered["Type"].mode().iloc[0] if not filtered.empty else "—"
m4.metric("Top Category", top_type)

st.divider()

# ── Card grid ────────────────────────────────────────────────────────────────
if filtered.empty:
    st.warning("No contests match your filters. Try broadening your search.")
else:
    st.caption(f"Showing {len(filtered)} contest(s)")
    cols_per_row = 3
    rows = [filtered.iloc[i : i + cols_per_row] for i in range(0, len(filtered), cols_per_row)]
    for chunk in rows:
        cols = st.columns(cols_per_row)
        for idx, (_, row) in enumerate(chunk.iterrows()):
            with cols[idx]:
                st.markdown(render_card(row), unsafe_allow_html=True)
