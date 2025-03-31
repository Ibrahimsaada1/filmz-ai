from etl.extract import fetch_interactions, fetch_items, fetch_users
from etl.transform import transform_data
from etl.load import try_load_data_to_warehouse
from aws.s3 import get_or_create_s3_bucket
from aws.personalize import setup_personalize
import logging
import boto3
import os


AWS_ACCOUNT_ID = boto3.client("sts").get_caller_identity().get("Account")
AWS_REGION = os.environ.get("AWS_REGION") or "us-east-1"
DATABASE_CONNECTION_STRING = os.environ.get("DATABASE_CONNECTION_STRING")

logging.basicConfig(level=logging.INFO)

def start_training():
    """
    Start the training job
    """

    result = setup_personalize(AWS_ACCOUNT_ID, AWS_REGION)

    return result.get("campaign_arn")


def main():
    logging.info("ETL process started")
    try:
        logging.info("Beginning load")
        interactions = fetch_interactions()
        items = fetch_items()
        users = fetch_users()
        logging.info("Load completed")

        logging.info("Beginning transform")
        transform_data(users, items, interactions)
        logging.info("Transform completed")

        logging.info("Beginning Load")
        bucket_name = get_or_create_s3_bucket().get("bucket_name")

        try_load_data_to_warehouse(bucket_name)
        logging.info("Load completed")
        
        
        logging.info("ETL process completed successfully")

        # Train the AWS personalize model
        start_training()
        return None
    except Exception as e:
        logging.error(f"Error in ETL process: {e}")
        raise e


if __name__ == "__main__":
    main()
