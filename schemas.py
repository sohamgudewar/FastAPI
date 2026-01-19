# this is the file where we define our database models
from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal, Dict
from database import tier_1_cities, tier_2_cities


# Define the Patient model table
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    weight = Column(Integer)
    height = Column(Integer)


# Define the Doctor model table
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialty = Column(String, index=True)


# Define the Admin model table
# class Admin(Base):
#     __tablename__ = "admin"
#     username = Column(String, primary_key=True, index=True)
#     hashed_pass = Column(String, index=True)
# # In schemas.py
class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_pass = Column(String)  # Make sure this matches admin_value.hashed_pass


# Pydantic models for data validation and serialization
class PatientCreate(BaseModel):
    name: str
    age: int
    weight: float
    height: float

    class Config:
        from_attributes = True


# Pydantic model for Doctor creation
class DoctorCreate(BaseModel):
    name: str
    specialty: str

    class Config:
        from_attributes = True


# pydantic model to validate incoming data
class UserInput(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the user')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the user')]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description='Height of the user')]
    income_lpa: Annotated[float, Field(..., gt=0, description='Annual salary of the user in lpa')]
    smoker: Annotated[bool, Field(..., description='Is user a smoker')]
    city: Annotated[str, Field(..., description='The city that the user belongs to')]
    occupation: Annotated[Literal['Engineer', 'Driver', 'Teacher', 'Banker','Sales Manager', 'Businessman', 'Factory Worker'], Field(..., description='Occupation of the user')]

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title()
        return v

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3


# Pydantic model for prediction response
class PredictionResponse(BaseModel):
    predicted_category: str = Field(
        ...,
        description="The predicted insurance premium category",
        example="High"
    )
    confidence: float = Field(
        ...,
        description="Model's confidence score for the predicted class (range: 0 to 1)",
        example=0.8432
    )
    class_probabilities: Dict[str, float] = Field(
        ...,
        description="Probability distribution across all possible classes",
        example={"Low": 0.01, "Medium": 0.15, "High": 0.84}
    )
