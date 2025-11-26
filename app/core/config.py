from dotenv import load_dotenv
import os
from pydantic import BaseModel, ValidationError, Field

load_dotenv()

class EnvSchema(BaseModel):
    GITHUB_PAT_TOKEN: str = Field(...,min_length=10)
    OPENAI_API_KEY: str = Field(...,min_length=10)
    OWNER_USERNAME: str = Field(...,min_length=4)
    API_ENDPOINT: str = Field(...,min_length=4)


try:
    env_conf = EnvSchema(
        GITHUB_PAT_TOKEN=os.getenv("GITHUB_PAT_TOKEN"),
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
        OWNER_USERNAME=os.getenv("OWNER_USERNAME"),
        API_ENDPOINT=os.getenv("API_ENDPOINT"),
    )
except ValidationError as e:
    print("Environment configuration error:")
    print(e)
    exit(1)


