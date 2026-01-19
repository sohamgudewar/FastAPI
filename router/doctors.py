from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
import schemas
from schemas import DoctorCreate
from database import get_db
from fastapi import APIRouter
# Create the database tables

# schemas.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/doctors",
    tags=["doctors"],
)


@router.post("/doctor/")
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = schemas.Doctor(name=doctor.name, specialty=doctor.specialty)
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor


@router.get("/doctor/{doctor_id}")
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(schemas.Doctor).filter(schemas.Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found in database")
    return db_doctor


@router.put("/doctor_id/{id}")
def update_doctor(id: int, updated_data: DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = db.query(schemas.Doctor).filter(schemas.Doctor.id == id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found in database")
    db_doctor.name = updated_data.name
    db_doctor.specialty = updated_data.specialty
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@router.delete("/doctor_id/{id}")
def delete_doctor(id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(schemas.Doctor).filter(schemas.Doctor.id == id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found in database")
    db.delete(db_doctor)
    db.commit()
    return {"detail": "Doctor deleted successfully"}
