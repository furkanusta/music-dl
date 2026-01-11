from abc import ABC, abstractmethod
from typing import List


class Scraper(ABC):
    """
    Abstract base class for all scrapers.
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }

    @abstractmethod
    async def scrape(self) -> List[str]:
        """
        Scrape the source for new music.

        Returns:
            A list of track names (e.g., "Artist - Title").
        """
        raise NotImplementedError
