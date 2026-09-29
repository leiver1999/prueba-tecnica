"""Carga datos solo en una base vacia. No borra registros existentes."""
import os
from .main import DEFAULT_DB
from .db import init_db, connection

SEED = [
    ('Cliente Demo A', 'Entrega de repuestos', 'pendiente'),
    ('Cliente Demo B', 'Traslado de cajas', 'en_proceso'),
    ('Cliente Demo C', 'Entrega de documentos', 'completado'),
    ('Cliente Demo D', 'Recoleccion en bodega', 'pendiente'),
    ('Cliente Demo E', 'Entrega local', 'en_proceso'),
    ('Cliente Demo F', 'Traslado de muestras ficticias', 'pendiente'),
]


def main() -> None:
    path = os.getenv('DATABASE_PATH', str(DEFAULT_DB))
    init_db(path)
    with connection(path) as conn:
        count = conn.execute('SELECT COUNT(*) FROM pedidos').fetchone()[0]
        if count:
            print(f'Base con {count} pedidos: no se modificaron datos.')
            return
        conn.executemany('INSERT INTO pedidos (cliente, descripcion, estado) VALUES (?, ?, ?)', SEED)
    print('6 pedidos ficticios creados. Conteos: pendiente=3, en_proceso=2, completado=1.')


if __name__ == '__main__':
    main()
