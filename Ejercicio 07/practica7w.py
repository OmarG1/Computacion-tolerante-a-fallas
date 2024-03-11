import requests
import json
from collections import namedtuple
from contextlib import closing
import sqlite3
from prefect import flow
from prefect import task, Flow
import json
from collections import namedtuple

# extract
@task
def get_apod_data():
    r = requests.get("https://api.nasa.gov/planetary/apod", params={'count':10, 'api_key': 'DEMO_KEY'})
    data = r.json()
    response_json = json.loads(r.text)
    return response_json

# transform
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

# load
@task
def store_apods(parsed):
    with open('apods.json', 'w') as f:
        for apod in parsed:
            f.write(f"{apod.title}\n{apod.date}\n{apod.explanation}\n{apod.url}\n\n")


@flow
def task_flow():
    raw = get_apod_data()
    parsed = parse_apod_data(raw)
    store_apods(parsed)

task_flow()

