import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AI_API_KEY = os.getenv("AI_API_KEY")
    AI_API_URL = os.getenv("AI_API_URL", "https://api.example.com/analyze")