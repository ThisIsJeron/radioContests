# alice.fm

A Streamlit app that scrapes contest listings from 23 iHeartRadio station pages across Northern California (Sacramento, Bay Area, Monterey, and Central Valley).

## Features

- Scrapes and classifies contests by type (Music, Movie, Travel, Virtual Event, Other)
- Filter contests by type
- Clickable links to contest entry pages
- 30-minute data cache with manual refresh option

## Usage

```bash
pip install streamlit pandas requests beautifulsoup4 pytz
streamlit run streamlit_app.py
```
