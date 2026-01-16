import os
import re
from anthropic import Anthropic


def generate_explanation(interests: str, faculty_name: str, papers: list[str]) -> dict:
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

    explanation, breakdown = _parse_explanation_response(raw_text)

    return {
        "explanation": explanation,
        "breakdown": breakdown
    }


def _parse_explanation_response(raw_text: str) -> tuple[str, dict | None]:
    try:
        lines = raw_text.strip().split("\n")
        explanation_lines = []
        breakdown = {}

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
                    reason = re.sub(r'^[\-\s]+', '', reason)
                    breakdown[key] = {
                        "level": level,
                        "reason": reason.capitalize() if reason else ""
                    }
                    matched = True
                    break

            if not matched and line.strip():
                if not any(key.replace("_", " ") in line_lower for key in patterns.keys()):
                    explanation_lines.append(line.strip())

        explanation = " ".join(explanation_lines).strip()

        if not breakdown:
            breakdown = None

        return explanation, breakdown

    except Exception as e:
        print(f"Error parsing explanation response: {e}")
        return raw_text.strip(), None


def generate_explanation_simple(interests: str, faculty_name: str, papers: list[str]) -> str:
    result = generate_explanation(interests, faculty_name, papers)
    return result["explanation"]
