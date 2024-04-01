from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

def get_contests(url):
    contests = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        contest_titles = soup.find_all(class_='component-content-tile')
        for title in contest_titles:
            text = title.get_text().strip()
            relative_url = title.find('a')['href']
            full_url = urljoin(url, relative_url)
            contests.append({"title": text, "url": full_url})
    return contests

@app.route('/get-contests', methods=['POST'])
def handle_get_contests():
    data = request.json
    urls = data.get('urls', [])
    all_contests = []
    for url in urls:
        contests = get_contests(url)
        all_contests.extend(contests)
    return jsonify(all_contests)

if __name__ == '__main__':
    app.run(debug=True)
