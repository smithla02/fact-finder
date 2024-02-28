import os
from sqlalchemy import create_engine, Table, Column, String, MetaData
from config import DATABASE_NAME

# Define the path to the database file
database_path = f"{DATABASE_NAME}"

# Delete the existing database file if it exists
if os.path.exists(database_path):
    os.remove(database_path)
    print(f"Deleted existing database: {database_path}")
else:
    print(f"Database file not found: {database_path}")

# Recreate the database with the updated schema
engine = create_engine(f"sqlite:///{DATABASE_NAME}")
metadata = MetaData()
facts_table = Table(
    "facts",
    metadata,
    Column("topic", String, primary_key=True),
    Column("persona", String, primary_key=True),
    Column("facts", String),
    Column("related_topics", String),
)
metadata.create_all(engine)
print(f"Created new database with updated schema: {database_path}")
