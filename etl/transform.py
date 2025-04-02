import pandas as pd
import os
from datetime import datetime
import random
import time

def transform_items_data(items: list[dict]) -> list[dict]:
    """
    Transform the items data to meet AWS personalize items schema before loaded into the data warehouse
    """
    new_items = []
    for item in items:
        # Drop item with missing values
        if not item["id"] or not item["genreId"] or not item["releaseDate"] or not item["title"] or not item["rating"] or not item["description"]:
            continue

        new_item = {}
        new_item["ITEM_ID"] = str(item.pop("id"))
        new_item["GENRE_ID"] = str( item.pop("genreId"))
        new_item["RELEASE_DATE"] = int(datetime.strptime(str(item.pop("releaseDate")), "%Y-%m-%d %H:%M:%S").timestamp())
        new_item["TITLE"] = item.pop("title")
        new_item["RATING"] = float(item.pop("rating"))
        new_item["DESCRIPTION"] = item.pop("description")
        new_items.append(new_item)
    return new_items

def transform_users_data(users: list[dict]) -> list[dict]:
    """
    Transform the users data to meet AWS personalize users schema before loaded into the data warehouse
    """
    for user in users:
        user.pop("createdAt")
        user.pop("updatedAt")
        user["USER_ID"] = user.get("id")
        user["AGE"] = int(user.pop("id"))
        user["FIRST_NAME"] = user.pop("firstname")
        user["LAST_NAME"] = user.pop("lastname")
    return 

def generate_interaction_data(num_interactions=1000):
    interactions = []
    current_time = int(time.time())

    for _ in range(num_interactions):
        interaction = {
            'USER_ID': random.randint(1, 25),
            'ITEM_ID': random.randint(1, 2000),
            'TIMESTAMP': current_time - random.randint(0, 31536000)  # up to one year ago
        }
        interactions.append(interaction)

    return interactions

def transform_interactions_data(interactions: list[dict]) -> list[dict]:
    """
    Transform the interactions data to meet AWS personalize interactions schema before loaded into the data warehouse
    """
    for interaction in interactions:
        # Drop interaction with missing values
        if not interaction["userId"] or not interaction["itemId"] or not interaction["createdAt"]:
            continue

        interaction["USER_ID"] = interaction.pop("userId")
        interaction["ITEM_ID"] = interaction.pop("itemId")
        # Convert eg. 2025-03-31 00:21:03.762000 to timestamp
        interaction["TIMESTAMP"] = int(datetime.strptime(str(interaction.pop("createdAt")).split(" ")[0], "%Y-%m-%d").timestamp())
    
    fake_interactions = generate_interaction_data(2000)
    interactions.extend(fake_interactions)
    print("interactions", len(interactions))
    return interactions

def transform_data(
    users: list[dict], 
    items: list[dict], 
    interactions: list[dict]
) -> None:
    """
    Transform the data to meet AWS personalize schema before loaded into the data warehouse
    Use pandas to save the data as CSV files in ./tmp directory
    """
    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    # Delete the existing files
    os.system("rm -rf tmp/users.csv")
    os.system("rm -rf tmp/items.csv")
    os.system("rm -rf tmp/interactions.csv")
    
    users_df = pd.DataFrame(transform_users_data(users))
    users_df.to_csv("tmp/users.csv", index=False)

    items_df = pd.DataFrame(transform_items_data(items))
    items_df.to_csv("tmp/items.csv", index=False)

    interactions_df = pd.DataFrame(transform_interactions_data(interactions))
    interactions_df.to_csv("tmp/interactions.csv", index=False)
    return None
    
