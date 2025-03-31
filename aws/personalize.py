import boto3

def setup_personalize( account_id: str, region: str):
    """
    Create a personalize schema
    """
    solution_name = "filmz-solution"

    personalize = boto3.client("personalize")


    # Create a solution
    solution_arn = f"arn:aws:personalize:{region}:{account_id}:solution/{solution_name}"

    # Create a solution version
    response = personalize.create_solution_version(
        solutionArn= solution_arn
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
        solutionVersionArn= solution_version_arn,
        minProvisionedTPS=1
    )
    compute_arn = response["campaignArn"]

    output= {
        "solution_arn": solution_arn,
        "solution_version_arn": solution_version_arn,
        "campaign_arn": compute_arn, # Needed for client to get recommendations
    }

    print(output)
    return output
