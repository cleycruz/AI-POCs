from pydantic import BaseModel
from datetime import datetime

class AnalisisStock(BaseModel):
    """
    Esquema para la respuesta final al usuario.
    Incluye resumen IA, SKU, cantidad, nivel de urgencia y timestamp.

    Ejemplo:
        {
            "resumen": "El stock está bajo el mínimo recomendado.",
            "sku": "PROD-123",
            "cantidad_actual": 5,
            "nivel_urgencia": "ALTA",
            "timestamp": "2026-02-19T12:00:00"
        }
    """
    resumen: str
    sku: str
    cantidad_actual: int
    nivel_urgencia: str
    timestamp: datetime = datetime.now()