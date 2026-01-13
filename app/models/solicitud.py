from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base

class SolicitudImpresion(Base):
    __tablename__ = "solicitudes_impresion"

    id = Column(Integer, primary_key=True, index=True)
    nombre_impresion = Column(String, nullable=False)
    nombre_cliente = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    cantidad = Column(Integer, nullable=False)
    estado = Column(String, default="Pendiente por cotización")
    fecha_estado = Column(DateTime, nullable=True) 