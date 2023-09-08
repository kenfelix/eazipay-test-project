from pymongo import MongoClient
from app.config import settings


def get_db():
    cluster = settings.DB_URL
    db = ""
    try:
        client = MongoClient(cluster)
        db = client.graphql
        print(
            """
            ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️
            --------------------------------------
            Pinged your deployment. 
            You successfully connected to MongoDB!

            -------------------- 🎺️🎺️🎺️🎺️🎺️🎺️
            """
        )
    except Exception as e:
        print(e)
    return db