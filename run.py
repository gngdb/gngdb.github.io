#!/usr/bin/env python3
"""
Main entry point: fetch feeds → deduplicate → summarize → generate HTML.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python run.py
"""

import json
from pathlib import Path

from fetch_feeds import load_feed_urls, fetch_feeds
from summarize import get_client, summarize
from generate import generate_feed

POSTS_PATH = "posts.json"
MAX_NEW_POSTS_PER_RUN = 110  # Cost control


def load_posts() -> list[dict]:
    """Load existing posts from JSON."""
    path = Path(POSTS_PATH)
    if not path.exists():
        return []
    return json.loads(path.read_text())


def save_posts(posts: list[dict]) -> None:
    """Save posts to JSON."""
    Path(POSTS_PATH).write_text(json.dumps(posts, indent=2))


def main():
    # Load existing posts and build set of known IDs
    posts = load_posts()
    known_ids = {p["id"] for p in posts}
    print(f"Loaded {len(posts)} existing posts")

    # Fetch all feed items
    feed_urls = load_feed_urls()
    print(f"Fetching {len(feed_urls)} feeds...")
    items = fetch_feeds(feed_urls)
    print(f"Found {len(items)} total items")

    # Filter to new items only
    new_items = [item for item in items if item["id"] not in known_ids]
    print(f"Found {len(new_items)} new items")

    if not new_items:
        print("No new posts to add")
        generate_feed(posts)
        return

    # Limit new posts per run for cost control
    if len(new_items) > MAX_NEW_POSTS_PER_RUN:
        print(f"Limiting to {MAX_NEW_POSTS_PER_RUN} new posts")
        new_items = new_items[:MAX_NEW_POSTS_PER_RUN]

    # Initialize Claude client once
    client = get_client()

    # Summarize each new item
    new_posts = []
    for item in new_items:
        try:
            text = summarize(item["title"], item["description"], item.get("source_context", ""), client)
            new_posts.append({
                "id": item["id"],
                "text": text,
                "url": item["url"],
                "source": item["source"],
                "timestamp": item["timestamp"],
            })
            print(f"  [{item['source']}] {text[:50]}...")
        except Exception as e:
            print(f"  Error summarizing {item['id']}: {e}")

    # Merge and sort all posts newest-first by timestamp
    posts = new_posts + posts
    posts.sort(key=lambda p: p["timestamp"], reverse=True)
    save_posts(posts)
    print(f"Saved {len(posts)} total posts")

    # Generate HTML
    generate_feed(posts)


if __name__ == "__main__":
    main()
