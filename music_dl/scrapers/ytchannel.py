from typing import List
import httpx
from parsel import Selector
from music_dl.scrapers.base import Scraper
import re
import shelve


class YoutubeChannel(Scraper):

    # yt-dlp already has the ability to downlaod a channel, though I think the options in the
    # downloader will only force a single video to be downloaded but I can live with that for the
    # time being
    async def scrape(self) -> List[str]:
        return [
            "https://www.youtube.com/@nprmusic/videos",
            "https://www.youtube.com/@kexp/videos"
        ]
