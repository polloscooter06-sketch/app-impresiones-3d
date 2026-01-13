from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models.cotizacion import Cotizacion
from fastapi import Body
from app.core.database import SessionLocal, engine, Base
from app.models.solicitud import SolicitudImpresion
from typing import Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
# -------------------------
# APP
# -------------------------
app = FastAPI()

# Static files (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# -------------------------
# DATABASE
# -------------------------
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# ROUTES
# -------------------------

# FORMULARIO
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# GUARDAR IMPRESIÓN
@app.post("/crear")
def crear_impresion(
    nombre_impresion: Optional[str] = Form(None),
    nombre_cliente: str =Form(...),
    telefono: str =Form(...),
    descripcion: str = Form (...),
    cantidad: int = Form(...),
    estado: str = Form(...),
    db: Session = Depends(get_db)
):
    nueva = SolicitudImpresion(
        nombre_impresion=nombre_impresion,
        nombre_cliente=nombre_cliente,
        telefono=telefono,
        descripcion=descripcion,
        cantidad=cantidad,
        estado=estado
    )

    db.add(nueva)
    db.commit()

    return RedirectResponse("/impresiones", status_code=303)

# LISTA DE IMPRESIONES
@app.get("/impresiones")
def listar_impresiones(request: Request, db: Session = Depends(get_db)):
    impresiones = db.query(SolicitudImpresion)\
        .order_by(SolicitudImpresion.fecha_creacion.desc())\
        .all()

    return templates.TemplateResponse(
        "lista.html",
        {
            "request": request,
            "impresiones": impresiones
        }
    )

@app.post("/impresiones/{impresion_id}/estado")
def cambiar_estado(
    impresion_id: int,
    estado: str = Form(...),
    db: Session = Depends(get_db)
):
    impresion = db.query(SolicitudImpresion).filter(SolicitudImpresion.id ==impresion_id).first()

    if not impresion:
        return {"error": "Impresión no encontrada"}

    impresion.estado = estado
    impresion.fecha_estado = datetime.utcnow()
    db.commit()

    return RedirectResponse("/impresiones", status_code=303)

@app.post("/impresiones/{impresion_id}/cotizacion")
def crear_cotizacion(
    impresion_id: int,
    data: dict = Body(...),
    db: Session = Depends(get_db)
):
    cotizacion = Cotizacion(
        impresion_id=impresion_id,
        cantidad_producto=data["cantidad_producto"],
        tiempo_impresion=data["tiempo_impresion"],
        tiempo_postprocesado=data["tiempo_postprocesado"],
        tiempo_pintado=data["tiempo_pintado"],
        margen_ganancia=data["margenGanancia"],
        descripcion=data["descripcion"]
    )

    db.add(cotizacion)
    db.commit()

    return {"ok": True}

# -------------------------
# FORMULARIO COTIZACIÓN
# -------------------------
@app.get("/impresiones/{impresion_id}/cotizar")
def form_cotizacion(request: Request, impresion_id: int):
    return templates.TemplateResponse(
        "cotizacion.html",
        {
            "request": request,
            "impresion_id": impresion_id
        }
    )

from datetime import datetime, timedelta

@app.get("/impresiones/atrasadas")
def impresiones_atrasadas(db: Session = Depends(get_db)):
    limite = datetime.utcnow() - timedelta(hours=1)

    return (
        db.query(SolicitudImpresion)
        .filter(
            SolicitudImpresion.fecha_estado < limite,
            SolicitudImpresion.estado.notin_(["terminado", "cancelado"])
        )
        .all()
    )