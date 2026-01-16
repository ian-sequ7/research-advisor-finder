"""
Research Path Explorer - Session management and LLM orchestration.

Helps students narrow vague research interests to specific directions
through guided paper exploration.
"""
import os
import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

from anthropic import Anthropic
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.services.embeddings import get_embedding
from app.models import Paper, Faculty


# In-memory session storage
_sessions: dict[str, "ExploreSession"] = {}


@dataclass
class ExploreSession:
    """Session state for exploration."""
    session_id: str
    initial_interest: str
    shown_paper_ids: list[int] = field(default_factory=list)
    conversation: list[dict] = field(default_factory=list)  # [{role, content}]
    preferences: dict = field(default_factory=lambda: {"liked": [], "disliked": [], "curious": []})
    created_at: datetime = field(default_factory=datetime.now)
    rounds: int = 0


def create_session(initial_interest: str) -> ExploreSession:
    """Create a new exploration session."""
    session_id = str(uuid.uuid4())
    session = ExploreSession(
        session_id=session_id,
        initial_interest=initial_interest
    )
    _sessions[session_id] = session
    return session


def get_session(session_id: str) -> Optional[ExploreSession]:
    """Get an existing session."""
    return _sessions.get(session_id)


def delete_session(session_id: str) -> None:
    """Delete a session."""
    _sessions.pop(session_id, None)


def get_diverse_papers(db: Session, interest: str, exclude_ids: list[int], limit: int = 4) -> list[Paper]:
    """
    Get diverse papers matching an interest.
    Uses embedding similarity but tries to maximize diversity.
    """
    query_embedding = get_embedding(interest)

    # Build exclusion clause
    exclude_clause = ""
    params = {
        "embedding": str(query_embedding),
        "limit": limit * 3  # Get more, then diversify
    }

    if exclude_ids:
        exclude_clause = "AND id != ALL(:exclude_ids)"
        params["exclude_ids"] = exclude_ids

    # Get candidate papers by similarity
    results = db.execute(
        text(f"""
            SELECT id, title, abstract, year, venue, faculty_id,
                   1 - (embedding <=> :embedding) as similarity
            FROM papers
            WHERE embedding IS NOT NULL
                AND abstract IS NOT NULL
                AND abstract != ''
                {exclude_clause}
            ORDER BY embedding <=> :embedding
            LIMIT :limit
        """),
        params
    ).fetchall()

    if not results:
        return []

    # Simple diversity: take every Nth paper to spread out
    diverse_papers = []
    step = max(1, len(results) // limit)
    for i in range(0, len(results), step):
        if len(diverse_papers) >= limit:
            break
        row = results[i]
        paper = db.query(Paper).filter(Paper.id == row.id).first()
        if paper:
            diverse_papers.append(paper)

    return diverse_papers


def get_similar_papers(db: Session, query: str, exclude_ids: list[int], limit: int = 4) -> list[Paper]:
    """Get papers similar to a refined query."""
    query_embedding = get_embedding(query)

    exclude_clause = ""
    params = {
        "embedding": str(query_embedding),
        "limit": limit
    }

    if exclude_ids:
        exclude_clause = "AND id != ALL(:exclude_ids)"
        params["exclude_ids"] = exclude_ids

    results = db.execute(
        text(f"""
            SELECT id
            FROM papers
            WHERE embedding IS NOT NULL
                AND abstract IS NOT NULL
                {exclude_clause}
            ORDER BY embedding <=> :embedding
            LIMIT :limit
        """),
        params
    ).fetchall()

    paper_ids = [r.id for r in results]
    return db.query(Paper).filter(Paper.id.in_(paper_ids)).all()


def extract_preferences_and_refine(session: ExploreSession, user_response: str) -> dict:
    """
    Use LLM to extract preferences from user response and generate refined query.
    Returns: {preferences: {liked, disliked, curious}, refined_query: str, is_converged: bool}
    """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Build conversation context
    conv_context = f"Initial interest: {session.initial_interest}\n"
    conv_context += f"Rounds so far: {session.rounds}\n"
    if session.preferences["liked"]:
        conv_context += f"Previously liked: {', '.join(session.preferences['liked'])}\n"
    if session.preferences["curious"]:
        conv_context += f"Previously curious about: {', '.join(session.preferences['curious'])}\n"

    prompt = f"""Analyze this user's response about research papers they were shown.

{conv_context}

User's latest response:
"{user_response}"

Extract:
1. What aspects they LIKED (topics, methods, applications they found interesting)
2. What they DISLIKED or found uninteresting
3. What they're CURIOUS about or want to explore more
4. A refined search query (5-10 keywords) to find papers matching their evolving interests
5. Whether they seem to have CONVERGED on a specific direction (true if consistent interests over 2+ responses)

Respond in this exact JSON format:
{{
    "liked": ["topic1", "topic2"],
    "disliked": ["topic3"],
    "curious": ["aspect1", "aspect2"],
    "refined_query": "keyword1 keyword2 keyword3 specific research terms",
    "is_converged": false,
    "convergence_reason": "why or why not converged"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse JSON from response
    import json
    try:
        result = json.loads(response.content[0].text)
    except json.JSONDecodeError:
        # Fallback: extract what we can
        result = {
            "liked": [],
            "disliked": [],
            "curious": [],
            "refined_query": user_response,
            "is_converged": False
        }

    return result


def synthesize_direction(session: ExploreSession) -> dict:
    """
    Synthesize a research direction from the exploration conversation.
    Returns: {title: str, description: str}
    """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Build full context
    context = f"Initial interest: {session.initial_interest}\n\n"
    context += "Conversation history:\n"
    for msg in session.conversation:
        context += f"- {msg['role']}: {msg['content'][:200]}...\n"

    context += f"\nFinal preferences:\n"
    context += f"- Liked: {', '.join(session.preferences['liked'])}\n"
    context += f"- Curious about: {', '.join(session.preferences['curious'])}\n"

    prompt = f"""Based on this research exploration conversation, synthesize the student's research direction.

{context}

Provide:
1. A concise title for their research direction (5-10 words)
2. A 2-3 sentence description of what specifically interests them

Respond in JSON format:
{{
    "title": "Research Direction Title",
    "description": "Description of their specific interests and what they want to explore."
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    try:
        result = json.loads(response.content[0].text)
    except json.JSONDecodeError:
        result = {
            "title": "Research Direction",
            "description": f"Based on your interest in {session.initial_interest} and exploration of related topics."
        }

    return result


def match_faculty_to_direction(db: Session, direction_description: str, limit: int = 3) -> list[dict]:
    """
    Find faculty matching the synthesized research direction.
    Returns list of {faculty, similarity, explanation}
    """
    query_embedding = get_embedding(direction_description)

    results = db.execute(
        text("""
            SELECT id, name, affiliation, h_index, paper_count,
                   semantic_scholar_id, research_tags,
                   1 - (embedding <=> :embedding) as similarity
            FROM faculty
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> :embedding
            LIMIT :limit
        """),
        {"embedding": str(query_embedding), "limit": limit}
    ).fetchall()

    matches = []
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    for row in results:
        # Get faculty's top paper
        top_paper = db.query(Paper).filter(
            Paper.faculty_id == row.id
        ).order_by(Paper.citation_count.desc()).first()

        # Generate brief explanation
        explanation_prompt = f"""In 1-2 sentences, explain why this faculty member matches a student interested in: "{direction_description}"

Faculty: {row.name} at {row.affiliation}
Research areas: {', '.join(row.research_tags or [])}
Top paper: {top_paper.title if top_paper else 'N/A'}"""

        explanation_response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            messages=[{"role": "user", "content": explanation_prompt}]
        )

        matches.append({
            "faculty": {
                "id": row.id,
                "name": row.name,
                "affiliation": row.affiliation,
                "h_index": row.h_index,
                "paper_count": row.paper_count,
                "semantic_scholar_id": row.semantic_scholar_id,
                "research_tags": row.research_tags or []
            },
            "similarity": float(row.similarity),
            "explanation": explanation_response.content[0].text.strip(),
            "key_paper": top_paper.title if top_paper else None
        })

    return matches


def generate_exploration_prompt(papers: list[Paper], round_num: int) -> str:
    """Generate the prompt to show user with papers."""
    if round_num == 0:
        return "Here are some papers spanning different areas related to your interest. Which aspects resonate with you? What draws you to them or what's missing?"
    elif round_num < 3:
        return "Based on your interests, here are more focused papers. What specifically interests you about these? What would you like to explore further?"
    else:
        return "We're narrowing in on your interests. Do any of these capture what you're looking for? Or would you like to see faculty working in this area?"
