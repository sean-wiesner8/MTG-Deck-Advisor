import psycopg2
import os
from dotenv import dotenv_values


curr_dir = os.getcwd()
config = dotenv_values(f"{curr_dir}/configuration.env")


def create_conn():
    try:
        conn = psycopg2.connect(
            host=config["redshift_host"].split(":")[0],
            port=config["redshift_port"],
            user=config["redshift_username"],
            password=config["rds_password"],
            dbname=config["redshift_database_name"],
        )

        return conn
    except Exception as exception:
        print(exception)


def prepare_query(query_filename: str) -> str:

    query_cursor = open(
        f"{curr_dir}/redshift_tasks/sql_queries/{query_filename}.sql", "r")
    query = query_cursor.read()

    return query


def main():
    conn = create_conn()
    cursor = conn.cursor()

    create_tables_query = prepare_query("create_tables")
    load_temp_tables_query = prepare_query("load_temp_tables").format(
        bucket_name=config["s3_bucket"],
        aws_access_id=config["aws_access_key_id"],
        aws_secret_key=config["aws_secret_access_key"],
    )
    load_main_tables_query = prepare_query("load_main_tables")

    cursor.execute(create_tables_query)
    cursor.execute(load_temp_tables_query)
    cursor.execute(load_main_tables_query)

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
