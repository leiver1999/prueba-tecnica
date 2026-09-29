"""Consultas parametrizadas. Mantener SQLite; no se necesita un ORM."""
from pathlib import Path
from .db import connection


def list_pedidos(db_path: str | Path, estado: str | None = None) -> list[dict]:
    with connection(db_path) as conn:
        if estado is None:
            rows = conn.execute('SELECT * FROM pedidos ORDER BY id').fetchall()
        else:
            rows = conn.execute(
                'SELECT * FROM pedidos WHERE estado = ? ORDER BY id', (estado,)
            ).fetchall()
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


def update_estado(db_path: str | Path, pedido_id: int, estado: str) -> dict | None:
    with connection(db_path) as conn:
        conn.execute(
            'UPDATE pedidos SET estado = ? WHERE id = ?', (estado, pedido_id)
        )
        row = conn.execute('SELECT * FROM pedidos WHERE id = ?', (pedido_id,)).fetchone()
    return dict(row) if row is not None else None
