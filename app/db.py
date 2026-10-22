"""Small MySQL persistence layer using parameterized queries."""
import os
from contextlib import contextmanager
from typing import Iterator

import pymysql
from pymysql.cursors import DictCursor

from app.config import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER


@contextmanager
def connection() -> Iterator[pymysql.connections.Connection]:
    conn = pymysql.connect(
        host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE, cursorclass=DictCursor, autocommit=True,
    )
    try:
        yield conn
    finally:
        conn.close()


def initialize_schema() -> None:
    with connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS scan_results (
              id BIGINT AUTO_INCREMENT PRIMARY KEY,
              task_id VARCHAR(100) NOT NULL,
              language VARCHAR(30) NOT NULL,
              score DECIMAL(5,2) NOT NULL,
              result_json JSON NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              INDEX scan_task_id_idx (task_id)
            )
            """)
