"""Celery task entry point. Queue processing is separate from the API."""
import json
import os

from celery import Celery

from app.similarity import compare_sources

broker = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
celery_app = Celery("plagiarismguard", broker=broker, backend="rpc://")


@celery_app.task(name="plagiarismguard.compare")
def compare_task(language: str, source_a: str, source_b: str) -> dict:
    if language != "python":
        return {"status": "unsupported", "message": "This starter currently supports Python AST comparisons only."}
    return {"status": "complete", **compare_sources(source_a, source_b)}
