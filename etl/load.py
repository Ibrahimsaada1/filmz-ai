import boto3
import os

def load_data_to_s3(file_path: str, bucket_name: str, key: str):
    """
    Load the data into S3
    """
    s3 = boto3.client("s3")
    with open(file_path, "rb") as data:
        s3.upload_fileobj(data, bucket_name, key)
    return None

def load_data_to_warehouse(
        bucket_name: str,
):
    """
    Load the data into the data warehouse
    """

    # Load items.csv into the data warehouse
    load_data_to_s3("tmp/items.csv", bucket_name, "items.csv")

    # Load users.csv into the data warehouse
    load_data_to_s3("tmp/users.csv", bucket_name, "users.csv")

    # Load interactions.csv into the data warehouse
    load_data_to_s3("tmp/interactions.csv", bucket_name, "interactions.csv")
    return None

def clean_up():
    """
    Clean up the temporary files
    """
    os.system("rm -rf tmp")
    return None

def try_load_data_to_warehouse(bucket_name: str):
    """
    Load the data into the data warehouse
    """
    try:
        load_data_to_warehouse(bucket_name)
    except Exception as e:
        print(f"Error loading data to the data warehouse: {e}")
        raise e
    finally:
        clean_up()
    return None