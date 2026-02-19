from pydantic import BaseModel

class ChatRequest(BaseModel):
    """Esquema para la pregunta del usuario"""
    query: str