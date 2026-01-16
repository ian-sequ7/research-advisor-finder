"""
Research Path Explorer API endpoints.

Helps students narrow vague research interests through guided paper exploration.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Paper, Faculty
from app.schemas import (
    ExploreStartRequest, ExploreStartResponse,
    ExploreRespondRequest, ExploreRespondResponse,
    ExploreFinishRequest, ExploreFinishResponse,
    ExplorePaper, FacultyMatch
)
from app.services.explorer import (
    create_session, get_session, delete_session,
    get_diverse_papers, get_similar_papers,
    extract_preferences_and_refine, synthesize_direction,
    match_faculty_to_direction, generate_exploration_prompt
)

router = APIRouter()


def _paper_to_response(paper: Paper, db: Session) -> ExplorePaper:
    """Convert Paper model to ExplorePaper response."""
    faculty_name = None
    if paper.faculty_id:
        faculty = db.query(Faculty).filter(Faculty.id == paper.faculty_id).first()
        if faculty:
            faculty_name = faculty.name

    return ExplorePaper(
        id=paper.id,
        title=paper.title,
        abstract=paper.abstract[:500] + "..." if paper.abstract and len(paper.abstract) > 500 else paper.abstract,
        year=paper.year,
        venue=paper.venue,
        faculty_name=faculty_name
    )


@router.post("/start", response_model=ExploreStartResponse)
def start_exploration(request: ExploreStartRequest, db: Session = Depends(get_db)):
    """
    Start a new exploration session.
    Returns diverse papers spanning the initial interest area.
    """
    try:
        # Create session
        session = create_session(request.initial_interest)

        # Get diverse papers
        papers = get_diverse_papers(
            db,
            interest=request.initial_interest,
            exclude_ids=[],
            limit=4
        )

        if not papers:
            raise HTTPException(
                status_code=404,
                detail="No papers found matching your interest. Try a broader topic."
            )

        # Track shown papers
        session.shown_paper_ids = [p.id for p in papers]
        session.conversation.append({
            "role": "system",
            "content": f"User interested in: {request.initial_interest}"
        })

        # Generate prompt
        prompt = generate_exploration_prompt(papers, round_num=0)

        return ExploreStartResponse(
            session_id=session.session_id,
            papers=[_paper_to_response(p, db) for p in papers],
            prompt=prompt
        )
    except HTTPException:
        # Re-raise HTTPException as-is
        raise
    except Exception as e:
        # Catch any other errors and return 500
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start exploration session: {str(e)}"
        )


@router.post("/respond", response_model=ExploreRespondResponse)
def respond_to_exploration(request: ExploreRespondRequest, db: Session = Depends(get_db)):
    """
    Process user's response and return next set of papers.
    Extracts preferences, generates refined query, checks convergence.
    """
    try:
        session = get_session(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found or expired")

        # Record user response
        session.conversation.append({
            "role": "user",
            "content": request.response
        })
        session.rounds += 1

        # Extract preferences and get refined query
        result = extract_preferences_and_refine(session, request.response)

        # Update session preferences
        session.preferences["liked"].extend(result.get("liked", []))
        session.preferences["disliked"].extend(result.get("disliked", []))
        session.preferences["curious"].extend(result.get("curious", []))

        # Get next papers based on refined query
        refined_query = result.get("refined_query", request.response)
        papers = get_similar_papers(
            db,
            query=refined_query,
            exclude_ids=session.shown_paper_ids,
            limit=4
        )

        # Check for empty papers
        if not papers:
            raise HTTPException(
                status_code=404,
                detail="No more papers found matching your refined interests. Try finishing the exploration to see faculty matches."
            )

        # Track shown papers
        session.shown_paper_ids.extend([p.id for p in papers])

        # Check if converged
        is_ready = result.get("is_converged", False) or session.rounds >= 4

        # Generate prompt
        prompt = generate_exploration_prompt(papers, round_num=session.rounds)
        if is_ready:
            prompt = "It looks like you're developing a clear research direction! Would you like to see faculty who work in this area, or continue exploring?"

        return ExploreRespondResponse(
            papers=[_paper_to_response(p, db) for p in papers],
            prompt=prompt,
            is_ready=is_ready
        )
    except HTTPException:
        # Re-raise HTTPException as-is
        raise
    except Exception as e:
        # Catch any other errors and return 500
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process exploration response: {str(e)}"
        )


@router.post("/finish", response_model=ExploreFinishResponse)
def finish_exploration(request: ExploreFinishRequest, db: Session = Depends(get_db)):
    """
    Finish exploration and return synthesized direction + matched faculty.
    """
    try:
        session = get_session(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found or expired")

        # Synthesize research direction
        direction = synthesize_direction(session)

        # Match faculty
        faculty_matches = match_faculty_to_direction(
            db,
            direction_description=f"{direction['title']}: {direction['description']}",
            limit=3
        )

        # Clean up session
        delete_session(request.session_id)

        return ExploreFinishResponse(
            direction_summary=direction["title"],
            direction_description=direction["description"],
            faculty_matches=[
                FacultyMatch(
                    faculty=m["faculty"],
                    similarity=m["similarity"],
                    explanation=m["explanation"],
                    key_paper=m["key_paper"]
                )
                for m in faculty_matches
            ]
        )
    except HTTPException:
        # Re-raise HTTPException as-is
        raise
    except Exception as e:
        # Catch any other errors and return 500
        raise HTTPException(
            status_code=500,
            detail=f"Failed to finish exploration: {str(e)}"
        )
