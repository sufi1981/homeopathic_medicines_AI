from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base

# Database setup
DATABASE_URL = "sqlite:///./sql.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Models
class HomeoMed(Base):
    __tablename__ = 'homeo_med'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Symptom(Base):
    __tablename__ = 'symptom'
    id = Column(Integer, primary_key=True, index=True)
    symptom_name = Column(String, index=True)

class SymptomMedicine(Base):
    __tablename__ = 'symptom_medicine'
    symptom_id = Column(Integer, ForeignKey('symptom.id'), primary_key=True)
    medicine_id = Column(Integer, ForeignKey('homeo_med.id'), primary_key=True)

    symptom = relationship(Symptom, back_populates="medicines")
    medicine = relationship(HomeoMed, back_populates="symptoms")

Symptom.medicines = relationship('SymptomMedicine', back_populates="symptom")
HomeoMed.symptoms = relationship('SymptomMedicine', back_populates="medicine")

# FastAPI app setup
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class SymptomCreate(BaseModel):
    symptom_name: str

class Medicine(BaseModel):
    id: int
    name: str

# CRUD operations
def get_medicines_for_symptom(db: Session, symptom_name: str):
    symptom = db.query(Symptom).filter(Symptom.symptom_name == symptom_name).first()
    if symptom:
        medicines = db.query(HomeoMed).join(SymptomMedicine).filter(SymptomMedicine.symptom_id == symptom.id).all()
        return medicines
    return None

# FastAPI Endpoints
@app.post("/symptoms/")
def create_symptom(symptom: SymptomCreate, db: Session = Depends(get_db)):
    db_symptom = Symptom(symptom_name=symptom.symptom_name)
    db.add(db_symptom)
    db.commit()
    db.refresh(db_symptom)
    return db_symptom

@app.get("/suggest_medicines/{symptom_name}")
def suggest_medicines(symptom_name: str, db: Session = Depends(get_db)):
    medicines = get_medicines_for_symptom(db, symptom_name)
    if medicines:
        return medicines
    raise HTTPException(status_code=404, detail="Medicines not found for this symptom")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_app:app", host="127.0.0.1", port=8000, reload=True)