from pydantic import BaseModel
from datetime import datetime

class SolicitudCreate(BaseModel):
    nombre_impresion: str | None = None
    nombre_cliente: str
    telefono: str
    descripcion: str
    cantidad: int

class SolicitudResponse(SolicitudCreate):
    id: int
    fecha_creacion: datetime
    estado: str

    class Config:
        from_attributes = True