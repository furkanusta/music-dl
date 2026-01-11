import asyncio
import shutil
import urllib


async def download_track(track_query: str, download_path: str = "downloads"):
    """
    Downloads a track from YouTube using yt-dlp.

    Args:
        track_query: The search query for the track (e.g., "Artist - Title").
        download_path: The directory to save the downloaded file.
    """
    if not shutil.which("yt-dlp"):
        raise RuntimeError(
            "yt-dlp is not installed or not in your PATH. "
            "Please install it to download music."
        )

    args = [
        "yt-dlp",
        "--extract-audio",
        "-f", "bestaudio",
        "--no-playlist",
        "--ignore-config",
        "--playlist-items", "1", # In case the link we got was already a playlist
        "--default-search", "ytsearch",
        "--output", f"{download_path}/%(title)s.%(ext)s",
        f"'{track_query}'",
    ]

    process = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(
            f"yt-dlp failed with exit code {process.returncode}\n"
            f"Stderr: {stderr.decode()}"
        )

    print(f"Successfully downloaded '{track_query}'")
