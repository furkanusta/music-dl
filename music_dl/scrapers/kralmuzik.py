from typing import List
from music_dl.scrapers.base import Scraper
from parsel import Selector

class KralMuzik(Scraper):
    base_url = "https://www.kralmuzik.com.tr"

    # "kral-pop-radyo-top-20",
    chart = "en-kral-20-38"

    async def scrape(self) -> List[str]:
        url = f"{self.base_url}/top-listeler/{self.chart}"
        tracks = []
        response = httpx.get(url, headers=self.headers)
        response.raise_for_status()
        selector = Selector(text=response.text)
        songs = selector.css("div.item-link")
        for song in songs:
            artist = song.css("span ::text").get()
            title = song.css("strong ::text").get()
            tracks.append(f"{artist} {title}")
        return tracks
