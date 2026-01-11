from abc import ABC, abstractmethod
from typing import List


class Scraper(ABC):
    """
    Abstract base class for all scrapers.
    """

    @abstractmethod
    async def scrape(self) -> List[str]:
        """
        Scrape the source for new music.

        Returns:
            A list of track names (e.g., "Artist - Title").
        """
        raise NotImplementedError
