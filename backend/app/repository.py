"""Consultas parametrizadas. Mantener SQLite; no se necesita un ORM."""
from pathlib import Path
from .db import connection


def list_pedidos(db_path: str | Path, estado: str | None = None) -> list[dict]:
    # TODO P2: aplicar el filtro cuando estado no sea None.
    with connection(db_path) as conn:
        rows = conn.execute('SELECT * FROM pedidos ORDER BY id').fetchall()
    return [dict(row) for row in rows]


def get_pedido(db_path: str | Path, pedido_id: int) -> dict | None:
    with connection(db_path) as conn:
        row = conn.execute('SELECT * FROM pedidos WHERE id = ?', (pedido_id,)).fetchone()
    return dict(row) if row is not None else None


def create_pedido(db_path: str | Path, cliente: str, descripcion: str) -> dict:
    with connection(db_path) as conn:
        cursor = conn.execute(
            'INSERT INTO pedidos (cliente, descripcion) VALUES (?, ?)',
            (cliente, descripcion),
        )
        row = conn.execute('SELECT * FROM pedidos WHERE id = ?', (cursor.lastrowid,)).fetchone()
    return dict(row)


# TODO P3: agregar la operacion de actualizacion de estado.
