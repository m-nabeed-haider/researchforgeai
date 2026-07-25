from __future__ import annotations

from backend.app.ai.search.models import SearchResponse


def format_search_context(
    response: SearchResponse,
) -> str:
    """
    Formats search results into a structured context block
    for prompt injection.
    """

    lines: list[str] = []

    lines.append(
        "The following information was retrieved from trusted sources."
    )
    lines.append(
        "Use these sources when answering the user's question."
    )
    lines.append("")

    for result in response.results:

        lines.append(f"Source: {result.source}")
        lines.append(f"Title: {result.title}")
        lines.append(f"URL: {result.url}")
        lines.append("")
        lines.append(result.content)
        lines.append("")
        lines.append("-" * 80)
        lines.append("")

    return "\n".join(lines)