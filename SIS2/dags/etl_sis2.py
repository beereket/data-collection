import json
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from extract import scrape_euronews
from transform import clean_data
from load_to_db import save_to_db
import os




DATA_DIR = "/opt/airflow/data"
os.makedirs(DATA_DIR, exist_ok=True)


with DAG(
    "euronews_scraper",
    description="Scraper for Euronews Asia using Playwright",
    start_date=datetime(2025, 1, 1),

) as dag:

    scrape_task = PythonOperator(
        task_id="scrape_euronews_task",
        python_callable=scrape_euronews,
        retries=1,
        retry_delay=timedelta(seconds=5),
    )

    transform_task = PythonOperator(
        task_id="clean_data_task",
        python_callable=clean_data,
        retries=1,
        retry_delay=timedelta(seconds=5),
    )

    load_to_db_task = PythonOperator(
        task_id="load_to_db_task",
        python_callable=save_to_db,
        retries=1,
        retry_delay=timedelta(seconds=5),
    )

    scrape_task >> transform_task >> load_to_db_task
