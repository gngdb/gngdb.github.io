"""Summarize feed items using Claude API."""

import os
import anthropic


def get_client() -> anthropic.Anthropic:
    """Get Anthropic client from environment."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    return anthropic.Anthropic(api_key=api_key)


def summarize(title: str, description: str, client: anthropic.Anthropic = None) -> str:
    """
    Summarize an article to 140 characters or fewer.

    Args:
        title: Article title
        description: Article description/summary
        client: Anthropic client (created if not provided)

    Returns:
        A punchy 140-char summary
    """
    if client is None:
        client = get_client()

    content = f"{title}. {description}".strip()

    # Strip HTML tags from content
    import re
    content = re.sub(r"<[^>]+>", "", content)

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": (
                "Summarize the following article in 140 characters or fewer. "
                "Write one punchy, informative sentence. "
                "Do not use hashtags. Return only the summary, nothing else.\n\n"
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
