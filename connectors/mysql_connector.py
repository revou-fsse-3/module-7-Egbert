from sqlalchemy import create_engine
import os

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database_name = os.getenv("DB_NAME")

print("Connecting to SQL database")

ConnectionString = f'mysql+mysqlconnector://{username}:{password}@{host}/{database_name}'
engine = create_engine(ConnectionString)

connection = engine.connect()

print("Success connection to SQL database")