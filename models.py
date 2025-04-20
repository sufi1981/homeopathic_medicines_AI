from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# HomeoMed Model
class HomeoMed(Base):
    __tablename__ = 'homeo_med'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    symptoms = relationship("SymptomMedicine", back_populates="medicine")


# Symptom Model
class Symptom(Base):
    __tablename__ = 'symptom'
    id = Column(Integer, primary_key=True, autoincrement=True)
    symptom_name = Column(String, nullable=False)

    medicines = relationship("SymptomMedicine", back_populates="symptom")


# Symptom-Medicine Mapping Table
class SymptomMedicine(Base):  # ✅ CamelCase Name for import consistency
    __tablename__ = 'symptom_medicine'
    symptom_id = Column(Integer, ForeignKey('symptom.id'), primary_key=True)
    medicine_id = Column(Integer, ForeignKey('homeo_med.id'), primary_key=True)

    symptom = relationship("Symptom", back_populates="medicines")  # ✅ match with 'medicines' in Symptom
    medicine = relationship("HomeoMed", back_populates="symptoms")  # ✅ match with 'symptoms' in HomeoMed
