from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.solicitud import SolicitudCreate, CambiarEstado
from app.models.solicitud import SolicitudImpresion
from app.core.database import SessionLocal

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def crear_solicitud(
    data: SolicitudCreate,
    db: Session = Depends(get_db)
):
    solicitud = SolicitudImpresion(**data.dict())
    db.add(solicitud)
    db.commit()
    db.refresh(solicitud)
    return solicitud

@router.get("/")
def listar_solicitudes(db: Session = Depends(get_db)):
    return (
        db.query(SolicitudImpresion)
        .order_by(SolicitudImpresion.fecha_creacion.desc())
        .all()
    )

@router.put("/{id}/estado")
def cambiar_estado(
    id: int,
    data: CambiarEstado,
    db: Session = Depends(get_db)
):
    solicitud = db.query(SolicitudImpresion).filter(
        SolicitudImpresion.id == id
    ).first()

    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    solicitud.estado = data.estado
    db.commit()
    db.refresh(solicitud)

    return {
        "mensaje": "Estado actualizado",
        "estado": solicitud.estado
    }