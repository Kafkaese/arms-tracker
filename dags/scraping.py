# Airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor

# Taro
from taro.data import scrapers, database

# Utils
from datetime import datetime

# Scraper callable
def _get_conflicts(ti):
    conflicts = scrapers.get_armed_conflicts()
    ti.xcom_push(key='conflict_data', value=conflicts)
    
def _get_belligerents(ti):
    conflicts = ti.xcom_pull(key='conflict_data', task_id='get_conflicts')
    results = [scrapers.get_conflict_belligerents(conflict['url']) for conflict in conflicts]
    ti.xcom_push(key='belligerent_data')

# Databse callable
def _save_data(ti):
    data_dict = ti.xcom_pull(key='data', task_id = 'run_scraper')
    database.create_write_dict_db()

with DAG('scraping', start_date=datetime(2023, 3, 14), schedule='@daily', catchup=False) as dag:
    
    # Check can reach website
    is_wiki_available = HttpSensor(
        task_id = 'is_wiki_available',
        endpoint="",
        http_conn_id = 'https://en.wikipedia.org/wiki/List_of_ongoing_armed_conflicts' 
    )
    
    # Run scrapers 
    get_conflicts = PythonOperator(
        task_id = 'run_conflicts',
        python_callable=_get_conflicts
    )
    
    get_belligerents = PythonOperator(
        task_id = 'get_belligerents',
        python_callable=_get_belligerents
    )
    
    # Write data to sqlite
    save_data = PythonOperator(
        task_id = 'save_data',
        python_callable = _save_data
    )
    
is_wiki_available >> get_conflicts >>  get_belligerents >> save_data
