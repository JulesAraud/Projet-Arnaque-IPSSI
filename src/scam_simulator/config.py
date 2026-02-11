import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    MODEL_VICTIM = os.getenv("MODEL_VICTIM")
    MODEL_DIRECTOR = os.getenv("MODEL_DIRECTOR")
    MODEL_MODERATOR = os.getenv("MODEL_MODERATOR")
