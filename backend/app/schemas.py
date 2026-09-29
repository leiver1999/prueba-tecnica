from pydantic import BaseModel, ConfigDict, Field

ESTADOS = ('pendiente', 'en_proceso', 'completado')


class PedidoCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    cliente: str = Field(max_length=100)
    descripcion: str = Field(max_length=300)


class EstadoUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    estado: str


class PedidoOut(BaseModel):
    id: int
    cliente: str
    descripcion: str
    estado: str
