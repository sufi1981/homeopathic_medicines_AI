import sqlite3
import csv

# Database connection
sqliteConn = sqlite3.connect('sql.db')
cursor = sqliteConn.cursor()

# Create homeo_med table
create_medicine_table = '''
CREATE TABLE IF NOT EXISTS homeo_med(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
)
'''

# Create symptom table
create_symptom_table = '''
CREATE TABLE IF NOT EXISTS symptom(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symptom_name TEXT NOT NULL UNIQUE
)
'''

# Create mapping table
create_symptom_medicine_table = '''
CREATE TABLE IF NOT EXISTS symptom_medicine(
    symptom_id INTEGER,
    medicine_id INTEGER,
    FOREIGN KEY (symptom_id) REFERENCES symptom(id),
    FOREIGN KEY (medicine_id) REFERENCES homeo_med(id),
    PRIMARY KEY (symptom_id, medicine_id)
)
'''

# Create tables if not exist
cursor.execute(create_medicine_table)
cursor.execute(create_symptom_table)
cursor.execute(create_symptom_medicine_table)

print('✅ Tables created or verified.')

# Insert medicines into homeo_med table
with open('clean_medicine_list.csv', newline='', encoding='utf-8') as file:
    contents = csv.reader(file)
    next(contents)  # Skip header
    for row in contents:
        cursor.execute("INSERT OR IGNORE INTO homeo_med (name) VALUES (?)", (row[0].strip(),))

print('✅ Medicines inserted from clean_medicine_list.csv.')

# Insert symptoms into symptom table AND create mappings
with open('medicine_symptoms.csv', newline='', encoding='utf-8') as file:
    contents = csv.reader(file)
    next(contents)  # Skip header
    for row in contents:
        symptom_name = row[0].strip()
        medicine_name = row[1].strip()

        # Insert symptom
        cursor.execute("INSERT OR IGNORE INTO symptom (symptom_name) VALUES (?)", (symptom_name,))
        
        # Get IDs
        cursor.execute("SELECT id FROM symptom WHERE symptom_name = ?", (symptom_name,))
        symptom_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM homeo_med WHERE name = ?", (medicine_name,))
        result = cursor.fetchone()
        if result:
            medicine_id = result[0]

            # Insert mapping
            cursor.execute(
                "INSERT OR IGNORE INTO symptom_medicine (symptom_id, medicine_id) VALUES (?, ?)",
                (symptom_id, medicine_id)
            )

print('✅ Symptoms inserted and mappings created from medicine_symptoms.csv.')

# Commit and close
sqliteConn.commit()
sqliteConn.close()
print('✅ All done. DB closed.')
