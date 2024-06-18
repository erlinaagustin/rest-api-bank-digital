import argparse
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from config import get_database_url

# Argument parser setup
parser = argparse.ArgumentParser(description='Bank Digital Application')
parser.add_argument('--db-url', type=str, help='Database URL')
args, unknown = parser.parse_known_args()

# Use the argument if provided, otherwise use the environment variable
database_url = args.db_url if args.db_url else get_database_url()

# SQLAlchemy setup
engine = create_async_engine(
    url=database_url
)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

metadata = MetaData()
Base = declarative_base(metadata=metadata)

async def get_async_session():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
