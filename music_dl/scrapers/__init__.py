import importlib
from typing import List
from music_dl.scrapers.base import Scraper
from music_dl import config


def get_scrapers() -> List[Scraper]:
    """
    Dynamically imports and instantiates the scrapers listed in the config.
    """
    scrapers = []
    for module_name in config.SCRAPER_MODULES:
        try:
            module = importlib.import_module(f"music_dl.scrapers.{module_name}")
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if (
                    isinstance(attribute, type)
                    and issubclass(attribute, Scraper)
                    and attribute is not Scraper
                ):
                    scrapers.append(attribute())
        except ImportError as e:
            print(f"Could not import scraper '{module_name}': {e}")
    return scrapers
