from airflow import DAG
from airflow.operators.bash_operator import BashOperator # type: ignore
from airflow.utils.dates import days_ago # type: ignore
from datetime import datetime

# Define the DAG
dag = DAG(
    'bash_dag',
    description='hello world in bash',
    schedule_interval="@daily",
    start_date=days_ago(10),
    catchup=True
)

# Define the BashOperator task
hello_world_task = BashOperator(
    task_id='hello_world_task',
    bash_command='source /home/kennedy/KR/Programação/01.Exercícios/DE/Airflow/venv/bin/activate && python -c "print(\'Hello, world!\')"  > /home/kennedy/KR/Programação/01.Exercícios/DE/Airflow/airflow-testes/files/bash-dag/{{ ds }}output.txt',
    dag=dag
)

# Define the task dependencies
hello_world_task
