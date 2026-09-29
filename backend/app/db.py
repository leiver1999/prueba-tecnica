"""SQLite local: una conexion por operacion, siempre cerrada."""
from contextlib import contextmanager
from pathlib import Path
import sqlite3
from collections.abc import Iterator


@contextmanager
def connection(db_path: str | Path) -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(str(db_path), timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def init_db(db_path: str | Path) -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'pendiente'
                    CHECK (estado IN ('pendiente', 'en_proceso', 'completado'))
            )
        """)
