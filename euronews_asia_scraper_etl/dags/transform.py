import pandas as pd

def clean_data(**context):

    data = context['ti'].xcom_pull(key='euronews_data', task_ids='scrape_euronews_task')

    print(f"Received {len(data)} items from scrape task") if data else print("No data received")

    df = pd.DataFrame(data)

    df = df.dropna()

    df['title'] = df['title'].str.strip()
    df['description'] = df['description'].fillna('').astype(str).str.strip()
    df['link'] = df['link'].str.strip()

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['date'] = df['date'].dt.strftime('%Y-%m-%d').fillna('')  

    cleaned = df.to_dict('records')

    context['ti'].xcom_push(key='cleaned_data', value=cleaned)

    print(f"Cleaned data contains {len(cleaned)} articles.")
    return cleaned
