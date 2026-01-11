from typing import List
from parsel import Selector
from music_dl.scrapers.base import Scraper
from datetime import date
import calendar
from parsel import Selector
import curl_cffi

class AlbumOfTheYear(Scraper):
    """
    A scraper for discovering music from albumoftheyear.org
    """

    base_url = "https://www.albumoftheyear.org"

    async def scrape(self) -> List[str]:
        # 2026/releases/january-01/
        year = date.today().year
        month = date.today().month
        month_name = calendar.month_name[month].lower()
        url = f"{self.base_url}/{year}/releases/{month_name}-{month:02}"
        tracks = []
        response = curl_cffi.get(url, impersonate="chrome")
        response.raise_for_status()
        selector = Selector(text=response.text)
        albums = selector.css("div.albumBlock")
        for album in albums:
            artist = album.css("div.artistTitle ::text").get()
            title = album.css("div.albumTitle ::text").get()
            tracks.append(f"{artist} {title}")
        return tracks
