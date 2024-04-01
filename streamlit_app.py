import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pytz
from datetime import datetime

def get_contests(url):
    contests = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        contest_titles = soup.find_all(class_='component-content-tile')
        for title in contest_titles:
            contest_text = title.get_text().strip()
            relative_url = title.find('a')['href']
            full_url = urljoin(url, relative_url)
            contests.append((contest_text, full_url))
    return contests

def display_contests(urls):
    for url in urls:
        contests = get_contests(url)
        if contests:
            for title, link in contests:
                st.write(f"**[{title}]({link})**")
                #st.write(f"[Link]({link})")
        else:
            st.write("No contests found for:", url)

if __name__ == "__main__":
    st.title('Hi Baby here are Contest Listings from iHeartRadio Stations')
    pst = pytz.timezone('US/Pacific')
    current_time = datetime.now(pst).strftime("%Y-%m-%d %H:%M:%S")
    st.write("Current time and date in PST: ", current_time)
    
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

    display_contests(urls)
