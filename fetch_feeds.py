"""Fetch and parse RSS/Atom feeds."""

import feedparser
from pathlib import Path
from datetime import datetime
from email.utils import parsedate_to_datetime


def load_feed_urls(feeds_file: str = "feeds.txt") -> list[str]:
    """Load feed URLs from feeds.txt (one per line)."""
    path = Path(feeds_file)
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def parse_timestamp(entry) -> str:
    """Extract and normalize timestamp from feed entry."""
    # Try published first, then updated
    for attr in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, attr, None)
        if parsed:
            try:
                dt = datetime(*parsed[:6])
                return dt.isoformat() + "Z"
            except (TypeError, ValueError):
                pass

    # Try parsing from string
    for attr in ("published", "updated"):
        raw = getattr(entry, attr, None)
        if raw:
            try:
                dt = parsedate_to_datetime(raw)
                return dt.isoformat().replace("+00:00", "Z")
            except (TypeError, ValueError):
                pass

    # Fallback to now
    return datetime.utcnow().isoformat() + "Z"


def fetch_feeds(feed_urls: list[str]) -> list[dict]:
    """
    Fetch all feeds and return a list of items.

    Each item is a dict with:
    - id: unique identifier (guid or link)
    - source: feed title
    - title: entry title
    - description: entry summary/description
    - url: link to the article
    - timestamp: ISO timestamp
    """
    items = []

    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            source_name = feed.feed.get("title", url)

            for entry in feed.entries:
                item_id = entry.get("id") or entry.get("link") or entry.get("title")
                if not item_id:
                    continue

                items.append({
                    "id": item_id,
                    "source": source_name,
                    "title": entry.get("title", ""),
                    "description": entry.get("summary", entry.get("description", "")),
                    "url": entry.get("link", ""),
                    "timestamp": parse_timestamp(entry),
                })
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    return items


if __name__ == "__main__":
    urls = load_feed_urls()
    items = fetch_feeds(urls)
    for item in items[:3]:
        print(f"{item['source']}: {item['title'][:50]}...")
