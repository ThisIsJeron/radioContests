import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import pytz

st.set_page_config(
    page_title="alice.fm",
    page_icon="📡",
    layout="wide"
)

STATION_URLS = [
    "https://981thebreeze.iheart.com/promotions/",
    "https://1013.iheart.com/promotions/",
    "https://kmel.iheart.com/promotions/",
    "https://wild949.iheart.com/promotions/",
    "https://mega100fm.iheart.com/promotions/",
    "https://kfbk.iheart.com/promotions/",
    "https://925thebreeze.iheart.com/promotions/",
    "https://v1011sacramento.iheart.com/promotions/",
    "https://kste.iheart.com/promotions/",
    "https://thebullsacramento.iheart.com/promotions/",
    "https://kiss1079.iheart.com/promotions/",
    "https://kdon.iheart.com/promotions/",
    "https://1051kocean.iheart.com/promotions/",
    "https://ktom.iheart.com/promotions/",
    "https://foxsportsam1280.iheart.com/promotions/",
    "https://sunny102fm.iheart.com/promotions/",
    "https://rock967.iheart.com/promotions/",
    "https://929thebigdog.iheart.com/promotions/",
    "https://powertalk1360.iheart.com/promotions/",
    "https://b95forlife.iheart.com/promotions/",
    "https://softrock989.iheart.com/promotions/",
    "https://thebeat1037.iheart.com/promotions/",
    "https://1027thewolf.iheart.com/promotions/",
]


def classify_contest(title):
    if "Advance Screening Passes" in title:
        return "Movie"
    elif "Tickets" in title:
        return "Music"
    elif "Trip" in title or "Tour" in title:
        return "Travel"
    elif "Virtual Screening" in title or "Watch" in title:
        return "Virtual Event"
    else:
        return "Other"


def extract_station_name(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname.split('.')[0]


@st.cache_data(ttl=1800)
def fetch_and_classify_contests(urls):
    all_contests = []
    for url in urls:
        station_name = extract_station_name(url)
        try:
            response = requests.get(url, timeout=10)
        except requests.RequestException:
            continue
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            contest_titles = soup.find_all(class_='component-content-tile')
            for title in contest_titles:
                contest_text = title.get_text().strip()
                link_tag = title.find('a')
                if not link_tag or not link_tag.get('href'):
                    continue
                full_url = urljoin(url, link_tag['href'])
                contest_type = classify_contest(contest_text)
                all_contests.append((contest_text, full_url, contest_type, station_name))

    df = pd.DataFrame(all_contests, columns=['Title', 'Link', 'Type', 'Station'])
    return df


st.title('Hi Mimi here are Contest Listings from iHeartRadio Stations')
pst = pytz.timezone('US/Pacific')
current_time = datetime.now(pst).strftime("%Y-%m-%d %I:%M:%S %p")
st.write("Current as of: ", current_time)

if st.button("Refresh Data"):
    st.cache_data.clear()

with st.spinner("Fetching contest listings..."):
    df = fetch_and_classify_contests(tuple(STATION_URLS))

if df.empty:
    st.info("No contests found. Try refreshing later.")
else:
    filter_option = st.selectbox('Filter by type:', ['All'] + sorted(df['Type'].unique()))
    if filter_option != 'All':
        df = df[df['Type'] == filter_option]

    st.caption(f"Showing {len(df)} contest(s)")

    st.dataframe(
        df,
        column_config={
            "Link": st.column_config.LinkColumn("Link"),
        },
        use_container_width=True,
        hide_index=True,
    )
