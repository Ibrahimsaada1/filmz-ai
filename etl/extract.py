import logging.config
import psycopg
import logging

logging.basicConfig(level=logging.INFO)

DATABASE_CONNECTION_STRING = "postgres://postgres:Filmzdbpass$@filmz-db.c49gimqecoz4.us-east-1.rds.amazonaws.com:5432/appdb"

def fetch_users() -> list[dict]:
    logging.info("Fetching users from the database")
    try:
        fetch_user_sql = """
            SELECT 
                id,
                email,
                firstname,
                lastname,
                "createdAt",
                "updatedAt"
            FROM public."User"
        """
        with psycopg.Connection.connect(DATABASE_CONNECTION_STRING) as conn:
            with conn.cursor() as cur:
                cur.execute(fetch_user_sql)
                users = cur.fetchall()
                users_dict: list[dict] = []
                for user in users:
                    users_dict.append(
                        {
                            "id": user[0],
                            "email": user[1],
                            "firstname": user[2],
                            "lastname": user[3],
                            "createdAt": user[4],
                            "updatedAt": user[5],
                        }
                    )
                return users_dict
            
    except Exception as e:
        logging.error(f"Error fetching users from the database: {e}")
        raise e
            

def fetch_items() -> list[dict]:
    logging.info("Fetching items from the database")
    try:
        # fetch movies
        fetch_movies_sql = """
            SELECT 
                id,
                title,
                "genreId",
                rating,
                description,
                "releaseDate",
                "createdAt",
                "updatedAt"
            FROM public."Movie"
        """
        with psycopg.Connection.connect(DATABASE_CONNECTION_STRING) as conn:
            with conn.cursor() as cur:
                cur.execute(fetch_movies_sql)
                movies = cur.fetchall()
                movies_dict: list[dict] = []
                for movie in movies:
                    movies_dict.append(
                        {
                            "id": movie[0],
                            "title": movie[1],
                            "genreId": movie[2],
                            "rating": movie[3],
                            "description": movie[4],
                            "releaseDate": movie[5],
                            "createdAt": movie[6],
                            "updatedAt": movie[7],
                        }
                    )
                return movies_dict
    except Exception as e:
        logging.error(f"Error fetching items from the database: {e}")
        raise e
# Fetch interactions

def fetch_interactions() -> list[dict]:
    """
    fetch interactions which is union of
      user_purchases
      "UserLikes"
      only fetch userId and movieId as userId and ItemId respectively
    """
    logging.info("Fetching interactions from the database")

    try:
        fetch_interactions_sql = """
            SELECT
                "userId",
                "itemId",
                "createdAt"
            FROM
                (
                    SELECT
                        "userId",
                        "movieId" AS "itemId",
                        "purchaseDate" AS "createdAt"
                    FROM public."user_purchases"
                    UNION
                    SELECT
                        "userId",
                        "movieId" AS "itemId",
                        "createdAt"
                    FROM public."UserLike"
                ) AS interactions
            """
        with psycopg.Connection.connect(DATABASE_CONNECTION_STRING) as conn:
            with conn.cursor() as cur:
                cur.execute(fetch_interactions_sql)
                interactions = cur.fetchall()
                interactions_dict: list[dict] = []
                for interaction in interactions:
                    interactions_dict.append(
                        {
                            "userId": interaction[0],
                            "itemId": interaction[1],
                            "createdAt": interaction[2]
                        }
                    )
                return interactions_dict
    except Exception as e:
        logging.error(f"Error fetching interactions from the database: {e}")
        raise e
