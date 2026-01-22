from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db
import schemas
from router import auth, patients, doctors, insurance

# Create the database tables
schemas.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Management System API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allowing all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(auth.router)
app.include_router(insurance.router)


@app.get("/")
def home():
    return {"message": "Hospital Management System API is Live!"}


@app.get("/check-connection")
def check_db(db: Session = Depends(get_db)):
    return {"status": "Successfully connected to the database!"}
