from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas
from schemas import PatientCreate
# Create the database tables
# schemas.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@router.post("/patient/")
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = schemas.Patient(name=patient.name, age=patient.age, weight=patient.weight, height=patient.height)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


@router.get("/patient/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(schemas.Patient).filter(schemas.Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found in database")
    return db_patient


@router.get("/patients_list/{limit}")
def get_patients(limit: int, db: Session = Depends(get_db)):
    patients = db.query(schemas.Patient).limit(limit).all()
    return {"patients": patients}


@router.put("/patient_id/{id}")
def update_patient(id: int, updated_data: PatientCreate, db: Session = Depends(get_db)):
    db_patient = db.query(schemas.Patient).filter(schemas.Patient.id == id).first()

    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db_patient.name = updated_data.name
    db_patient.age = updated_data.age

    db.commit()
    db.refresh(db_patient)
    return {"message": "Update successful", "patient": db_patient}


@router.delete("/patient_id/{id}")
def delete_patient(id: int, name: str, db: Session = Depends(get_db)):
    db_patient = db.query(schemas.Patient).filter(schemas.Patient.id == id).first()
    db_patient = db.query(schemas.Patient).filter(schemas.Patient.name == name).first()

    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(db_patient)
    db.commit()
    return {"message": "Deletion successful", "id_deleted": id}
