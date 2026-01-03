import os
from anthropic import Anthropic

def generate_explanation(interests: str, faculty_name: str, papers: list[str]) -> str:
    """Generate match explanation with Claude."""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    paper_list = "\n".join(f"- {p}" for p in papers[:5])
    
    prompt = f"""A prospective PhD student is interested in: {interests}

They matched with Professor {faculty_name}, who has written papers including:
{paper_list}

In 2-3 sentences, explain why this professor might be a good research advisor match. Be specific about the connection between the student's interests and the professor's research."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=250,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text
