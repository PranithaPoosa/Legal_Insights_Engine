from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import delete_graph, create_graph, create_embeddings


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
    'retry_delay':timedelta(minutes=5)
}

# Define the DAG
dag = DAG(
    'preprocessing_dag',
    default_args=default_args,
    description='',
    schedule_interval=None,
)

task1 = BashOperator(
    task_id='dbt',
    bash_command="""cd /Users/manideepakreddyaila/Desktop/projects/Legal_Insights_Engine/cap_dbt && dbt run""",
    dag=dag,
)

# Task 2: Python task
def python_task_1():
    delete_graph.main()

task2 = PythonOperator(
    task_id='delete_graph',
    python_callable=python_task_1,
    dag=dag,
)

# Task 3: Python task
def python_task_2():
    create_graph.main()

task3 = PythonOperator(
    task_id='build_graph',
    python_callable=python_task_2,
    dag=dag,
)

# Task 4: Python task
def python_task_3():
    create_embeddings.main()

task4 = PythonOperator(
    task_id='create_embeddings',
    python_callable=python_task_3,
    dag=dag,
)

# Define task dependencies
task1 >> task2 >> task3 >> task4
