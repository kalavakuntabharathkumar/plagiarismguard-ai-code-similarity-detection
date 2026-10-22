# PlagiarismGuard — AI-Assisted Code Similarity Detection

A portfolio starter demonstrating a FastAPI service, AST-based structural normalization, scikit-learn TF-IDF similarity, MySQL persistence, Celery + RabbitMQ background jobs, pytest, and Kubernetes/Jenkins deployment scaffolding.

> The scoring pipeline is a screening aid, not proof of plagiarism. Similarity scores can be affected by templates, common algorithms, language choice, and legitimate collaboration. Keep human review in the decision loop. The LLM explanation adapter is intentionally optional and does not make an accusation.

## Quick start
Requires Python 3.11+, Docker Compose, and optionally `kubectl`.

1. Copy `.env.example` to `.env`.
2. Start MySQL and RabbitMQ: `docker compose up -d`.
3. Create a virtual environment and install: `python -m venv .venv`; activate it; `pip install -r requirements.txt`.
4. Run API: `uvicorn app.main:app --reload`.
5. Open `http://127.0.0.1:8000/docs`.
6. Run tests: `pytest`.

## Endpoints
- `GET /health`
- `POST /api/compare` with `{"language":"python","source_a":"...","source_b":"..."}`
- `POST /api/scans` queues a background scan.
- `GET /api/scans/{task_id}` returns task status/result.

## Similarity approach
1. Parse Python source with `ast` and normalize identifiers/literals.
2. Build token streams and TF-IDF vectors.
3. Compute cosine similarity and produce an explainable heuristic score.
4. Optional LLM adapter can generate a neutral explanation from selected evidence; configure `LLM_API_URL` and `LLM_API_KEY` before enabling it.

## Fairness and safety
Treat results as signals for reviewer investigation, never as automatic disciplinary decisions. Store only necessary source material, restrict access, define retention, and audit false positives.
