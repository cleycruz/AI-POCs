from pydantic import BaseModel
from datetime import datetime

class AnalisisStock(BaseModel):
    """Esquema para la respuesta final al usuario"""
    resumen: str
    sku: str
    cantidad_actual: int
    nivel_urgencia: str
    timestamp: datetime = datetime.now()