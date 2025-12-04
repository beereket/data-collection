# **Euronews Asia Scraper — ETL Pipeline (Airflow + Playwright + SQLite)**

This project implements a complete ETL (Extract–Transform–Load) pipeline for collecting news articles from **Euronews Asia** using **Playwright** for web scraping and **Apache Airflow** for orchestration.
The pipeline extracts article metadata, cleans and normalizes it, and stores it in a local SQLite database.

---

## 🚀 **Features**

* **Automated scraping** of Euronews Asia (first 5 paginated pages).
* **Playwright (headless Chromium)** for reliable, JavaScript-rendered scraping.
* **ETL pipeline orchestrated by Airflow**:

  * `extract`: Scrapes raw article metadata.
  * `transform`: Cleans/normalizes/validates data.
  * `load`: Saves unique articles into SQLite.
* **XCom-based communication** between ETL stages.
* **Dockerized Airflow environment** (optional).
* Ensures **idempotent** inserts using `INSERT OR IGNORE`.
* Outputs both **JSON file** and **final database**.

---

## 🔄 **ETL Pipeline Overview**

### **1. Extract — `scrape_euronews()`**

* Uses Playwright (Chromium) to navigate Euronews Asia pages.
* Extracts:

  * Title
  * Description
  * URL
  * Published date
* Saves raw output to `data/euronews_data.json`.
* Pushes records to XCom.

### **2. Transform — `clean_data()`**

* Loads scraped list from XCom.
* Converts to pandas DataFrame.
* Removes empty/invalid entries.
* Cleans whitespace, formats dates, forces string types.
* Pushes cleaned list to XCom.

### **3. Load — `save_to_db()`**

* Creates SQLite DB (`final.db`) if missing.
* Creates `articles` table.
* Inserts cleaned articles using `INSERT OR IGNORE`.
* Avoids duplicates based on article `link`.

---

## 🛠️ **Running the Project**

### **Recommended: Docker Compose (Airflow)**

1. Start Airflow environment:

```bash
docker-compose up -d
```

2. Access Airflow UI:

```
http://localhost:8080
```

3. Enable & trigger DAG:
   `euronews_scraper`

Airflow will run all tasks in the correct ETL order:

```
scrape_euronews_task → clean_data_task → load_to_db_task
```

---

## 🧪 **Running Locally (Without Docker)**

> Useful for debugging Playwright or data-cleaning logic.

### 1. Create venv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright browsers

```bash
playwright install chromium
```

### 4. Run functions manually (debug mode)

```python
from extract import scrape_euronews
from transform import clean_data
from load_to_db import save_to_db

raw = scrape_euronews()
clean = clean_data(euronews_data=raw)
save_to_db(cleaned_data=clean)
```

---

## 🗄️ **Output**

### ✔ JSON

`/opt/airflow/data/euronews_data.json`

### ✔ SQLite Database

`/opt/airflow/data/final.db`

### SQLite Schema:

```sql
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    link TEXT UNIQUE,
    description TEXT,
    date DATE
);
```

To inspect DB:

```bash
sqlite3 final.db
SELECT * FROM articles LIMIT 10;
```

---

## 🐛 Troubleshooting

### **Airflow does not detect DAG**

* Ensure container mounts your local `dags/` folder.
* Restart scheduler:

```bash
docker-compose restart airflow-scheduler
```

### **Playwright errors**

Run inside container:

```bash
playwright install chromium
```

### **Empty dataset?**

* Euronews sometimes blocks bots → User-Agent already spoofed.
* Add proxy if needed.



