import boto3
from dotenv import dotenv_values
from botocore.exceptions import NoCredentialsError
import sys
import os


def data_lake_upload(stage):
    # load config

    curr_dir = os.getcwd()
    config = dotenv_values(f"{curr_dir}/configuration.env")

    # get upload files
    files = ["mtgtop8_data.json",
             "standard_cards.json"]

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
                Filename=f"{curr_dir}/tmp/{file}", Bucket=AWS_BUCKET, Key=f"{stage}/{file}")

    upload_csv_s3()


def main():
    stage = sys.argv[1]
    data_lake_upload(stage)


if __name__ == "__main__":
    main()
