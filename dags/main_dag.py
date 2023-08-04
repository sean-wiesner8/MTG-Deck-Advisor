from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator


schedule_interval = "@daily"
start_date = days_ago(1)
default_args = {"owner": "airflow", "depends_on_past": False, "retries": 1}

with DAG(
    dag_id="mtg_analysis_pipeline",
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=True,
) as dag:

    # scrape_untapped_data = BashOperator(
    #     task_id="scrape_untapped_data",
    #     bash_command="chmod +x /opt/airflow/tasks/bash_scripts/scrape_untapped.sh && /opt/airflow/tasks/bash_scripts/scrape_untapped.sh ", do_xcom_push=True,
    # )

    # scrape_mtg_data = BashOperator(
    #     task_id="scrape_mtg_data",
    #     bash_command="python /opt/airflow/tasks/scraper_scripts/scrape_mtg.py ",
    # )

    # scrape_mtgtop8_data = BashOperator(
    #     task_id="scrape_mtgtop8_data",
    #     bash_command="python /opt/airflow/tasks/scraper_scripts/scrape_mtgtop8.py ",
    # )

    upload_to_s3 = BashOperator(
        task_id="upload_to_s3",
        bash_command="python /opt/airflow/tasks/data_lake_upload.py ",
    )

(
    # scrape_untapped_data
    # scrape_mtg_data
    # >> scrape_mtgtop8_data
    upload_to_s3
)
