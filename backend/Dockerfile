FROM python:3.11-slim
	#wd
WORKDIR /app
	# 1st layer cache
COPY requirements/text .

RUN pip install --no-cahce-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

Create 'backend/requirements.txt':
```
fastapi>=0.109.0
uvicorn>=0.27.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.9
pgvector>=0.2.4
pydantic>=2.5.0
pydantic-settings>=2.1.0
openai>=1.0.0
anthropic>=0.18.0
requests>=2.31.0
python-dotenv>=1.0.0
numpy>=1.24.0
