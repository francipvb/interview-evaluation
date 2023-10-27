from typing import List, Optional, Union, Dict, Any
from pydantic import AnyUrl, field_validator, BaseModel, ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname("./app/core/.env"), ".env")
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[Union[str, List[str]]] = []

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[Union[str, List[str]]]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: Optional[AnyUrl] = None

    @field_validator("DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[AnyUrl], values: Dict[str, Any]) -> Optional[AnyUrl]:
        if v is not None:
            return v
        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        server = values.get("POSTGRES_SERVER")
        db = values.get("POSTGRES_DB")
        if all([user, password, server, db]):
            db_url = f"postgresql://{user}:{password}@{server}/{db}"
            print("Constructed Database URL:", db_url) 
            return db_url

settings = Settings()