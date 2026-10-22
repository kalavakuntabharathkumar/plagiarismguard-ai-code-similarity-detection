from __future__ import annotations

from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.similarity import compare_sources
from app.tasks import celery_app, compare_task

app = FastAPI(title="PlagiarismGuard API", version="1.0.0")


class CompareRequest(BaseModel):
    language: str = Field(default="python", max_length=30)
    source_a: str = Field(min_length=1, max_length=100_000)
    source_b: str = Field(min_length=1, max_length=100_000)


class ScanRequest(CompareRequest):
    pass


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/compare")
def compare(request: CompareRequest) -> dict:
    if request.language != "python":
        raise HTTPException(status_code=400, detail="This starter currently supports Python comparisons only.")
    return compare_sources(request.source_a, request.source_b)


@app.post("/api/scans", status_code=202)
def create_scan(request: ScanRequest) -> dict[str, str]:
    task = compare_task.delay(request.language, request.source_a, request.source_b)
    return {"task_id": task.id, "status": "queued"}


@app.get("/api/scans/{task_id}")
def get_scan(task_id: str) -> dict:
    result = AsyncResult(task_id, app=celery_app)
    if result.failed():
        return {"task_id": task_id, "status": "failed"}
    if not result.ready():
        return {"task_id": task_id, "status": "queued"}
    return {"task_id": task_id, "status": "complete", "result": result.result}
