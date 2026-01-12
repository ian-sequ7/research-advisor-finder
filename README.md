# Research Advisor Finder

An AI-powered tool to help PhD applicants discover faculty whose research interests align with theirs.

### Development Notes
- Currently in progress
    - MVP finished Jan 3rd
    - Improved Faculty Numbers Jan 8th
    - Added Resources Page + Faculty Badges Jan 12th

## Live Demo

**Frontend:** https://research-advisor-frontend.vercel.app

**Backend:** https://research-advisor-finder-production.up.railway.app

## Cool Features

- *Semantic Search:* Research interests in natural language
- *Smart Matching:* Use OpenAI embeddings to find faculty that align with interests
- *Faculty Profiles:* View h-index, citation counts, and top papers
- *Faculty Badges:* Junior Faculty (h-index < 30) and Established Faculty (h-index > 60) badges help identify career stage
- *AI Explanations:* Claude explains reasoning for matching to certain faculty
- *Resources Page:* Comprehensive guide on cold emailing professors, coffee chat best practices, questions to ask advisors, PhD application timeline, and red flags to watch for
- *Top Programs:* Currently includes faculty from MIT, CMU, Berkeley, and more

## Tech Stack

**Frontend:**
- Next.js 16
- React
- Tailwind CSS
- shadcn/ui

**Backend:**
- FastAPI
- PostgreSQL + pgvector
- SQLAlchemy

**AI/ML:**
- OpenAI Embeddings (text-embedding-3-small)
- Anthropic Claude (match explanations)
- Semantic Scholar API (faculty data)

**Deployment:**
- Vercel (frontend)
- Railway (backend + database)

## How It Works

1. User describes their research interests
2. Query is converted to a vector embedding using OpenAI
3. pgvector finds faculty with similar research embeddings
4. Results ranked by cosine similarity
5. Claude generates personalized explanations for top matches

## Local Development

### Prerequisites
- Docker
- Node.js 18+
- Python 3.11+

### Backend
```bash
cd backend
docker-compose up -d
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - For generating embeddings
- `ANTHROPIC_API_KEY` - For match explanations

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL

## License

MIT
