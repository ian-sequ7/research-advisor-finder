import os
import re
from anthropic import Anthropic


def generate_explanation(interests: str, faculty_name: str, papers: list[str]) -> dict:
    """
    Generate match explanation with Claude, including structured breakdown.

    Returns:
        dict with 'explanation' (str) and 'breakdown' (dict or None)
    """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    paper_list = "\n".join(f"- {p}" for p in papers[:5])

    prompt = f"""A prospective PhD student is interested in: {interests}

They matched with Professor {faculty_name}, who has written papers including:
{paper_list}

In 2-3 sentences, explain why this professor might be a good research advisor match. Be specific about the connection between the student's interests and the professor's research.

Also provide a brief breakdown:
- Topic Alignment: [High/Medium/Low] - [1 sentence why]
- Paper Relevance: [High/Medium/Low] - [1 sentence about specific papers]
- Research Fit: [High/Medium/Low] - [1 sentence about methodology/approach fit]"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )

    raw_text = response.content[0].text

    # Parse the response
    explanation, breakdown = _parse_explanation_response(raw_text)

    return {
        "explanation": explanation,
        "breakdown": breakdown
    }


def _parse_explanation_response(raw_text: str) -> tuple[str, dict | None]:
    """
    Parse LLM response to extract explanation and structured breakdown.

    Returns:
        tuple of (explanation_text, breakdown_dict or None)
    """
    try:
        lines = raw_text.strip().split("\n")
        explanation_lines = []
        breakdown = {}

        # Patterns to match breakdown lines
        patterns = {
            "topic_alignment": r"topic\s*alignment[:\s]*\[?(high|medium|low)\]?[:\s\-]*(.+)",
            "paper_relevance": r"paper\s*relevance[:\s]*\[?(high|medium|low)\]?[:\s\-]*(.+)",
            "research_fit": r"research\s*fit[:\s]*\[?(high|medium|low)\]?[:\s\-]*(.+)",
        }

        for line in lines:
            line_lower = line.lower().strip()
            matched = False

            for key, pattern in patterns.items():
                match = re.search(pattern, line_lower, re.IGNORECASE)
                if match:
                    level = match.group(1).capitalize()
                    reason = match.group(2).strip()
                    # Clean up the reason - remove trailing punctuation artifacts
                    reason = re.sub(r'^[\-\s]+', '', reason)
                    # Get original case from the line for the reason
                    breakdown[key] = {
                        "level": level,
                        "reason": reason.capitalize() if reason else ""
                    }
                    matched = True
                    break

            # If not a breakdown line, add to explanation
            if not matched and line.strip():
                # Skip lines that look like breakdown headers
                if not any(key.replace("_", " ") in line_lower for key in patterns.keys()):
                    explanation_lines.append(line.strip())

        explanation = " ".join(explanation_lines).strip()

        # Only return breakdown if we found at least one item
        if not breakdown:
            breakdown = None

        return explanation, breakdown

    except Exception as e:
        print(f"Error parsing explanation response: {e}")
        # Return the full text as explanation if parsing fails
        return raw_text.strip(), None


# Legacy function for backwards compatibility
def generate_explanation_simple(interests: str, faculty_name: str, papers: list[str]) -> str:
    """Generate match explanation (simple version, returns string only)."""
    result = generate_explanation(interests, faculty_name, papers)
    return result["explanation"]
