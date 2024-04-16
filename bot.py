import os
from dotenv import load_dotenv

load_dotenv()

API_key = os.getenv("API")

print(API_key)