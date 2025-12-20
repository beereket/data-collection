import sqlite3
import os

DATA_DIR = "/opt/airflow/data"  
os.makedirs(DATA_DIR, exist_ok=True)

def save_to_db(**context):
    cleaned_data = context['ti'].xcom_pull(key='cleaned_data', task_ids='clean_data_task')
    
    if not cleaned_data or not isinstance(cleaned_data, list):
        return
    
    db_path = os.path.join(DATA_DIR, 'final.db')  

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            description TEXT,
            date DATE
        )
    ''')
    
    for row in cleaned_data:
        cursor.execute('''
            INSERT OR IGNORE INTO articles (title, link, description, date)
            VALUES (?, ?, ?, ?)
        ''', (row['title'], row['link'], row['description'], row['date']))
    
    conn.commit()
    conn.close()
    
    print(f"Saved {len(cleaned_data)} articles to {db_path}")
