from transformers import pipeline
from sqlalchemy.orm import Session
import crud
import models
# Initialize the transformer pipeline for symptom to medicine suggestion
model = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')

# Function to suggest medicine based on symptom
# chat_transformer.py


def suggest_medicine_based_on_symptom(symptom: str, possible_meds: list) -> str:
    result = model(symptom, possible_meds)
    best_match = result['labels'][0]
    return best_match


    # Step 2: Use transformer model to predict the best matching medicine
    possible_meds = [med.name for med in homeo_meds]  # extracting medicine names from database
    
    # Step 3: Get transformer prediction for the symptom
    result = model(symptom, possible_meds)
    
    # Step 4: Return the best matching medicine
    best_match = result['labels'][0]  # the top label (medicine) suggested by the model
    return best_match
