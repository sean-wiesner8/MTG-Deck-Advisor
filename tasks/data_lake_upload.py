import boto3
from dotenv import dotenv_values
from botocore.exceptions import NoCredentialsError


def data_lake_upload():
    # load config
    config = dotenv_values("/opt/airflow/tasks/configuration.env")

    # get upload files
    files = ["tmp/mtgtop8_data.json",
             "tmp/standard_cards.json"]

    # set config variables
    AWS_BUCKET = config["s3-bucket"]
    AWS_ACCESS_KEY_ID = config["aws_access_key_id"]
    AWS_SECRET_ACCESS_KEY = config["aws_secret_access_key"]

    def connect_s3():
        """
        Create a boto3 session and connect to the S3 Resource

        Returns:
            connection to the S3 bucket
        """
        try:
            s3_conn = boto3.resource(
                "s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
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
