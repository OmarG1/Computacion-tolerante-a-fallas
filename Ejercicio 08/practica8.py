import requests
import json
from collections import namedtuple
from contextlib import closing
import sqlite3
from prefect import flow
from prefect import task, Flow
import json
from collections import namedtuple
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime



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

# Clean data
@task
def clean_data(parsed):
    try:
        with open('apods.json', 'r') as f:
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
    min = 9999
    max = 0
    plus = 0
    for i in range(0, len(cleaned)):
        if min > int(cleaned[i][1][:4]):
            min = int(cleaned[i][1][:4])
        if max < int(cleaned[i][1][:4]):
            max = int(cleaned[i][1][:4])
        plus += int(cleaned[i][1][:4])

    ave = plus / len(cleaned)
    data = [min, max, int(ave)]
    return data


@task
def show_data(data):
    
    labels = ['Min', 'Max', 'Average']
    fig, ax = plt.subplots()
    bars = ax.bar(labels, data, 0.30, color="skyblue", edgecolor='black')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom')  

    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig("graph"+date+".png")   
     
# load
@task
def store_apods(parsed):
    
    with open('apods.json', 'w') as f:
        json.dump(parsed, f, indent=4)


@flow
def task_flow():
    raw = get_apod_data()
    parsed = parse_apod_data(raw)
    cleaned = clean_data(parsed)
    dataAnalyzed = analyze_data(cleaned)
    show_data(dataAnalyzed)
    store_apods(cleaned)

task_flow()

