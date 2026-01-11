from typing import List
from music_dl.scrapers.base import Scraper
from parsel import Selector

# Same as kralmuzik but with a slightly different initial selector
class Karnaval(Scraper):
    base_url = "https://karnaval.com/muzik-listeleri"

    async def scrape(self) -> List[str]:
        url = f"{self.base_url}"
        tracks = []
        response = httpx.get(url, headers=self.headers)
        response.raise_for_status()
        selector = Selector(text=response.text)
        songs = selector.css("div.item_overlay_content")
        for song in songs:
            artist = song.css("span ::text").get()
            title = song.css("strong ::text").get()
            tracks.append(f"{artist} {title}")
        return tracks
