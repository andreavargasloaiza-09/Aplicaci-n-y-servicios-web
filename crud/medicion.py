from sqlalchemy import select
from sqlalchemy.orm import Session
from models.medicion import Medicion
from schemas.medicion import MedicionCreate, MedicionUpdate

def get_all(db: Session) -> list[Medicion]:
    return list(db.scalars(select(Medicion).order_by(Medicion.id)).all())

def get(db: Session, medicion_id: int) -> Medicion | None:
    return db.get(Medicion, medicion_id)

def create(db: Session, data: MedicionCreate) -> Medicion:
    medicion = Medicion(**data.model_dump())
    db.add(medicion)
    db.commit()
    db.refresh(medicion)
    return medicion

def update(db: Session, medicion: Medicion, data: MedicionUpdate) -> Medicion:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(medicion, field, value)
    db.commit()
    db.refresh(medicion)
    return medicion

def delete(db: Session, medicion: Medicion) -> None:
    db.delete(medicion)
    db.commit()