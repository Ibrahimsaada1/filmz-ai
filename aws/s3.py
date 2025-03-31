import boto3

def get_or_create_s3_bucket()-> dict:
    """
    Create an S3 bucket
    return bucket ARN
    """
    bucket_name = "filmz-ml-data"
    s3 = boto3.client("s3")    
    # Check if the bucket exists
    s3.head_bucket(Bucket=bucket_name)
        
    return {
        "bucket_name": bucket_name,
    }
