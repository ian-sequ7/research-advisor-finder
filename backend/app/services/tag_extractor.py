import os
from anthropic import Anthropic


def extract_research_tags(papers: list) -> list[str]:
    """
    Use Claude to extract 3-5 research area tags from paper titles/abstracts.

    Args:
        papers: List of Paper objects (or dicts) with 'title' and 'abstract' fields

    Returns:
        List of normalized tags like ["Natural Language Processing", "Machine Learning", "Neural Networks"]
    """
    # Handle edge case: empty papers list
    if not papers:
        return []

    try:
        client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

        # Build paper summaries (truncate abstracts to 300 chars)
        paper_summaries = []
        for paper in papers[:10]:  # Limit to 10 most recent papers to avoid token limits
            # Handle both dict and object access patterns
            title = paper.get("title") if isinstance(paper, dict) else getattr(paper, "title", None)
            abstract = paper.get("abstract") if isinstance(paper, dict) else getattr(paper, "abstract", None)

            if not title:
                continue

            summary = f"- {title}"
            if abstract:
                truncated_abstract = abstract[:300]
                if len(abstract) > 300:
                    truncated_abstract += "..."
                summary += f"\n  Abstract: {truncated_abstract}"

            paper_summaries.append(summary)

        # Handle edge case: no valid papers with titles
        if not paper_summaries:
            return []

        paper_text = "\n\n".join(paper_summaries)

        prompt = f"""Based on these research papers, extract exactly 3-5 research area tags that describe the main topics.

Papers:
{paper_text}

Requirements:
- Provide exactly 3-5 tags
- Tags should be specific research areas (e.g., "Natural Language Processing", "Computer Vision")
- Avoid overly narrow tags (e.g., prefer "Neural Networks" over "BERT fine-tuning")
- Avoid overly broad tags (e.g., prefer "Machine Learning" over "Computer Science")
- Return ONLY the tags, one per line, no numbering or extra text
"""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse and normalize tags
        raw_text = response.content[0].text.strip()
        tags = []

        for line in raw_text.split("\n"):
            # Clean up the line
            tag = line.strip()

            # Remove numbering (e.g., "1. ", "- ", etc.)
            tag = tag.lstrip("0123456789.-•*) \t")
            tag = tag.strip()

            if tag:
                # Normalize to title case
                tag = tag.title()
                tags.append(tag)

        # Deduplicate while preserving order
        seen = set()
        unique_tags = []
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower not in seen:
                seen.add(tag_lower)
                unique_tags.append(tag)

        return unique_tags

    except Exception as e:
        # Handle errors gracefully - log but don't crash
        print(f"Error extracting research tags: {e}")
        return []
