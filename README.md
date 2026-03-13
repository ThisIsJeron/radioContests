# alice.fm

A Streamlit app that scrapes contest listings from 23 iHeartRadio station pages across Northern California (Sacramento, Bay Area, Monterey, and Central Valley).

## Features

- **Card-based UI** with contest thumbnails, hover effects, and responsive grid layout
- **Multi-dimensional filtering** — filter by contest type, station, region, or keyword search
- **Region grouping** — stations organized into Bay Area, Sacramento, Central Valley, and Monterey
- **Summary metrics** — at-a-glance counts of contests, stations, regions, and top category
- **Classifies contests** by type (Music, Movie, Travel, Virtual Event, Other)
- **Clickable cards** linking directly to contest entry pages
- **30-minute data cache** with manual refresh button and toast confirmation

## Usage

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
