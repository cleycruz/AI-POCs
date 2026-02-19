from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ProductStock:
    """Entidad de dominio pura para representar el estado de un producto"""
    id: int
    sku: str
    name: str
    current_quantity: int
    min_threshold: int # Cantidad mínima antes del alerta
    last_update: datetime

    @property
    def is_below_threshold(self) -> bool:
        """Regla del negocio: ¿Estamos en riesgo de quiebre?"""
        return self.current_quantity <= self.min_threshold

    @property
    def calculate_refill_urgency(self) -> str:
        """Lógica de negocio para prorizar pedidos"""
        if self.current_quantity == 0:
            return "CRITICAL"
        if self.is_below_threshold:
            return "HIGH"
        return "NORMAL"
