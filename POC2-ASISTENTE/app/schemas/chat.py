from pydantic import BaseModel, field_validator

class ChatRequest(BaseModel):
    """
    Esquema para la pregunta del usuario.
    El campo 'query' debe ser un string no vacío.
    """
    query: str

    @field_validator('query')
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("El campo 'query' no puede estar vacío.")
        return v