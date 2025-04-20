import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, HomeoMed, Symptom, SymptomMedicine

# Step 1: CSV file ko pandas se read karo
csv_file = r'D:\adv.homeo.med\medicine_symptoms.csv'  # CSV file ka path yahan dalein
df = pd.read_csv(csv_file)

# Step 2: SQLite engine setup karo
DATABASE_URL = "sqlite:///your_database.db"  # Apna SQLite database URL daalein
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Step 3: Tables ko create karo (agar pehle se nahi hain)
Base.metadata.create_all(bind=engine)

# Step 4: Data ko insert karne ka logic
def insert_data(df):
    db = SessionLocal()
    try:
        for _, row in df.iterrows():
            # Step 4.1: Medicine create karo
            medicine = HomeoMed(name=row['Medicine Name'])
            db.add(medicine)
            db.commit()  # Commit karo taaki id assign ho jaye
            db.refresh(medicine)

            # Step 4.2: Symptoms ko split karo aur unhe insert karo
            symptoms_list = row['Symptoms'].split(", ")
            for symptom_name in symptoms_list:
                symptom = db.query(Symptom).filter(Symptom.symptom_name == symptom_name).first()
                if not symptom:
                    # Agar symptom database mein nahi hai, toh insert karo
                    symptom = Symptom(symptom_name=symptom_name)
                    db.add(symptom)
                    db.commit()
                    db.refresh(symptom)

                # Step 4.3: Symptom-Medicine relationship create karo
                symptom_medicine = SymptomMedicine(symptom_id=symptom.id, medicine_id=medicine.id)
                db.add(symptom_medicine)
            db.commit()
    finally:
        db.close()

# Step 5: Data ko insert karo
insert_data(df)
print("Data inserted successfully.")
