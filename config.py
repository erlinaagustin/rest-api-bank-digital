import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def get_database_url():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")

    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"