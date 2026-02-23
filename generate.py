"""Generate static feed.html from posts.json using Jinja2."""

import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Output path for the generated feed page
OUTPUT_PATH = "feed.html"
TEMPLATE_PATH = "template.html"
POSTS_PATH = "posts.json"


def load_posts(posts_file: str = POSTS_PATH) -> list[dict]:
    """Load posts from JSON file."""
    path = Path(posts_file)
    if not path.exists():
        return []
    return json.loads(path.read_text())


def generate_feed(posts: list[dict] = None, output_path: str = OUTPUT_PATH) -> None:
    """
    Generate feed.html from posts using Jinja2 template.

    Args:
        posts: List of post dicts (loaded from posts.json if not provided)
        output_path: Where to write the generated HTML
    """
    if posts is None:
        posts = load_posts()

    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=True
    )

    template = env.get_template(TEMPLATE_PATH)
    html = template.render(posts=posts)

    Path(output_path).write_text(html)
    print(f"Generated {output_path} with {len(posts)} posts")


if __name__ == "__main__":
    generate_feed()
