import os
import boto3
from dotenv import dotenv_values
from botocore.exceptions import NoCredentialsError


def data_lake_upload():
    # load config
    script_path = os.getcwd()
    config = dotenv_values("/opt/airflow/tasks/configuration.env")
    print(f"config: {config}")

    # get upload files
    files = [f"scraper_scripts/mtgtop8_data.json",
             f"scraper_scripts/standard_cards.json"]

    # set config variables
    AWS_BUCKET = config["s3-bucket"]
    print(AWS_BUCKET)

    def connect_s3():
        """
        Create a boto3 session and connect to the S3 Resource

        Returns:
            connection to the S3 bucket
        """
        try:
            s3_conn = boto3.resource(
                "s3", aws_access_key_id=config["aws_access_key_id"], aws_secret_access_key=config["aws_secret_access_key"])
            return s3_conn
        except NoCredentialsError as e:
            raise (e)

    def upload_csv_s3():
        """
        Upload both CSV files to the S3 bucket
        """
        s3_conn = connect_s3()
        for file in files:
            s3_conn.meta.client.upload_file(
                Filename=f"/opt/airflow/tasks/{file}", Bucket=AWS_BUCKET, Key=file)

    upload_csv_s3()


def main():
    data_lake_upload()


if __name__ == "__main__":
    main()
