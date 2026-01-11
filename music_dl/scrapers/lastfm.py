from typing import List
import httpx
from parsel import Selector
from music_dl.scrapers.base import Scraper


class LastfmScraper(Scraper):
    """
    A scraper for discovering music from Last.fm.
    """

    popular_url = "https://www.last.fm/music/+releases/out-now/popular"
    loved_url = "https://www.last.fm/charts#most-loved"

    async def scrape(self) -> List[str]:
        """
        Scrapes new music from Last.fm.
        """
        tracks = []
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.popular_url)
                response.raise_for_status()

                selector = Selector(text=response.text)
                songs = selector.css("div.resource-list--release-list-item")
                for song in songs:
                    title = song.css("h3.resource-list--release-list-item-name a ::text").get()
                    artist = song.css("p.resource-list--release-list-item-artist a ::text").get()
                    tracks.append(f"{artist} {title}")

                response = await client.get(self.loved_url)
                response.raise_for_status()

                selector = Selector(text=response.text)
                songs = selector.css("tr.globalchart-item")
                for song in songs:
                    title = song.css("td.globalchart-name a ::text").get()
                    artist = song.css("td.globalchart-track-artist-name a ::text").get()
                    tracks.append(f"{artist} {title}")

            except httpx.HTTPStatusError as e:
                print(f"Error fetching data from lastfm: {e}")
            except Exception as e:
                print(f"An unexpected error occurred while scraping lastfm: {e}")

        return tracks
