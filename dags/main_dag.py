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

    scrape_mtg_data = BashOperator(
        task_id="scrape_mtg_data",
        bash_command="python /opt/airflow/tasks/scraper_scripts/scrape_mtg.py ",
    )

    scrape_mtgtop8_data = BashOperator(
        task_id="scrape_mtgtop8_data",
        bash_command="python /opt/airflow/tasks/scraper_scripts/scrape_mtgtop8.py ",
    )

    upload_to_s3_raw = BashOperator(
        task_id="upload_to_s3_raw",
        bash_command="python /opt/airflow/tasks/data_lake_upload.py raw ",
    )

    validate_data = BashOperator(
        task_id="validate_data",
        bash_command="python /opt/airflow/tasks/validate.py ",
    )

    upload_to_s3_prep = BashOperator(
        task_id="upload_to_s3_prep",
        bash_command="python /opt/airflow/tasks/data_lake_upload.py prep ",
    )

    rds_upload = BashOperator(
        task_id="rds_upload",
        bash_command="python /opt/airflow/tasks/rds_tasks/rds_upload.py ",
    )

    redshift_upload = BashOperator(
        task_id="redshift_upload",
        bash_command="python /opt/airflow/tasks/redshift_tasks/redshift_rds_upload.py ",
    )

(
    scrape_mtg_data
    >> scrape_mtgtop8_data
    >> upload_to_s3_raw
    >> validate_data
    >> upload_to_s3_prep
    >> rds_upload
    >> redshift_upload
)
