from dotenv import load_dotenv
import os
from pydantic import BaseModel, ValidationError, Field

load_dotenv()

class EnvSchema(BaseModel):
    GITHUB_PAT_TOKEN: str = Field(...,min_length=10)

try:
    env_conf = EnvSchema(
        GITHUB_PAT_TOKEN=os.getenv("GITHUB_PAT_TOKEN"),
    )
except ValidationError as e:
    print("Environment configuration error:")
    print(e)
    exit(1)


