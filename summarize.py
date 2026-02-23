"""Summarize feed items using Claude API."""

import os
import anthropic


def get_client() -> anthropic.Anthropic:
    """Get Anthropic client from environment."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    return anthropic.Anthropic(api_key=api_key)


def summarize(title: str, description: str, source_context: str = "", client: anthropic.Anthropic = None) -> str:
    """
    Summarize a feed item to 140 characters or fewer.

    Args:
        title: Article/video title
        description: Article description/summary
        source_context: What this feed/channel is about
        client: Anthropic client (created if not provided)

    Returns:
        A punchy 140-char summary
    """
    import re

    if client is None:
        client = get_client()

    # Strip HTML tags
    description = re.sub(r"<[^>]+>", "", description)
    content = f"{title}. {description}".strip().rstrip(".")

    context_line = f"Background (do not repeat this in your summary): {source_context}\n\n" if source_context else ""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=40,
        messages=[{
            "role": "user",
            "content": (
                "Describe this specific item in around 15 tokens (a very short phrase). "
                "The reader already knows the source — focus only on what makes this particular item distinct. "
                "Do your best even if only a title is available. "
                "Do not use hashtags. Return only the description, nothing else.\n\n"
                f"{context_line}"
                f"{content}"
            )
        }]
    )

    return message.content[0].text.strip()[:140]


if __name__ == "__main__":
    # Test with a sample
    summary = summarize(
        "Test Article Title",
        "This is a test description of an article that would be summarized."
    )
    print(f"Summary ({len(summary)} chars): {summary}")
