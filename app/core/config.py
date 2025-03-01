from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "nosql_qa_db")
