from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "Cley Intellignet Invetory"
    VERSION: str = "1.0.0"
    API_VERSION_STR: str = "api/v1"

    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_KEY: str
    AZURE_OPENAI_MODEL: str  = "gtp-4o"

    # Azure SQL
    SQL_SERVER: str
    SQL_DATABASE: str
    SQL_USERNAME: Optional[str] = None
    SQL_PASSWORD: Optional[str] = None

    # Azure AI Search
    AZURE_SEARCH_ENDPOINT: str
    AZURE_SEARCH_KEY: str
    AZURE_SEARCH_INDEX: str = "interventory-index"

    # Configuración de Pidantic para leer el .env en desarrollo
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    
settings = Settings()
