# Research Advisor Finder

An AI-powered tool to help PhD applicants discover faculty whose research interests align with theirs.

### Development Notes
- Currently in progress
    - MVP finished Jan 3rd
    - Improved Faculty Numbers Jan 8th
    - Added Resources Page + Faculty Badges Jan 12th
    - Added Explore Mode + Compare Feature Jan 15th
    - Expanded to 12 STEM fields + 1,600+ faculty Jan 19th
    - Expanded to 15,000+ faculty at 45 universities, Feb 2026

## Live Demo

**Frontend:** https://research-advisor-finder.vercel.app

**Backend:** https://research-advisor-finder-production.up.railway.app

## Cool Features

### Search
- *Semantic Search:* Describe research interests in plain English
- *CV Upload:* Drop your CV and let AI extract your research interests
- *Hybrid Matching:* Combines vector similarity, full-text search, and tag matching
- *Smart Filters:* Filter by h-index, result count, or specific universities

### Faculty Profiles
- *Metrics:* H-index, citation counts, paper counts
- *Top Papers:* See each faculty's most-cited work
- *Career Badges:* Junior (h-index < 30), Rising (30-60), Established (> 60)
- *Research Tags:* Quick view of research areas
- *Semantic Scholar Links:* Jump to full profiles

### Compare Mode
- Select up to 3 faculty for side-by-side comparison
- Compare metrics, research areas, and top papers
- Sticky bottom bar for easy access

### Explore Mode
- *Guided Discovery:* For students unsure of their exact interests
- *Paper-Based Exploration:* Browse diverse papers and tell us what catches your eye
- *AI Refinement:* Claude tracks what you like/dislike across multiple rounds
- *Faculty Matching:* Once your direction clarifies, get matched faculty with explanations

### AI Explanations
- Click "Explain Match" on any result
- Claude breaks down the match into Topic Alignment, Paper Relevance, and Research Fit
- Each dimension rated High/Medium/Low

### Resources Page
- *Cold Email Guide:* Template + do's and don'ts
- *Coffee Chat Tips:* How to prep and what to ask
- *Questions for Advisors:* Mentorship, funding, lab culture, outcomes
- *PhD Timeline:* Month-by-month from June to April 15th
- *Red Flags:* Warning signs and how to vet advisors

## Faculty Coverage

**15,000+ faculty** across **12 STEM fields** at **45 US research universities**. Faculty data comes from the Semantic Scholar academic graph.

The project started with about 150 faculty from top CS programs and grew from there.

**Fields:** Computer Science, Statistics, Mathematics, Physics, Electrical Engineering, Economics, Biostatistics, Data Science, Computational Biology, Biomedical Engineering, Materials Science, Chemical Engineering

**Universities:** Berkeley, Boston University, Brown, Caltech, CMU, Columbia, Cornell, Delaware, Duke, Georgia Tech, Harvard, Johns Hopkins, Maryland, MIT, Minnesota, Northwestern, NYU, Ohio State, Princeton, Purdue, Rice, Rutgers, SDSU, Stanford, Texas A&M, UC Davis, UC Irvine, UCLA, UC Riverside, UC San Diego, UC Santa Barbara, UC Santa Cruz, UChicago, UIUC, UMass, UMich, UNC, UPenn, USC, UT Austin, Utah, Virginia Tech, UW, Wisconsin, Yale

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
- slowapi (rate limiting)

**AI/ML:**
- OpenAI Embeddings (text-embedding-3-small)
- Anthropic Claude (explanations + exploration)
- Semantic Scholar API (faculty data)

**Deployment:**
- Vercel (frontend)
- Railway (backend + database)

## How It Works

### Search Flow
1. User describes research interests (or uploads CV)
2. Query expanded for common abbreviations (LLM → large language models)
3. Converted to vector embedding using OpenAI
4. Hybrid search: pgvector similarity + Postgres full-text + tag matching
5. Results ranked and returned with metrics
6. Claude generates explanations on demand

### Explore Flow
1. User enters broad interest ("I like systems and ML")
2. Backend finds diverse papers matching that interest
3. User reacts to papers ("I like the distributed systems ones, not the theory")
4. Claude extracts preferences and refines the search
5. Repeat 2-4 times until direction clarifies
6. Final faculty matching with personalized explanations

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

See `.env.example` files in both `backend/` and `frontend/` directories.

### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - For generating embeddings
- `ANTHROPIC_API_KEY` - For match explanations and explore mode
- `SEMANTIC_SCHOLAR_API_KEY` - For fetching faculty data (optional but recommended)

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL

## API Rate Limits

| Endpoint | Limit |
|----------|-------|
| Search | 30/min |
| Explain | 20/min |
| CV Upload | 10/min |
| Explore Start | 20/min |
| Explore Respond | 40/min |
| Explore Finish | 20/min |

## License

MIT
