from typing import List
import httpx
from parsel import Selector
from music_dl.scrapers.base import Scraper
import re
import shelve


class RedditScraper(Scraper):
    """
    A scraper for discovering music from Reddit.
    """
    base_url = "https://www.reddit.com/r"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"

    NUM_POSTS    = 25
    NUM_COMMENTS = 25

    def __init__(self):
        # In a real implementation, you might want to pass subreddits, etc.
        self.subreddits = [
            ("ifyoulikeblank", "search.json?q=flair%3Amusic+OR+title%3Amusic&sort=top&restrict_sr=on&t=month"),
            # "listentothis",
            # "indieheads"
        ]

    async def get_posts(self) -> List[str]:
        print(f"Scraping Reddit for subreddits: {self.subreddits}")
        posts = []
        async with httpx.AsyncClient() as client:
            for subreddit in self.subreddits:
                sub      = subreddit[0] if type(subreddit) is tuple else subreddit
                json_url = subreddit[1] if type(subreddit) is tuple else "top.json?t=month"
                url = f"{self.base_url}/{sub}/{json_url}"
                try:
                    # This is a placeholder URL. You'll need to use the Reddit API
                    # or a library like asyncpraw for a real implementation.
                    response = await client.get(url, headers={"User-agent": self.user_agent})
                    response.raise_for_status()

                    data = response.json()['data']['children']
                    posts.extend([(sub, post['data']['id']) for post in data])

                except httpx.HTTPStatusError as e:
                    print(f"Error fetching data from Reddit for r/{subreddit}: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred while scraping r/{subreddit}: {e}")
        return posts

    async def get_comments(self, posts: List[str]) -> List[str]:
        comments = []
        async with httpx.AsyncClient() as client:
            for post in posts:
                url = f"{self.base_url}/{post[0]}/comments/{post[1]}/.json"
                print(f"Scraping for comments: {url}")
                try:
                    # This is a placeholder URL. You'll need to use the Reddit API
                    # or a library like asyncpraw for a real implementation.
                    response = await client.get(url, headers={"User-agent": self.user_agent})
                    response.raise_for_status()

                    # Limit to 25 comments for the time being
                    data = response.json()[1]['data']['children'][:self.NUM_COMMENTS]
                    comments.extend(d['data']['body'] for d in data if d['data']['depth'] == 0)

                except httpx.HTTPStatusError as e:
                    print(f"Error fetching data from {post}: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred while scraping {post}: {e}")
        return comments

    async def get_tracks(self, comments: List[str]) -> List[str]:
        tracks = []
        yt_re = "(https?://)?(www\\.|music\\.)?(youtube\\.com|youtu\\.be)/[^)\\]& ]+"
        for comment in comments:
            yt_links = [x.group() for x in re.finditer(yt_re, comment)]
            comment = comment.replace("&amp", "&")
            if yt_links:
                tracks.extend(yt_links)
            elif "\n\n\n" in comment:
                # If there are multiple lines usually they are list of songs/artists
                tracks.extend(c.strip() for c in comment.split("\n\n\n"))
            elif "\n\n" not in comment:
                comment = comment.replace("\n", " ")
                if comment.count(',') > 2:
                    # Comments are quite often mixed with commentary (heh) and I don't have a
                    # reliable way of separating the artist from the art. So Instead I'll hope that
                    # first 25 characters is satisfactory
                    parts = [c.strip() for c in comment.split(',') if len(c) <= 25]
                    tracks.extend(parts)
                elif "." in comment and comment.find(".") < 30:
                    tracks.append(comment.split('.')[0])
                elif len(comment) < 30:
                    tracks.append(comment)
        tracks = list(map(lambda x: x.strip(), tracks))
        return tracks

    async def scrape(self) -> List[str]:
        """
        Scrapes music from the configured subreddits.
        """
        posts    = await self.get_posts()
        posts = posts[:self.NUM_POSTS]
        with shelve.open(".db/posts") as db:
            posts = [post for post in posts if "/".join(post) not in db]
        comments = await self.get_comments(posts)
        tracks   = await self.get_tracks(comments)

        with shelve.open(".db/posts") as db:
            for post in posts:
                db["/".join(post)] = 1
        return tracks
