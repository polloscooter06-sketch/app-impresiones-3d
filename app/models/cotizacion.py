from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.core.database import Base

class Cotizacion(Base):
    __tablename__ = "impresion"

    id = Column(Integer, primary_key=True, index=True)
    impresion_id = Column(Integer, ForeignKey("solicitudes_impresion.id"))
    cantidad_producto = Column(Float)
    tiempo_impresion = Column(Float)
    tiempo_postprocesado = Column(Float)
    tiempo_pintado = Column(Float)
    margen_ganancia = Column(Float)
    descripcion = Column(String)
