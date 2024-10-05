from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from airflow.utils.dates import days_ago # type: ignore
from datetime import datetime


def today():
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year

    string_date = f"Today is the day {day} of the month of {month} from year {year}"

    filename = f"/home/kennedy/KR/Programação/01.Exercícios/DE/Airflow/airflow-testes/files/python-dag/{year}-{month}-{day}"

    with open(filename, 'w') as file:
        file.write(string_date)

dag = DAG(
    'python_dag',
    description='python script',
    schedule_interval="@daily",
    start_date=days_ago(5),
    catchup=True
)

python_task = PythonOperator(
    task_id='save_date',
    python_callable=today,
    dag=dag
)

python_task



