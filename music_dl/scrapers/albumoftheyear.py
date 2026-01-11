from typing import List
import requests
from parsel import Selector
from music_dl.scrapers.base import Scraper
from datetime import date
import calendar
from parsel import Selector

class AlbumOfTheYear(Scraper):
    """
    A scraper for discovering music from albumoftheyear.org
    """

    base_url = "https://www.albumoftheyear.org"

    def scrape(self) -> List[str]:
        # 2026/releases/january-01/
        year = date.today().year
        month = date.today().month
        month_name = calendar.month_name[month].lower()
        url = f"{self.base_url}/{year}/releases/{month_name}-{month:02}"
        tracks = []
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        selector = Selector(text=response.text)
        albums = selector.css("div.albumBlock")
        for album in albums:
            artist = album.css("div.artistTitle")
            title = album.css("div.albumTitle")
            tracks.append(f"{artist} {title}")
        return tracks
