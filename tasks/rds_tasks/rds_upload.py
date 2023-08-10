import psycopg2
import os
from dotenv import dotenv_values


curr_dir = os.getcwd()
config = dotenv_values(f"{curr_dir}/configuration.env")


def create_conn():
    try:
        conn = psycopg2.connect(
            host=config["rds_instance_endpoint"].split(":")[0],
            port=config["rds_port"],
            user=config["rds_username"],
            password=config["rds_password"],
            dbname=config["rds_database_name"],
        )

        return conn
    except Exception as exception:
        print(exception)


def prepare_query(query_filename: str) -> str:

    query_cursor = open(
        f"{curr_dir}/rds_tasks/sql_queries/{query_filename}.sql", "r")
    query = query_cursor.read()

    return query


def main():
    conn = create_conn()
    cursor = conn.cursor()

    create_tables_query = prepare_query("create_tables")
    cursor.execute(create_tables_query)

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
