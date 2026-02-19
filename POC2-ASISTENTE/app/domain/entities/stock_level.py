from dataclasses import dataclass

@dataclass(frozen=True)
class StockLevel:
	"""Entidad de validación"""
	value: int
	
	def __post_init__(self):
		"""Valida la entrada de datos"""
		if self.value < 0:
			raise ValueError("El nivel de stock no puede ser negativo.")
