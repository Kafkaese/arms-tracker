# Airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor

# Taro
from taro.data import scrapers, database

# Utils
from datetime import datetime

with DAG('scrapers', start_date=datetime(2023, 3, 14), schedule_interval='@daily', catchup=False) as dag:
    
    # Check can reach website
    is_wiki_available = HttpSensor(
        task_id = 'is_wiki_available',
        http_conn_id = 'https://en.wikipedia.org/wiki/List_of_ongoing_armed_conflicts' 
    )
    
    # Run scrapers 
    
    # Write data to sqlite
    
    