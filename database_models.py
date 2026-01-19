# this is the file where we define our database models
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Define the Patient model
Base = declarative_base()


# Define the Patient model
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    weight = Column(Integer)
    height = Column(Integer)
