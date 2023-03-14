# Airflow
from airflow import DAG
from airflow.operators.python import PythonOperator

# Taro
from taro.data import scrapers, database

# Utils
from datetime import datetime

with DAG('scrapers', start_date=datetime(2023, 3, 14), schedule_interval='@daily', catchup=False) as dag:
    
    # Run scrapers 
    
    # Write data to sqlite
    
    