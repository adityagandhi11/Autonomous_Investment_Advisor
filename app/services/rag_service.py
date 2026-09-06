"""Local retrieval service for investment guidance documents."""

import hashlib
import math
from pathlib import Path
import re
import sqlite3


KNOWLEDGE_DIR = Path(__file__).resolve().parents[2] / "knowledge"
VECTOR_DB = Path(__file__).resolve().parents[2] / ".investment_vectors.db"
EMBEDDING_SIZE = 256


def _embed(text: str) -> list[float]:
    """Create a small deterministic local embedding without external services."""
    vector = [0.0] * EMBEDDING_SIZE
    for token in re.findall(r"[a-z0-9]+", text.lower()):
        index = int(hashlib.sha256(token.encode()).hexdigest(), 16) % EMBEDDING_SIZE
        vector[index] += 1.0
    magnitude = math.sqrt(sum(value * value for value in vector))
    return [value / magnitude for value in vector] if magnitude else vector


def _similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def retrieve_investment_guidance(query: str, limit: int = 3) -> list[dict]:
    """Retrieve relevant local guidance using a persistent SQLite vector store."""
    documents = list(KNOWLEDGE_DIR.glob("*.md"))
    if not documents:
        return []

    with sqlite3.connect(VECTOR_DB) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS documents "
            "(source TEXT PRIMARY KEY, content TEXT NOT NULL, embedding TEXT NOT NULL)"
        )
        for document in documents:
            content = document.read_text(encoding="utf-8")
            embedding = ",".join(map(str, _embed(content)))
            connection.execute(
                "INSERT OR REPLACE INTO documents(source, content, embedding) VALUES (?, ?, ?)",
                (document.name, content, embedding),
            )
        rows = connection.execute("SELECT source, content, embedding FROM documents").fetchall()

    query_embedding = _embed(query)
    ranked = sorted(
        (
            _similarity(query_embedding, [float(value) for value in embedding.split(",")]),
            source,
            content,
        )
        for source, content, embedding in rows
    )
    return [
        {"content": content, "source": source, "score": round(score, 4)}
        for score, source, content in ranked[-limit:][::-1]
    ]