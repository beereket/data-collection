import json
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from extract import scrape_euronews
from transform import clean_data
from load_to_db import save_to_db
import os
import requests
import logging
from pathlib import Path
import traceback

DATA_DIR = "/opt/airflow/data"
os.makedirs(DATA_DIR, exist_ok=True)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow")
LOG_DIR = Path(AIRFLOW_HOME) / "logs" / "sis2_etl"

LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "project_api_to_dwh.log"


logger = logging.getLogger("project_api_to_dwh")
logger.setLevel(logging.INFO)
if not logger.handlers:
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)

def task_fail_alert_telegram(context):
    task = context['task_instance'].task_id
    dag = context['task_instance'].dag_id
    msg = f"❌ Task Failed\nDAG: {dag}\nTask: {task}"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=10)
        logger.info("Sent failure alert to Telegram.")
    except Exception as e:
        logger.error(f"Telegram alert failed: {e}")
        logger.debug(traceback.format_exc())

def success_notification(**context):
    try:
        msg = "✅ ETL DAG успешно завершён!"
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
        logger.info("Sent success notification to Telegram.")
    except Exception as e:
        logger.error(f"Failed to send success notification: {e}")
        logger.debug(traceback.format_exc())


with DAG(
    "euronews_scraper",
    description="Scraper for Euronews Asia using Playwright",
    start_date=datetime(2025, 1, 1),
    on_failure_callback=task_fail_alert_telegram,
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

    success_task = PythonOperator(
        task_id='success_notification',
        python_callable=success_notification
    )

    scrape_task >> transform_task >> load_to_db_task >> success_task
