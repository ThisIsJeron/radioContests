import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_contests(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all elements with class 'component-content-tile'
        contest_titles = soup.find_all(class_='component-content-tile')
        
        # Extract the text from these elements and print
        for title in contest_titles:
            print(title.get_text().strip())
            relative_url = title.find('a')['href']
            full_url = urljoin(url, relative_url)
            print(f"URL: {full_url}\n")

            #url = title.find('a')['href']
            #print(f"URL: {url}\n")
            
    else:
        print("Failed to retrieve page:", response.status_code)

if _name_ == "_main_":
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
    for url in urls:
        get_contests(url)