import os
from dotenv import load_dotenv

load_dotenv("settings.env")

class Config:
    DOMAIN = os.getenv("DOMAIN", "Generative AI & Deep Learning")
    MAX_RECORDS = int(os.getenv("MAX_RECORDS_PER_TOPIC", 100))
    TOPIC_COUNT = int(os.getenv("TOPIC_COUNT", 5))
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT","python:projectdatacollector:v1.0") 

    RAW_DATA_DIR = os.getenv("RAW_DATA_DIR","./data")
    PLATFORMS = [p.strip() for p in os.getenv("PLATFORMS").split(",")]

    # LLM Variables
    LONGCAT_API_KEY = os.getenv("LONGCAT_API_KEY")
    LONGCAT_MODEL = os.getenv("LONGCAT_MODEL")


    @classmethod
    def ensure_dirs(cls):
        """Creates the data directory if it doesn't already exist."""
        os.makedirs(cls.RAW_DATA_DIR, exist_ok=True)

# Run directory check automatically when config is imported
Config.ensure_dirs()