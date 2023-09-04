from dotenv import load_dotenv
import os


load_dotenv()

DB_USER = os.environ["DB_USER"]  # e.g. 'my-db-user'
DB_PASS = os.environ["DB_PASS"]  # e.g. 'my-db-password'
DB_NAME = os.environ["DB_NAME"]  # e.g. 'my-database'
DB_PORT = os.environ["DB_PORT"] 
