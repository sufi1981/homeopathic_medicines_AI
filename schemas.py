from pydantic import BaseModel

# Pydantic models for validation
class HomeoMedBase(BaseModel):
    name: str

class SymptomBase(BaseModel):
    symptom_name: str

class HomeoMedCreate(HomeoMedBase):
    pass

class SymptomCreate(SymptomBase):
    pass

# Response models
class HomeoMed(HomeoMedBase):
    id: int

    class Config:
        orm_mode = True

class Symptom(SymptomBase):
    id: int

    class Config:
        orm_mode = True
