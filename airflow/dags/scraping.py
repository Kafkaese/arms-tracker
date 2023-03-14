# Airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor

# Taro
from taro.data import scrapers, database

# Utils
from datetime import datetime

def _run_scrapers():
    conflicts = scrapers.get_armed_conflicts()
    results = [scrapers.get_conflict_belligerents(conflict['url']) for conflict in conflicts]

with DAG('scraping', start_date=datetime(2023, 3, 14), schedule='@daily', catchup=False) as dag:
    
    # Check can reach website
    is_wiki_available = HttpSensor(
        task_id = 'is_wiki_available',
        endpoint="",
        http_conn_id = 'https://en.wikipedia.org/wiki/List_of_ongoing_armed_conflicts' 
    )
    
    # Run scrapers 
    
    run_scrapers = PythonOperator(
        task_id = 'run_scrapers',
        python_callable=_run_scrapers
    )
    
    # Write data to sqlite
    
is_wiki_available >> run_scrapers 
