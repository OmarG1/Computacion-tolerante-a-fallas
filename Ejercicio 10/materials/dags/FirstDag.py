from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.decorators import dag, task
import requests
import json
from collections import namedtuple

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    "start_date": datetime(2024, 1, 1),
}

@task
def get_apod_data():
    r = requests.get("https://api.nasa.gov/planetary/apod", params={'count':10, 'api_key': 'DEMO_KEY'})
    print(r)
    data = r.json()
    return data

@task
def parse_apod_data(raw):
    apods = []
    Apod = namedtuple('Apod', ['title', 'date', 'explanation', 'url'])
    for row in raw:
        this_apod = Apod(
            title=row.get('title'),
            date=row.get('date'),
            explanation=row.get('explanation'),
            url=row.get('url')
        )
        apods.append(this_apod)
    return apods

@task
def clean_data(parsed):
    try:
        with open('./dags/apods.json', 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    for apod in parsed:
        if apod not in existing_data:
            existing_data.append(apod)

    for apod in existing_data:
        if apod == None:
            existing_data.remove(apod)

    return existing_data

@task
def analyze_data(cleaned):
    min_year = 9999
    max_year = 0
    total_years = 0
    for apod in cleaned:
        year = int(apod.date[:4])
        if year < min_year:
            min_year = year
        if year > max_year:
            max_year = year
        total_years += year

    average_year = total_years / len(cleaned)
    return [min_year, max_year, int(average_year)]

@task
def show_data(data):
    print("Data:", data)

@task
def store_apods(parsed):
    with open('./dags/apods.json', 'w') as f:
        json.dump([apod._asdict() for apod in parsed], f, indent=4)

with DAG(
    dag_id='first_dag',
    schedule_interval="@daily",
    default_args=default_args,    
) as dag:
    raw = get_apod_data()
    parsed = parse_apod_data(raw)
    cleaned = clean_data(parsed)
    dataAnalyzed = analyze_data(cleaned)
    show_data(dataAnalyzed)
    store_apods(cleaned)
