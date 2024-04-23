import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import pytz

# Function to classify contest type based on title
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
    # This assumes the station name is part of the domain name, like '981thebreeze.iheart.com'
    return parsed_url.hostname.split('.')[0]

def fetch_and_classify_contests(urls):
    all_contests = []
    for url in urls:
        station_name = extract_station_name(url)  # Get the station name from the URL
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            contest_titles = soup.find_all(class_='component-content-tile')
            for title in contest_titles:
                contest_text = title.get_text().strip()
                relative_url = title.find('a')['href']
                full_url = urljoin(url, relative_url)
                contest_type = classify_contest(contest_text)
                all_contests.append((contest_text, full_url, contest_type, station_name))
    
    df = pd.DataFrame(all_contests, columns=['Title', 'Link', 'Type', 'Station'])
    return df

def dataframe_to_markdown_table(df):
    # Create a new column 'Title Link' where 'Title' is a hyperlink using 'Link'
    df['Title Link'] = df.apply(lambda row: f"[**{row['Title']}**]({row['Link']})", axis=1)
    # Drop the original 'Title' and 'Link' columns
    df = df.drop(columns=['Title', 'Link'])
    
    # Rearrange columns so that 'Station' follows 'Title Link'
    df = df[['Title Link', 'Station', 'Type']]  # Adjusted column order here
    
    # Add the header row
    markdown = "| " + " | ".join(df.columns) + " |\n"
    # Add the separator row
    markdown += "| " + " | ".join(['---']*len(df.columns)) + " |\n"
    # Add data rows
    for i, row in df.iterrows():
        row_data = [str(row[col]) for col in df.columns]
        markdown += "| " + " | ".join(row_data) + " |\n"
    return markdown

# List of URLs (same as before)
urls = ["https://981thebreeze.iheart.com/promotions/", 
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
        "https://1027thewolf.iheart.com/promotions/"]

df = fetch_and_classify_contests(urls)

st.set_page_config(
    page_title="alice.fm",
    page_icon="📡",
    layout="wide"
)

st.title('Hi Baby here are Contest Listings from iHeartRadio Stations')
pst = pytz.timezone('US/Pacific')
current_time = datetime.now(pst).strftime("%Y-%m-%d %I:%M:%S %p")
st.write("Current as of: ", current_time)

filter_option = st.selectbox('Filter by type:', ['All'] + sorted(df['Type'].unique()))
if filter_option != 'All':
    df = df[df['Type'] == filter_option]

markdown_table = dataframe_to_markdown_table(df)
st.markdown(markdown_table)