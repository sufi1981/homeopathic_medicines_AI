from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import crud, models, database
import chat_transformer
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from models import SymptomMedicine
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
app = FastAPI()

# Allowing CORS for your frontend URL (Replace with your frontend URL if required)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    database.init_db()  # Ensure tables are created at the start

@app.post("/medicines/")
def create_medicine(name: str, db: Session = Depends(get_db)):
    return crud.create_medicine(db=db, name=name)

@app.post("/symptoms/")
def create_symptom(symptom_name: str, db: Session = Depends(get_db)):
    return crud.create_symptom(db=db, symptom_name=symptom_name)

@app.get("/suggest")
def suggest_medicines(symptom: str = Query(...), db: Session = Depends(get_db)):
    return crud.suggest_medicines(db=db, symptom_name=symptom)

@app.get("/ai-suggest")
def ai_suggest(symptom: str, db: Session = Depends(get_db)):
    try:
        # Fetch all medicines from the database
        homeo_meds = crud.get_homeo_meds(db=db)
        possible_meds = [med.name for med in homeo_meds]

        # AI model will suggest the best medicine for the given symptom
        best_match = chat_transformer.suggest_medicine_based_on_symptom(symptom, possible_meds)

        # Return the suggested medicine
        return {"suggested_medicine": best_match}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in AI suggestion: {e}")

@app.post("/link-symptom-medicine/")
def link_symptom_medicine(symptom_id: int = Body(...), medicine_id: int = Body(...), db: Session = Depends(get_db)):
    link = SymptomMedicine(symptom_id=symptom_id, medicine_id=medicine_id)
    db.add(link)
    db.commit()
    return {"message": "✅ Symptom and Medicine linked successfully"}
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})