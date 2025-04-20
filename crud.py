from sqlalchemy.orm import Session
from models import HomeoMed, Symptom, SymptomMedicine
import models

def create_medicine(db: Session, name: str):
    db_medicine = models.HomeoMed(name=name)
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine

def create_symptom(db: Session, symptom_name: str):
    db_symptom = models.Symptom(symptom_name=symptom_name)
    db.add(db_symptom)
    db.commit()
    db.refresh(db_symptom)
    return db_symptom

def suggest_medicines(db: Session, symptom_name: str):
    symptom_obj = db.query(Symptom).filter(Symptom.symptom_name == symptom_name).first()
    if not symptom_obj:
        return {"message": "❌ Symptom not found"}

    links = db.query(SymptomMedicine).filter(SymptomMedicine.symptom_id == symptom_obj.id).all()
    medicine_ids = [link.medicine_id for link in links]

    if not medicine_ids:
        return {"message": "⚠️ No medicines linked to this symptom"}

    medicines = db.query(HomeoMed).filter(HomeoMed.id.in_(medicine_ids)).all()
    return [med.name for med in medicines]

# ✅ New function to get all medicines
def get_homeo_meds(db: Session):
    return db.query(HomeoMed).all()
