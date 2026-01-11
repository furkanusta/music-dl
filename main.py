#!/usr/bin/env python
import sys
import os
import asyncio
import shelve

from music_dl.downloader import download_track
from music_dl.scrapers import get_scrapers


async def discover_music(scrapers):
    """
    Discovers music from a list of scrapers.
    """
    all_tracks = []
    for scraper in scrapers:
        print(f"Scraping {scraper.__class__.__name__}...")
        try:
            tracks = await scraper.scrape()
            all_tracks.extend(tracks)
            print(f"Found {len(tracks)} tracks from {scraper.__class__.__name__}.")
        except Exception as e:
            print(f"Error scraping {scraper.__class__.__name__}: {e}")
    return all_tracks


def remove_duplicates(tracks):
    """
    Removes duplicate tracks from a list.
    """
    tracks = map(lambda x: x.lower(), tracks)
    tracks = list(set(tracks))
    with shelve.open(".db/tracks") as db:
        tracks = [track for track in tracks if track not in db]
    return tracks


async def download_all(tracks):
    """
    Downloads all tracks in a list.
    """
    print("\nStarting downloads...")
    for track in tracks:
        print(f"Downloading: {track}")
        try:
            await download_track(str(track))
        except Exception as e:
            print(f"Error downloading {track}: {e}")
    print("\nAll downloads completed.")


async def main():
    """
    The main function to run the music discovery and download process.
    """
    print("Starting music discovery...")
    scrapers = get_scrapers()

    tracks = await discover_music(scrapers)

    tracks = remove_duplicates(tracks)

    print(f"Found Tracks: {tracks}")
    await download_all([tracks[0]])

    with shelve.open(".db/tracks") as db:
        for track in tracks:
            db[track] = 1


if __name__ == "__main__":
    asyncio.run(main())
