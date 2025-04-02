import boto3
import time
import nanoid

BUCKET_NAME = "filmz-ml-data"



def cresate_users_dataset_impot_job(account_id: str, region: str):
    roleArn = f"arn:aws:iam::{account_id}:role/service-role/AmazonPersonalize-ExecutionRole-1743384123100"
    """
    Create a personalize dataset import job for users
    """
    personalize = boto3.client("personalize")

    # Create a dataset import job
    response = personalize.create_dataset_import_job(
        datasetArn=f"arn:aws:personalize:{region}:{account_id}:dataset/fimz-recommendation-dataset/USERS",
        dataSource={
            "dataLocation": f"s3://{BUCKET_NAME}/users.csv"
        },
        roleArn=roleArn,
        jobName=f"filmz-users-import-job-{nanoid.generate(size=10)}"
    )

    while True:
        dataset_import_job = personalize.describe_dataset_import_job(
            datasetImportJobArn=response["datasetImportJobArn"]
        )
        status = dataset_import_job["datasetImportJob"]["status"]
        print(f"User Dataset import job status: {status}")
        if status == "ACTIVE" or status == "CREATE FAILED":
            break
        time.sleep(30)

    return response


def create_items_dataset_impot_job(account_id: str, region: str):
    """
    Create a personalize dataset import job for items
    """
    roleArn = f"arn:aws:iam::{account_id}:role/service-role/AmazonPersonalize-ExecutionRole-1743384123100"

    personalize = boto3.client("personalize")

    # Create a dataset import job
    response = personalize.create_dataset_import_job(
        datasetArn=f"arn:aws:personalize:{region}:{account_id}:dataset/fimz-recommendation-dataset/ITEMS",
        dataSource={
            "dataLocation": f"s3://{BUCKET_NAME}/items.csv"
        },
        roleArn=roleArn,
        jobName=f"filmz-items-import-job-{nanoid.generate(size=10)}"
    )

    while True:
        dataset_import_job = personalize.describe_dataset_import_job(
            datasetImportJobArn=response["datasetImportJobArn"]
        )
        status = dataset_import_job["datasetImportJob"]["status"]
        print(f"Item Dataset import job status: {status}")
        if status == "ACTIVE" or status == "CREATE FAILED":
            break
        time.sleep(30)

    return response


def create_interactions_dataset_impot_job(account_id: str, region: str):
    """
    Create a personalize dataset import job for interactions
    """
    roleArn = f"arn:aws:iam::{account_id}:role/service-role/AmazonPersonalize-ExecutionRole-1743384123100"

    personalize = boto3.client("personalize")

    # Create a dataset import job
    response = personalize.create_dataset_import_job(
        datasetArn=f"arn:aws:personalize:{region}:{account_id}:dataset/fimz-recommendation-dataset/INTERACTIONS",
        dataSource={
            "dataLocation": f"s3://{BUCKET_NAME}/interactions.csv"
        },
        roleArn=roleArn,
        jobName= f"filmz-interactions-import-job-{nanoid.generate(size=10)}"
    )

    while True:
        dataset_import_job = personalize.describe_dataset_import_job(
            datasetImportJobArn=response["datasetImportJobArn"]
        )
        status = dataset_import_job["datasetImportJob"]["status"]
        print(f"Interaction Dataset import job status: {status}")
        if status == "ACTIVE" or status == "CREATE FAILED":
            break
        time.sleep(30)

    return response


def setup_personalize(account_id: str, region: str):

    cresate_users_dataset_impot_job(account_id, region)
    create_items_dataset_impot_job(account_id, region)
    create_interactions_dataset_impot_job(account_id, region)

    solution_name = "filmz-recommendation-solution-2"

    personalize = boto3.client("personalize")

    # Create a solution
    solution_arn = f"arn:aws:personalize:{region}:{account_id}:solution/{solution_name}"

    # Create a solution version
    response = personalize.create_solution_version(
        solutionArn=solution_arn,
    )

    # Wait for the solution version to be active
    while True:
        solution_version = personalize.describe_solution_version(
            solutionVersionArn=response["solutionVersionArn"]
        )
        status = solution_version["solutionVersion"]["status"]
        print(f"Solution version status: {status}")
        if status == "ACTIVE" or status == "CREATE FAILED":
            break
        import time
        time.sleep(60)

    solution_version_arn = response["solutionVersionArn"]
    # Create a campaign
    response = personalize.create_campaign(
        name="filmz-campaign",
        solutionVersionArn=solution_version_arn,
        minProvisionedTPS=1
    )
    compute_arn = response["campaignArn"]

    output = {
        "solution_arn": solution_arn,
        "solution_version_arn": solution_version_arn,
        "campaign_arn": compute_arn,  # Needed for client to get recommendations
    }

    print(output)
    return output
