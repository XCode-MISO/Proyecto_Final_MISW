from sqlalchemy import create_engine
import os

# Replace 'your_database_url' with the actual database URL
database_url = os.environ.get('DATABASE_URL', "localhost:4567")
if database_url is None:
  raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(database_url)

# Test the connection
try:
  with engine.connect():
    print("Database connection successful")
except Exception as e:
  print(f"Error connecting to the database: {str(e)}")
