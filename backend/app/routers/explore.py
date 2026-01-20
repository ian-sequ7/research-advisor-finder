from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

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
limiter = Limiter(key_func=get_remote_address)


def _get_faculty_names(papers: list[Paper], db: Session) -> dict[int, str]:
    """Batch fetch faculty names for a list of papers to avoid N+1 queries."""
    faculty_ids = [p.faculty_id for p in papers if p.faculty_id]
    if not faculty_ids:
        return {}

    faculty_list = db.query(Faculty.id, Faculty.name).filter(
        Faculty.id.in_(faculty_ids)
    ).all()

    return {f.id: f.name for f in faculty_list}


def _paper_to_response(paper: Paper, faculty_names: dict[int, str]) -> ExplorePaper:
    faculty_name = faculty_names.get(paper.faculty_id) if paper.faculty_id else None

    return ExplorePaper(
        id=paper.id,
        title=paper.title,
        abstract=paper.abstract[:500] + "..." if paper.abstract and len(paper.abstract) > 500 else paper.abstract,
        year=paper.year,
        venue=paper.venue,
        faculty_name=faculty_name
    )


@router.post("/start", response_model=ExploreStartResponse)
@limiter.limit("20/minute")
def start_exploration(request: Request, body: ExploreStartRequest, db: Session = Depends(get_db)):
    try:
        session = create_session(body.initial_interest)

        papers = get_diverse_papers(
            db,
            interest=body.initial_interest,
            exclude_ids=[],
            limit=4
        )

        if not papers:
            raise HTTPException(
                status_code=404,
                detail="No papers found matching your interest. Try a broader topic."
            )

        session.shown_paper_ids = [p.id for p in papers]
        session.conversation.append({
            "role": "system",
            "content": f"User interested in: {body.initial_interest}"
        })

        prompt = generate_exploration_prompt(papers, round_num=0)

        faculty_names = _get_faculty_names(papers, db)
        return ExploreStartResponse(
            session_id=session.session_id,
            papers=[_paper_to_response(p, faculty_names) for p in papers],
            prompt=prompt
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start exploration session: {str(e)}"
        )


@router.post("/respond", response_model=ExploreRespondResponse)
@limiter.limit("40/minute")
def respond_to_exploration(request: Request, body: ExploreRespondRequest, db: Session = Depends(get_db)):
    try:
        session = get_session(body.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found or expired")

        session.conversation.append({
            "role": "user",
            "content": body.response
        })
        session.rounds += 1

        result = extract_preferences_and_refine(session, body.response)

        session.preferences["liked"].extend(result.get("liked", []))
        session.preferences["disliked"].extend(result.get("disliked", []))
        session.preferences["curious"].extend(result.get("curious", []))

        refined_query = result.get("refined_query", body.response)
        papers = get_similar_papers(
            db,
            query=refined_query,
            exclude_ids=session.shown_paper_ids,
            limit=4
        )

        if not papers:
            raise HTTPException(
                status_code=404,
                detail="No more papers found matching your refined interests. Try finishing the exploration to see faculty matches."
            )

        session.shown_paper_ids.extend([p.id for p in papers])

        is_ready = result.get("is_converged", False) or session.rounds >= 4

        prompt = generate_exploration_prompt(papers, round_num=session.rounds)
        if is_ready:
            prompt = "It looks like you're developing a clear research direction! Would you like to see faculty who work in this area, or continue exploring?"

        faculty_names = _get_faculty_names(papers, db)
        return ExploreRespondResponse(
            papers=[_paper_to_response(p, faculty_names) for p in papers],
            prompt=prompt,
            is_ready=is_ready
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process exploration response: {str(e)}"
        )


@router.post("/finish", response_model=ExploreFinishResponse)
@limiter.limit("20/minute")
def finish_exploration(request: Request, body: ExploreFinishRequest, db: Session = Depends(get_db)):
    try:
        session = get_session(body.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found or expired")

        direction = synthesize_direction(session)

        faculty_matches = match_faculty_to_direction(
            db,
            direction_description=f"{direction['title']}: {direction['description']}",
            limit=3
        )

        delete_session(body.session_id)

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
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to finish exploration: {str(e)}"
        )
