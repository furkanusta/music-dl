from typing import List
from music_dl.scrapers.base import Scraper
from parsel import Selector
import httpx

class TRTMuzik(Scraper):
    base_url = "https://www.trtdinle.com"

    # caz-en-cok-dinlenenler-5632819
    # klasik-en-cok-dinlenenler-5632809
    # turk-halk-muzigi-en-cok-dinlenenler-5632505
    # turk-sanat-muzigi-en-cok-dinlenenler-5632389
    # turkce-rock-en-cok-dinlenenler-5632634
    chart = "turkce-pop-en-cok-dinlenenler-5632504"

    def __init__(self):
        # Not sure why but brotli breaks it
        self.headers["Accept-Encoding"] = "gzip, deflate"

    async def scrape(self) -> List[str]:
        url = f"{self.base_url}/playlist/{self.chart}"
        tracks = []
        response = httpx.get(url, headers=self.headers)
        response.raise_for_status()
        selector = Selector(text=response.text)
        songs = selector.css("div.song-list-item")
        for song in songs:
            artist = song.css("div.title ::text").get().strip()
            title = song.css("div.desc a ::text").get().strip()
            tracks.append(f"{artist} {title}")
        return tracks
