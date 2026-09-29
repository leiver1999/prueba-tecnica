"""API de pedidos. Crear la app con otra ruta permite pruebas aisladas."""
from contextlib import asynccontextmanager
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .schemas import ESTADOS, PedidoCreate, PedidoOut, EstadoUpdate
from . import repository

DEFAULT_DB = Path(__file__).resolve().parents[1] / 'data' / 'pedidos.sqlite3'


def create_app(db_path: str | Path | None = None) -> FastAPI:
    database = Path(db_path) if db_path is not None else Path(os.getenv('DATABASE_PATH', str(DEFAULT_DB)))

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        init_db(database)
        yield

    application = FastAPI(title='Pedidos - Prueba Junior', version='1.0.0', lifespan=lifespan)
    application.state.db_path = database
    origins = os.getenv('CORS_ORIGINS',
        'http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000')
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[x.strip() for x in origins.split(',') if x.strip()],
        allow_credentials=False,
        allow_methods=['GET', 'POST', 'PATCH'],
        allow_headers=['Content-Type'],
    )

    @application.get('/health')
    def health():
        return {'status': 'ok'}

    @application.get('/pedidos', response_model=list[PedidoOut])
    def list_pedidos(request: Request, estado: str | None = None):
        if estado is not None and estado not in ESTADOS:
            raise HTTPException(status_code=400, detail='Estado no valido')
        return repository.list_pedidos(request.app.state.db_path, estado)

    @application.get('/pedidos/{pedido_id}', response_model=PedidoOut)
    def get_pedido(request: Request, pedido_id: int):
        pedido = repository.get_pedido(request.app.state.db_path, pedido_id)
        if pedido is None:
            raise HTTPException(status_code=404, detail='Pedido no encontrado')
        return pedido

    @application.post('/pedidos', response_model=PedidoOut, status_code=201)
    def create_pedido(request: Request, payload: PedidoCreate):
        cliente = payload.cliente.strip()
        descripcion = payload.descripcion.strip()
        if not cliente or not descripcion:
            raise HTTPException(
                status_code=400,
                detail='Cliente y descripcion no pueden estar vacios'
            )
        return repository.create_pedido(
            request.app.state.db_path, cliente, descripcion)

    @application.patch('/pedidos/{pedido_id}/estado', response_model=PedidoOut)
    def update_estado(request: Request, pedido_id: int, payload: EstadoUpdate):
        if payload.estado not in ESTADOS:
            raise HTTPException(status_code=400, detail='Estado no valido')
        pedido = repository.update_estado(
            request.app.state.db_path, pedido_id, payload.estado)
        if pedido is None:
            raise HTTPException(status_code=404, detail='Pedido no encontrado')
        return pedido

    return application


app = create_app()
