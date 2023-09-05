from dotenv import load_dotenv
import os


load_dotenv()

DB_USER = os.environ["DB_USER"] 
DB_PASS = os.environ["DB_PASS"]  
DB_HOST = os.environ["DB_HOST"]  
DB_PORT = os.environ["DB_PORT"] 
STRIPE_SK = os.environ["STRIPE_SK"]
STRIPE_PK = os.environ["STRIPE_PK"]
